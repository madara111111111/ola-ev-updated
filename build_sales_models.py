import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
import numpy as np
from prophet import Prophet

# Load data using a relative path for portability
csv_path = os.path.join(os.path.dirname(__file__), "ola_ev_sales_2020_2024.csv")
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Could not find CSV at {csv_path}. Please place 'ola_ev_sales_2020_2024.csv' in the same folder as this script.")
df = pd.read_csv(csv_path)
X = df[['Year']].values
y = df['Units Sold'].values

# For demonstration, let's treat this as a classification problem by binning sales
# (since confusion matrix and classification metrics don't apply to regression directly)
# We'll classify years as "Low" or "High" sales based on median
median_sales = np.median(y)
y_class = (y > median_sales).astype(int)  # 0: Low, 1: High

# Fit models for regression
lr = LinearRegression()
lr.fit(X, y)

# Polynomial Regression (degree 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
poly_lr = LinearRegression()
poly_lr.fit(X_poly, y)

# Define MODEL_DIR before saving any models
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'codespaces-flask-main', 'app', 'ml_models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Save PolynomialFeatures
import pickle
with open(os.path.join(MODEL_DIR, 'poly_features.pkl'), 'wb') as f:
    pickle.dump(poly, f)

# Prophet model (expects a DataFrame with columns 'ds' and 'y')
df_prophet = df.rename(columns={'Year': 'ds', 'Units Sold': 'y'})
df_prophet['ds'] = pd.to_datetime(df_prophet['ds'], format='%Y')
prophet_model = Prophet(yearly_seasonality=True, daily_seasonality=False)
prophet_model.fit(df_prophet)

# Predict for regression metrics
models = {
    'Linear Regression': lr,
    'Polynomial Regression': poly_lr,
    'Prophet': prophet_model
}
for name, model in models.items():
    if name == 'Polynomial Regression':
        y_pred = model.predict(X_poly)
    elif name == 'Prophet':
        future = pd.DataFrame({'ds': pd.to_datetime(df['Year'], format='%Y')})
        y_pred = model.predict(future)['yhat'].values
    else:
        y_pred = model.predict(X)
    print(f"\n{name} Regression Metrics:")
    print("R2 Score:", r2_score(y, y_pred))
    print("MAE:", mean_absolute_error(y, y_pred))
    print("MSE:", mean_squared_error(y, y_pred))

    # For classification metrics, bin predictions
    y_pred_class = (y_pred > median_sales).astype(int)
    print("Confusion Matrix:\n", confusion_matrix(y_class, y_pred_class))
    print("Accuracy:", accuracy_score(y_class, y_pred_class))
    print("Precision:", precision_score(y_class, y_pred_class, zero_division=0))
    print("Recall:", recall_score(y_class, y_pred_class, zero_division=0))
    print("F1 Score:", f1_score(y_class, y_pred_class, zero_division=0))

# For Prophet, ensure the input is year and output is sales
# (already handled: input is year, output is predicted sales)

# Example usage for prediction (for reference, not part of training script):
# year = 2025
# X_input = [[year]]
# y_pred_lr = lr.predict(X_input)[0]
# y_pred_poly = poly_lr.predict(poly.transform(X_input))[0]
# future = pd.DataFrame({'ds': [pd.to_datetime(year, format='%Y')]})
# y_pred_prophet = prophet_model.predict(future)['yhat'].values[0]

# Save models
joblib.dump(lr, os.path.join(MODEL_DIR, 'linear_regression.pkl'))
joblib.dump(poly_lr, os.path.join(MODEL_DIR, 'polynomial_regression.pkl'))

# Save Prophet model using pickle
import pickle
with open(os.path.join(MODEL_DIR, 'prophet_model.pkl'), 'wb') as f:
    pickle.dump(prophet_model, f)

print("Models trained and saved to", MODEL_DIR)
