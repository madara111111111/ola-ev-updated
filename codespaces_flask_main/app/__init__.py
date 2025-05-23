from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    @app.route('/')
    def index():
        return render_template('index.html', title="Ola EV Sentiment App")

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        # Preload admin credentials if not present
        admin_username = "admin"
        admin_email = "admin@example.com"
        admin_password = "admin123"
        admin = User.query.filter_by(username=admin_username, role="admin").first()
        if not admin:
            admin = User(
                username=admin_username,
                email=admin_email,
                password=generate_password_hash(admin_password),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    return app
