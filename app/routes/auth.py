# -*- coding: utf-8 -*-
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import config as app_config
from ..extensions import get_db, get_current_user_id
from ..models.users import User

auth_bp = Blueprint("auth", __name__)


# --- Google OAuth: tokens en base de datos ---

def _get_user():
    user_id = get_current_user_id()
    if not user_id:
        return None
    db = get_db()
    return db.query(User).filter(User.id == user_id).first()


def get_credentials():
    """
    Recupera credenciales de Google desde la columna google_refresh_token del usuario autenticado.
    """
    user = _get_user()
    if not user or not user.google_refresh_token:
        return None
    try:
        return Credentials.from_authorized_user_info(
            {
                "refresh_token": user.google_refresh_token,
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": _get_client_id(),
                "client_secret": _get_client_secret(),
            },
            app_config.GOOGLE_SCOPES,
        )
    except Exception:
        return None


def _get_client_id():
    import json
    data = json.loads(Path(app_config.CLIENT_SECRETS_FILE).read_text(encoding="utf-8"))
    return data["installed"]["client_id"] if "installed" in data else data["web"]["client_id"]


def _get_client_secret():
    import json
    data = json.loads(Path(app_config.CLIENT_SECRETS_FILE).read_text(encoding="utf-8"))
    return data["installed"]["client_secret"] if "installed" in data else data["web"]["client_secret"]


def _save_credentials_to_user(creds):
    user = _get_user()
    if not user:
        return False
    db = get_db()
    user.google_refresh_token = creds.refresh_token or creds.token
    db.commit()
    return True


@auth_bp.route("/google/connect")
def google_connect():
    if not current_app.secret_key:
        return "SECRET_KEY no configurada", 500
    flow = Flow.from_client_secrets_file(
        client_secrets_file=app_config.CLIENT_SECRETS_FILE,
        scopes=app_config.GOOGLE_SCOPES,
        redirect_uri=app_config.OAUTH_REDIRECT_URI,
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@auth_bp.route("/oauth2callback")
def oauth2callback():
    state_from_google = request.args.get("state")
    state_expected = session.get("oauth_state")
    if not state_from_google or state_from_google != state_expected:
        return "Estado OAuth inválido", 400
    flow = Flow.from_client_secrets_file(
        client_secrets_file=app_config.CLIENT_SECRETS_FILE,
        scopes=app_config.GOOGLE_SCOPES,
        redirect_uri=app_config.OAUTH_REDIRECT_URI,
    )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    _save_credentials_to_user(creds)
    flash("Google Calendar conectado", "success")
    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/google/disconnect")
def google_disconnect():
    user = _get_user()
    if user:
        db = get_db()
        user.google_refresh_token = None
        db.commit()
    flash("Google Calendar desconectado", "info")
    return redirect(url_for("dashboard.dashboard"))


# --- Autenticación local (login/register) ---


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        user = db.query(User).filter(User.email == email, User.is_active == True).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["user_email"] = user.email
            flash(f"Bienvenido, {user.nombre or user.email}", "success")
            return redirect(url_for("dashboard.dashboard"))
        flash("Credenciales inválidas", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        nombre = request.form.get("nombre", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not email or not password:
            flash("Email y contraseña son obligatorios", "warning")
            return redirect(url_for("auth.register"))
        if password != confirm:
            flash("Las contraseñas no coinciden", "warning")
            return redirect(url_for("auth.register"))
        db = get_db()
        if db.query(User).filter(User.email == email).first():
            flash("El email ya está registrado", "warning")
            return redirect(url_for("auth.register"))
        user = User(
            email=email,
            nombre=nombre or None,
            password_hash=generate_password_hash(password),
        )
        db.add(user)
        db.commit()
        session["user_id"] = user.id
        session["user_email"] = user.email
        flash("Cuenta creada exitosamente", "success")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("register.html")