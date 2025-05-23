# Admin Credentials Information

By default, admin credentials are not hardcoded in the project for security reasons.

## How to create an admin user

1. **Via the database shell (recommended for SQLite):**
   - Open a Python shell in your project environment:
     ```python
     from codespaces_flask_main.app import db
     from codespaces_flask_main.app.models import User
     from werkzeug.security import generate_password_hash

     admin = User(
         username="admin",
         email="admin@example.com",
         password=generate_password_hash("your_admin_password"),
         role="admin"
     )
     db.session.add(admin)
     db.session.commit()
     ```
   - Replace `"admin"` and `"your_admin_password"` with your desired username and password.

2. **Or, add an admin user directly in your database using a tool like DB Browser for SQLite.**

## Default Admin Credentials

- **There are no default admin credentials unless you create them as above.**
- If you want a default, you can add logic to create one if not present on app startup (not recommended for production).

---

**Summary:**  
- Create an admin user manually in your database.
- Use the username and password you set when creating the admin.
- Never share admin credentials publicly.
