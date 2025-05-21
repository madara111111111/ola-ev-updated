import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
import numpy as np

# Load data using a relative path for portability
csv_path = os.path.join(os.path.dirname(__file__), "ola_ev_sales_2020_2024.csv")
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
rf = RandomForestRegressor(random_state=42)
rf.fit(X, y)
dt = DecisionTreeRegressor(random_state=42)
dt.fit(X, y)

# Predict for regression metrics
models = {'Linear Regression': lr, 'Random Forest': rf, 'Decision Tree': dt}
for name, model in models.items():
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

# Save models
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'codespaces-flask-main', 'app', 'ml_models')
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(lr, os.path.join(MODEL_DIR, 'linear_regression.pkl'))
joblib.dump(rf, os.path.join(MODEL_DIR, 'random_forest.pkl'))
joblib.dump(dt, os.path.join(MODEL_DIR, 'decision_tree.pkl'))

print("Models trained and saved to", MODEL_DIR)
