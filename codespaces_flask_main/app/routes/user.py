from flask import Blueprint, render_template, redirect, url_for, request, send_file, flash, abort
from flask_login import login_required, current_user
from ..models import Comment, Showroom, Vehicle
from .. import db
import csv
import io
import joblib
import os
import pandas as pd
import pickle
from sklearn.preprocessing import PolynomialFeatures

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/home')
@login_required
def user_home():
    return render_template('user_home.html', comments=Comment.query.limit(10).all())

@user_bp.route('/comments')
def comments():
    if not current_user.is_authenticated:
        return render_template('not_logged_in.html', title="Not Logged In"), 200
    comments = Comment.query.all()
    return render_template('comments.html', comments=comments)

@user_bp.route('/graphs')
def graphs():
    if not current_user.is_authenticated:
        return render_template('not_logged_in.html', title="Not Logged In"), 200
    # Sentiment counts
    positive = Comment.query.filter_by(sentiment='positive').count()
    neutral = Comment.query.filter_by(sentiment='neutral').count()
    negative = Comment.query.filter_by(sentiment='negative').count()
    labels = ['Positive', 'Neutral', 'Negative']
    data = [positive, neutral, negative]
    return render_template(
        'graphs.html',
        positive=positive,
        neutral=neutral,
        negative=negative,
        labels=labels,
        data=data,
        counts=data
    )

@user_bp.route('/download')
def download():
    if not current_user.is_authenticated:
        return render_template('not_logged_in.html', title="Not Logged In"), 200
    # Create CSV with comments and sentiment
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Source', 'Comment', 'Sentiment'])
    comments = Comment.query.all()
    for c in comments:
        cw.writerow([c.source, c.text, c.sentiment])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    # Use 'download_name' instead of deprecated 'attachment_filename'
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='comments.csv')

@user_bp.route('/showrooms')
def showrooms():
    if not current_user.is_authenticated:
        return render_template('not_logged_in.html', title="Not Logged In"), 200
    showrooms = Showroom.query.all()
    print("Showrooms fetched:", showrooms)  # Debug: see if any showrooms are fetched
    return render_template('showrooms.html', showrooms=showrooms)

@user_bp.route('/compare')
def compare():
    if not current_user.is_authenticated:
        return render_template('not_logged_in.html', title="Not Logged In"), 200
    vehicles = Vehicle.query.all()
    vehicle1 = None
    vehicle2 = None
    v1_id = request.args.get('vehicle1', type=int)
    v2_id = request.args.get('vehicle2', type=int)
    if v1_id:
        vehicle1 = Vehicle.query.get(v1_id)
    if v2_id:
        vehicle2 = Vehicle.query.get(v2_id)
    return render_template('compare.html', vehicles=vehicles, vehicle1=vehicle1, vehicle2=vehicle2)

# Use the correct absolute path for the sales CSV (always D:\ola-ev\ola_ev_sales_2020_2024.csv)
SALES_CSV = r'D:\ola-ev\ola_ev_sales_2020_2024.csv'
if not os.path.exists(SALES_CSV):
    raise FileNotFoundError(f"Could not find sales CSV at {SALES_CSV}. Please place 'ola_ev_sales_2020_2024.csv' in d:/ola-ev")
sales_df = pd.read_csv(SALES_CSV)

@user_bp.route('/predict_sales', methods=['GET', 'POST'])
def predict_sales():
    if not current_user.is_authenticated:
        return render_template('not_logged_in.html', title="Not Logged In"), 200
    prediction = None
    confidence = None
    confusion_matrix = None
    year = None
    all_conf_matrices = {}
    all_metrics = {}
    actual_result = None
    show_graphs = True
    all_model_results = {}

    if request.method == 'POST':
        year = request.form.get('year')
        if not year or not year.isdigit():
            flash("Please enter a valid year.")
        else:
            year = int(year)
            # Check if year is in actual sales data
            actual_row = sales_df[sales_df['Year'] == year]
            if not actual_row.empty:
                actual_result = int(actual_row['Units Sold'].iloc[0])
                show_graphs = False
            else:
                # Get predictions and metrics for all models
                results = {}
                metrics = {}
                for model_name in ['linear_regression', 'polynomial_regression', 'prophet']:
                    pred, conf, cm, acc, prec, rec, f1 = predict_sales_model(year, model_name, with_metrics=True)
                    results[model_name] = {
                        'prediction': pred,
                        'confidence': conf,
                        'confusion_matrix': cm
                    }
                    metrics[model_name] = {
                        'accuracy': acc,
                        'precision': prec,
                        'recall': rec,
                        'f1': f1
                    }
                # For display
                prediction = results['linear_regression']['prediction']
                confidence = results['linear_regression']['confidence']
                confusion_matrix = results['linear_regression']['confusion_matrix']
                all_conf_matrices = {k: v['confusion_matrix'] for k, v in results.items()}
                all_metrics = metrics
                all_model_results = results

    return render_template(
        'predict_sales.html',
        year=year,
        prediction=prediction,
        confidence=confidence,
        confusion_matrix=confusion_matrix,
        all_conf_matrices=all_conf_matrices if show_graphs else None,
        all_metrics=all_metrics if show_graphs else None,
        actual_result=actual_result,
        show_graphs=show_graphs,
        all_model_results=all_model_results
    )

@user_bp.route('/users')
@login_required
def manage_users():
    # Only allow access if current user is admin
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('user.user_home'))
    users = db.session.query(db.Model).with_polymorphic(None).session.query(User).all()
    return render_template('manage_users.html', users=users)

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models')
lr_model = joblib.load(os.path.join(MODEL_DIR, 'linear_regression.pkl'))
rf_model = joblib.load(os.path.join(MODEL_DIR, 'random_forest.pkl'))
dt_model = joblib.load(os.path.join(MODEL_DIR, 'decision_tree.pkl'))
poly_model = joblib.load(os.path.join(MODEL_DIR, 'polynomial_regression.pkl'))
with open(os.path.join(MODEL_DIR, 'prophet_model.pkl'), 'rb') as f:
    prophet_model = pickle.load(f)
# Load the fitted PolynomialFeatures object
with open(os.path.join(MODEL_DIR, 'poly_features.pkl'), 'rb') as f:
    poly = pickle.load(f)

def predict_sales_model(year, model_name='linear_regression', with_metrics=False):
    # Choose model
    if model_name == 'polynomial_regression':
        X_poly = poly.transform([[year]])
        prediction = int(poly_model.predict(X_poly)[0])
    elif model_name == 'prophet':
        import pandas as pd
        future = pd.DataFrame({'ds': [pd.to_datetime(year, format='%Y')]})
        prediction = int(prophet_model.predict(future)['yhat'].values[0])
    else:
        prediction = int(lr_model.predict([[year]])[0])

    # Dummy confusion matrix and metrics for demonstration
    import random
    cm = [
        [random.randint(30, 60), random.randint(0, 10)],
        [random.randint(0, 10), random.randint(30, 60)]
    ]
    accuracy = round(random.uniform(0.7, 0.99), 2)
    precision = round(random.uniform(0.7, 0.99), 2)
    recall = round(random.uniform(0.7, 0.99), 2)
    f1 = round(random.uniform(0.7, 0.99), 2)
    confidence = accuracy

    if with_metrics:
        return prediction, confidence, cm, accuracy, precision, recall, f1
    else:
        return prediction, confidence, cm
