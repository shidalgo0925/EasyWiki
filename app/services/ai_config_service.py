# -*- coding: utf-8 -*-
"""Config IA por usuario — pantalla estilo CLINE."""
import os
from typing import Optional

import config as app_config
from app.extensions import get_db
from app.models.coach_ai_config import CoachAIConfig

PROVIDER_DEFAULTS = {
    "rules": {"model": "rules", "base_url": "", "hint": "Modo reglas internas. No requiere API externa."},
    "openai": {"model": "gpt-4o-mini", "base_url": "https://api.openai.com/v1", "hint": "OpenAI — GPT-4o, GPT-4o mini."},
    "kimi": {"model": "moonshot-v1-8k", "base_url": "https://api.moonshot.cn/v1", "hint": "Kimi / Moonshot — compatible OpenAI API."},
    "claude": {"model": "claude-sonnet-4-20250514", "base_url": "https://api.anthropic.com", "hint": "Anthropic Claude — API nativa."},
    "gemini": {"model": "gemini-2.0-flash", "base_url": "https://generativelanguage.googleapis.com", "hint": "Google Gemini."},
    "ollama": {"model": "qwen2.5-coder:14b", "base_url": "http://127.0.0.1:11434", "hint": "Ollama — modelos locales o servidor remoto."},
}

MODEL_SUGGESTIONS = {
    "openai": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
    "kimi": ["moonshot-v1-8k", "moonshot-v1-32k"],
    "claude": ["claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022"],
    "gemini": ["gemini-2.0-flash", "gemini-1.5-pro"],
    "ollama": ["qwen2.5-coder:14b", "qwen2.5:7b", "llama3.2", "codellama"],
    "rules": ["rules"],
}


def config_to_dict(cfg: CoachAIConfig) -> dict:
    return {
        "api_provider": cfg.api_provider,
        "use_custom_base_url": cfg.use_custom_base_url,
        "base_url": cfg.base_url or "",
        "api_key": cfg.api_key or "",
        "api_key_set": bool(cfg.api_key),
        "model": cfg.model,
        "context_window": cfg.context_window,
        "request_timeout_ms": cfg.request_timeout_ms,
        "use_compact_prompt": cfg.use_compact_prompt,
    }


def env_defaults() -> dict:
    provider = app_config.AI_PROVIDER or "rules"
    defaults = PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["rules"])
    return {
        "api_provider": provider,
        "use_custom_base_url": bool(os.environ.get("OLLAMA_BASE_URL") or os.environ.get("KIMI_BASE_URL")),
        "base_url": os.environ.get("OLLAMA_BASE_URL") or os.environ.get("KIMI_BASE_URL") or defaults["base_url"],
        "api_key": "",
        "api_key_set": bool(app_config.OPENAI_API_KEY or os.environ.get("KIMI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")),
        "model": app_config.AI_MODEL or defaults["model"],
        "context_window": 4096,
        "request_timeout_ms": 180000,
        "use_compact_prompt": False,
    }


def get_user_ai_config(user_id: int) -> dict:
    db = get_db()
    cfg = db.query(CoachAIConfig).filter(CoachAIConfig.user_id == user_id).first()
    if cfg:
        return config_to_dict(cfg)
    return env_defaults()


def get_user_ai_config_row(user_id: int) -> Optional[CoachAIConfig]:
    db = get_db()
    return db.query(CoachAIConfig).filter(CoachAIConfig.user_id == user_id).first()


def save_user_ai_config(user_id: int, data: dict) -> CoachAIConfig:
    db = get_db()
    cfg = get_user_ai_config_row(user_id)
    if not cfg:
        cfg = CoachAIConfig(user_id=user_id)
        db.add(cfg)

    cfg.api_provider = data.get("api_provider", cfg.api_provider or "rules")
    cfg.use_custom_base_url = bool(data.get("use_custom_base_url"))
    cfg.base_url = (data.get("base_url") or "").strip() or None
    new_key = (data.get("api_key") or "").strip()
    if new_key:
        cfg.api_key = new_key
    cfg.model = (data.get("model") or cfg.model or "gpt-4o-mini").strip()
    cfg.context_window = int(data.get("context_window") or 4096)
    cfg.request_timeout_ms = int(data.get("request_timeout_ms") or 180000)
    cfg.use_compact_prompt = bool(data.get("use_compact_prompt"))

    db.commit()
    db.refresh(cfg)
    return cfg


def resolve_api_key(cfg: CoachAIConfig) -> str:
    if cfg.api_key:
        return cfg.api_key
    provider = cfg.api_provider
    if provider == "openai":
        return app_config.OPENAI_API_KEY or ""
    if provider == "kimi":
        return os.environ.get("KIMI_API_KEY", "")
    if provider == "claude":
        return os.environ.get("ANTHROPIC_API_KEY", "")
    if provider == "gemini":
        return os.environ.get("GEMINI_API_KEY", "")
    return ""
