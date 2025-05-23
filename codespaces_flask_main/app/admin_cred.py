# Fix import for direct script execution
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Change import to match your package structure
from codespaces_flask_main.app import db
from codespaces_flask_main.app.models import User
from werkzeug.security import generate_password_hash
from codespaces_flask_main.app import create_app

app = create_app()

with app.app_context():
    admin = User(
        username="admin",
        email="admin@example.com",
        password=generate_password_hash("admin123"),
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()