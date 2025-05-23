from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import User, Vehicle, Showroom, Comment
from .. import db
from ..scraper import scrape_comments
from ..sentiment import analyze_sentiment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    from functools import wraps
    from flask import abort
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view

@admin_bp.route('/home')
@login_required
@admin_required
def admin_home():
    return render_template('admin_home.html')

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    total_comments = Comment.query.count()
    pos = Comment.query.filter_by(sentiment='positive').count()
    neu = Comment.query.filter_by(sentiment='neutral').count()
    neg = Comment.query.filter_by(sentiment='negative').count()
    labels = ['Positive', 'Neutral', 'Negative']
    counts = [pos, neu, neg]
    return render_template(
        'analytics.html',
        total_comments=total_comments,
        pos=pos,
        neu=neu,
        neg=neg,
        labels=labels,
        counts=counts
    )

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@admin_bp.route('/scrape')
@login_required
@admin_required
def scrape_and_store():
    comments = scrape_comments()
    count = 0
    for c in comments:
        # Check if comment already exists to avoid duplicates
        if not Comment.query.filter_by(text=c['text']).first():
            sentiment = analyze_sentiment(c['text'])
            new_comment = Comment(source=c['source'], text=c['text'], sentiment=sentiment)
            db.session.add(new_comment)
            count += 1
    db.session.commit()
    flash(f'Scraped and added {count} new comments.')
    return redirect(url_for('admin.admin_home'))

# @admin_bp.route('/manage_data', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def manage_data():
#     if request.method == 'POST':
#         # Add vehicle
#         if 'add_vehicle' in request.form:
#             model_name = request.form.get('model_name')
#             price = request.form.get('price')
#             top_speed = request.form.get('top_speed')
#             range_ = request.form.get('range')
#             features = request.form.get('features')
#             if model_name:
#                 v = Vehicle(
#                     model_name=model_name,
#                     price=price,
#                     top_speed=top_speed,
#                     range=range_,
#                     features=features
#                 )
#                 db.session.add(v)
#                 db.session.commit()
#                 flash('Vehicle added successfully.')
#
#         # Add showroom
#         if 'add_showroom' in request.form:
#             name = request.form.get('name')
#             district = request.form.get('district')
#             address = request.form.get('address')
#             phone = request.form.get('phone')
#             map_link = request.form.get('map_link')
#             if name:
#                 s = Showroom(
#                     name=name,
#                     district=district,
#                     address=address,
#                     phone=phone,
#                     map_link=map_link
#                 )
#                 db.session.add(s)
#                 db.session.commit()
#                 flash('Showroom added successfully.')
#     vehicles = Vehicle.query.all()
#     showrooms = Showroom.query.all()
#     return render_template('manage_data.html', vehicles=vehicles, showrooms=showrooms)

@admin_bp.route('/add_vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if current_user.role != 'admin':
        flash('Unauthorized')
        return redirect(url_for('admin.admin_home'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        top_speed = request.form.get('top_speed')
        battery = request.form.get('battery')
        weight = request.form.get('weight')
        range_ = request.form.get('range')
        if name and price and top_speed and battery and weight and range_:
            vehicle = Vehicle(
                name=name,
                price=price,
                top_speed=top_speed,
                battery=battery,
                weight=weight,
                range=range_
            )
            db.session.add(vehicle)
            db.session.commit()
            flash('Vehicle added successfully!')
            return redirect(url_for('admin.admin_home'))
        else:
            flash('All fields are required.')
    return render_template('add_vehicle.html')

@admin_bp.route('/add_showroom', methods=['GET', 'POST'])
@login_required
def add_showroom():
    if current_user.role != 'admin':
        flash('Unauthorized')
        return redirect(url_for('admin.admin_home'))
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        map_link = request.form.get('map_link')
        if name and address:
            showroom = Showroom(
                name=name,
                address=address,
                phone=phone,
                map_link=map_link
            )
            db.session.add(showroom)
            db.session.commit()
            flash('Showroom added successfully!')
            return redirect(url_for('admin.admin_home'))
        else:
            flash('Name and address are required.')
    return render_template('add_showroom.html')

@admin_bp.route('/vehicles')
@login_required
@admin_required
def view_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('view_vehicles.html', vehicles=vehicles)

@admin_bp.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
@login_required
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle deleted successfully!')
    return redirect(url_for('admin.view_vehicles'))

@admin_bp.route('/showrooms')
@login_required
@admin_required
def view_showrooms():
    showrooms = Showroom.query.all()
    return render_template('view_showrooms.html', showrooms=showrooms)

@admin_bp.route('/delete_showroom/<int:showroom_id>', methods=['POST'])
@login_required
@admin_required
def delete_showroom(showroom_id):
    showroom = Showroom.query.get_or_404(showroom_id)
    db.session.delete(showroom)
    db.session.commit()
    flash('Showroom deleted successfully!')
    return redirect(url_for('admin.view_showrooms'))
