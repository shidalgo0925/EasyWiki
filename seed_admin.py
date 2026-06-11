# -*- coding: utf-8 -*-
"""
Script de seed: crea usuarios iniciales.
Ejecutar: python seed_admin.py
"""
import os
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import get_db
from app.models.users import User

os.environ.setdefault("DATABASE_URL", "sqlite:///easycoach_dev.db")

USERS_SEED = [
    {"email": "admin@easycoach.app", "nombre": "Administrador", "password": "admin123"},
    {"email": "shidalgo@easytech.services", "nombre": "Seul", "password": "easy2026"},
    {"email": "test@example.com", "nombre": "Test User", "password": "test123"},
]


def create_user(db, email, nombre, password):
    if db.query(User).filter(User.email == email).first():
        print(f"  {email} — ya existe.")
        return False
    user = User(
        email=email,
        nombre=nombre,
        password_hash=generate_password_hash(password),
        is_active=True,
    )
    db.add(user)
    print(f"  {email} — creado.")
    return True


app = create_app()
with app.app_context():
    db = get_db()
    created = 0
    for u in USERS_SEED:
        if create_user(db, u["email"], u["nombre"], u["password"]):
            created += 1
    if created:
        db.commit()
        print(f"\nTotal usuarios creados: {created}")
    else:
        print("\nTodos los usuarios ya existen.")
