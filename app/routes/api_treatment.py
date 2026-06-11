# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session

from app.services.treatment_service import (
    get_active_treatment,
    get_latest_draft,
    build_prefill,
    save_treatment,
    activate_treatment,
    treatment_to_dict,
)

api_treatment_bp = Blueprint("api_treatment", __name__, url_prefix="/api/treatment")


def _user_id():
    return session.get("user_id")


@api_treatment_bp.get("/prefill")
def prefill():
    uid = _user_id()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401
    return jsonify({"ok": True, "prefill": build_prefill(uid)})


@api_treatment_bp.get("/current")
def current():
    uid = _user_id()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401

    active = get_active_treatment(uid)
    draft = get_latest_draft(uid)
    return jsonify({
        "ok": True,
        "active": treatment_to_dict(active) if active else None,
        "draft": treatment_to_dict(draft) if draft else None,
    })


@api_treatment_bp.post("/save-draft")
def save_draft():
    uid = _user_id()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401

    data = request.get_json(force=True, silent=True) or {}
    profile_id = data.pop("profile_id", None)
    profile = save_treatment(uid, data, profile_id=profile_id)
    return jsonify({"ok": True, "profile_id": profile.id, "message": "Borrador guardado"})


@api_treatment_bp.post("/activate")
def activate():
    uid = _user_id()
    if not uid:
        return jsonify({"ok": False, "error": "No autenticado"}), 401

    data = request.get_json(force=True, silent=True) or {}
    profile_id = data.get("profile_id")
    replace = bool(data.get("replace", False))

    if not profile_id:
        return jsonify({"ok": False, "error": "profile_id requerido"}), 400

    try:
        profile = activate_treatment(uid, profile_id, replace=replace)
        return jsonify({
            "ok": True,
            "profile_id": profile.id,
            "message": "Tratamiento activado",
        })
    except ValueError as e:
        if str(e) == "ACTIVE_EXISTS":
            active = get_active_treatment(uid)
            return jsonify({
                "ok": False,
                "error": "ACTIVE_EXISTS",
                "active_id": active.id if active else None,
                "message": "Ya tienes un tratamiento activo. ¿Deseas reemplazarlo?",
            }), 409
        return jsonify({"ok": False, "error": str(e)}), 404
