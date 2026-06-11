# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session, flash

from app.services.ai_config_service import (
    get_user_ai_config,
    save_user_ai_config,
    PROVIDER_DEFAULTS,
    MODEL_SUGGESTIONS,
)
from app.services.ai_provider_router import build_router_for_user

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


def _uid():
    return session.get("user_id")


@settings_bp.route("/ai", methods=["GET", "POST"])
def ai_settings():
    uid = _uid()
    if not uid:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        data = {
            "api_provider": request.form.get("api_provider", "rules"),
            "use_custom_base_url": request.form.get("use_custom_base_url") == "1",
            "base_url": request.form.get("base_url", ""),
            "api_key": request.form.get("api_key", ""),
            "model": request.form.get("model", ""),
            "context_window": request.form.get("context_window", 4096),
            "request_timeout_ms": request.form.get("request_timeout_ms", 180000),
            "use_compact_prompt": request.form.get("use_compact_prompt") == "1",
        }
        save_user_ai_config(uid, data)
        flash("Configuración guardada.", "success")
        return redirect(url_for("settings.ai_settings"))

    cfg = get_user_ai_config(uid)
    provider = cfg.get("api_provider", "rules")
    return render_template(
        "settings/ai.html",
        cfg=cfg,
        providers=PROVIDER_DEFAULTS,
        model_suggestions=MODEL_SUGGESTIONS,
        provider_hint=PROVIDER_DEFAULTS.get(provider, {}).get("hint", ""),
    )


@settings_bp.post("/ai/test")
def ai_test():
    uid = _uid()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    try:
        router = build_router_for_user(uid)
        result = router.chat([{"role": "user", "content": "Responde solo: OK"}], temperature=0)
        return jsonify({"ok": True, "message": result.get("content", "")[:200], "provider": result.get("provider"), "model": result.get("model")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)[:300]})


@settings_bp.get("/ai/models")
def ai_list_models():
    uid = _uid()
    if not uid:
        return jsonify({"ok": False}), 401
    provider = request.args.get("provider", "ollama")
    base_url = request.args.get("base_url", "").rstrip("/")
    if provider == "ollama" and base_url:
        try:
            import requests
            r = requests.get(f"{base_url}/api/tags", timeout=10)
            r.raise_for_status()
            names = [m["name"] for m in r.json().get("models", [])]
            return jsonify({"ok": True, "models": names})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e), "models": MODEL_SUGGESTIONS.get("ollama", [])})
    return jsonify({"ok": True, "models": MODEL_SUGGESTIONS.get(provider, [])})
