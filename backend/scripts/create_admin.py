"""
Create initial admin user.
Usage: py -3.13 scripts/create_admin.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User

USERNAME = "admin"
PASSWORD = "admin123"
EMAIL = "admin@apiforge.com"

db = SessionLocal()

existing = db.query(User).filter(User.username == USERNAME).first()
if existing:
    print(f"User '{USERNAME}' already exists.")
else:
    user = User(
        username=USERNAME,
        password_hash=hash_password(PASSWORD),
        email=EMAIL,
        role="admin",
        is_active=1,
    )
    db.add(user)
    db.commit()
    print(f"Admin user created: {USERNAME} / {PASSWORD}")

db.close()
