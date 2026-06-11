# -*- coding: utf-8 -*-
import os
from flask import Flask, g, session
from dotenv import load_dotenv
from .extensions import init_db, Base, engine, get_db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")
    if not app.secret_key:
        raise RuntimeError("SECRET_KEY no configurada. Crear archivo .env o definir variable de entorno.")

    # current_user disponible en todos los templates
    @app.before_request
    def load_current_user():
        from .models.users import User
        user_id = session.get("user_id")
        g.current_user = None
        if user_id:
            db = get_db()
            g.current_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        g.user_logged_in = g.current_user is not None

    @app.context_processor
    def inject_globals():
        return {
            "current_user": getattr(g, "current_user", None),
            "user_logged_in": getattr(g, "user_logged_in", False),
        }

    # Blueprints
    from .routes.dashboard import dashboard_bp, misc_bp
    from .routes.auth import auth_bp
    from .routes.wizard_ai_plan import ai_wizard_bp
    from .routes.api_ai_plan import api_ai_bp
    from .routes.visions import visions_bp
    from .routes.daily_close import daily_close_bp
    from .routes.strategy import strategy_bp
    from .routes.wizard_treatment import treatment_wizard_bp
    from .routes.api_treatment import api_treatment_bp
    from .routes.coach_activity import coach_bp, activity_wizard_bp
    from .routes.coach_ai import coach_ai_bp
    from .routes.settings import settings_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_wizard_bp)
    app.register_blueprint(api_ai_bp)
    app.register_blueprint(visions_bp)
    app.register_blueprint(daily_close_bp)
    app.register_blueprint(strategy_bp)
    app.register_blueprint(treatment_wizard_bp)
    app.register_blueprint(api_treatment_bp)
    app.register_blueprint(coach_bp)
    app.register_blueprint(activity_wizard_bp)
    app.register_blueprint(coach_ai_bp)
    app.register_blueprint(settings_bp)

    # DB
    init_db(app)

    return app
