# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Archivo de credenciales de OAuth2 (descargado de Google Cloud Console)
# Pon el JSON aquí o cambia la ruta absoluta si lo tienes en otro lado
CLIENT_SECRETS_FILE = os.environ.get(
    "CLIENT_SECRETS_FILE",
    os.path.join(BASE_DIR, "client_secret.json"),
)

# Dónde guardar el token de usuario
TOKEN_FILE = os.environ.get(
    "TOKEN_FILE",
    os.path.join(BASE_DIR, ".secrets", "token.json"),
)

# Redirect URI registrado en Google (debe coincidir 1:1)
OAUTH_REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI",
    "https://focus.easytech.services/oauth2callback",
)

# Scopes para leer y escribir eventos
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

# Zona horaria local
LOCAL_TZ = os.environ.get("LOCAL_TZ", "America/Panama")

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://onepercent_user:STRONG_PASS@localhost:5432/onepercent_db"
)
SQLALCHEMY_ECHO = os.environ.get("SQL_ECHO", "0") == "1"

# OpenAI / IA
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", os.environ.get("AI_MODEL", "gpt-4o-mini"))
AI_PROVIDER = os.environ.get("AI_PROVIDER", "rules")
AI_MODEL = os.environ.get("AI_MODEL", OPENAI_MODEL)
AI_TIMEOUT_SECONDS = int(os.environ.get("AI_TIMEOUT_SECONDS", "60"))
AI_MAX_TOKENS = int(os.environ.get("AI_MAX_TOKENS", "1200"))
AI_TEMPERATURE = float(os.environ.get("AI_TEMPERATURE", "0.4"))
AI_FALLBACK_ENABLED = os.environ.get("AI_FALLBACK_ENABLED", "true").lower() == "true"
AI_FALLBACK_PROVIDERS = os.environ.get("AI_FALLBACK_PROVIDERS", "openai,ollama,rules").split(",")
