# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session, g

from app.services.coach_assistant_service import assistant

coach_ai_bp = Blueprint("coach_ai", __name__, url_prefix="/api/coach")


def _uid():
    return session.get("user_id")


def _user_name():
    if getattr(g, "current_user", None):
        return g.current_user.nombre or g.current_user.email.split("@")[0]
    return ""


def _handle_message(data: dict):
    uid = _uid()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    result = assistant.send_message(
        user_id=uid,
        message=data.get("message", ""),
        source=data.get("source", data.get("screen_context", "floating_chat")),
        activity_id=data.get("activity_id"),
        screen_context=data.get("screen_context"),
        conversation_id=data.get("conversation_id"),
        user_name=_user_name(),
        provider=data.get("provider"),
        model=data.get("model"),
    )
    return jsonify(result), (200 if result.get("ok") else 400)


@coach_ai_bp.post("/message")
def message():
    return _handle_message(request.get_json(force=True, silent=True) or {})


@coach_ai_bp.post("/chat")
def chat():
    """Alias retrocompatible."""
    return _handle_message(request.get_json(force=True, silent=True) or {})


@coach_ai_bp.get("/context")
def context():
    uid = _uid()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    ctx = assistant.get_context(
        uid,
        screen_context=request.args.get("screen_context", "dashboard"),
        activity_id=request.args.get("activity_id", type=int),
        user_name=_user_name(),
    )
    return jsonify({"ok": True, "context": ctx})


@coach_ai_bp.get("/conversation")
def conversation():
    uid = _uid()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    from app.services.coach_memory_service import get_latest_conversation
    conv = get_latest_conversation(uid, source=request.args.get("source"))
    if not conv:
        return jsonify({"ok": True, "conversation": None})
    return jsonify({
        "ok": True,
        "conversation": {
            "id": conv.id,
            "title": conv.title,
            "source": conv.source or conv.screen_context,
            "provider": conv.provider_used,
            "model": conv.model_used,
        },
    })


@coach_ai_bp.post("/activity/<int:activity_id>/message")
def activity_message(activity_id):
    data = request.get_json(force=True, silent=True) or {}
    data["activity_id"] = activity_id
    data.setdefault("source", "activity")
    return _handle_message(data)


@coach_ai_bp.post("/daily-recommendation")
def daily_recommendation():
    uid = _uid()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    return jsonify(assistant.daily_recommendation(uid, user_name=_user_name()))


@coach_ai_bp.get("/models")
def models_catalog():
    return jsonify({"ok": True, "models": assistant.list_models()})


@coach_ai_bp.get("/history/<int:conversation_id>")
def history(conversation_id):
    uid = _uid()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    return jsonify({"ok": True, "messages": assistant.get_history(uid, conversation_id)})
