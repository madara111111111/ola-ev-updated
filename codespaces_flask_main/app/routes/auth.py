from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            flash('Please use the admin login page for admin accounts.')
            return redirect(url_for('auth.admin_login'))
        else:
            return redirect(url_for('user.user_home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, role='viewer').first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials or not a user account')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('user.user_home'))

    return render_template('login.html')

@auth_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    from ..models import User
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_home'))
        else:
            flash('You are not authorized to access the admin panel.')
            return redirect(url_for('user.user_home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid admin credentials')
            return redirect(url_for('auth.admin_login'))
        login_user(user)
        return redirect(url_for('admin.admin_home'))

    return render_template('admin_login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password != confirm:
            flash("Passwords don't match")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role='viewer'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/not_logged_in')
def not_logged_in():
    return render_template('not_logged_in.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
