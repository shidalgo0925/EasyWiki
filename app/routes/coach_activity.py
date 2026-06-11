# -*- coding: utf-8 -*-
from datetime import datetime, date as date_cls
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session

from app.services.coach_live_service import (
    create_activity_with_steps,
    start_activity,
    pause_activity,
    complete_step,
    complete_activity,
    mark_water,
    build_daily_coach_context,
)
from app.models.coach_live import CoachActivity

coach_bp = Blueprint("coach", __name__, url_prefix="/coach")
activity_wizard_bp = Blueprint("activity_wizard", __name__, url_prefix="/wizard")


def _uid():
    return session.get("user_id")


def _require_login():
    if not _uid():
        return redirect(url_for("auth.login"))
    return None


@coach_bp.get("/activity/<int:activity_id>")
def activity_view(activity_id):
    redir = _require_login()
    if redir:
        return redir
    from app.extensions import get_db
    db = get_db()
    activity = db.query(CoachActivity).filter(
        CoachActivity.id == activity_id,
        CoachActivity.user_id == _uid(),
    ).first()
    if not activity:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("coach/activity.html", activity=activity)


@coach_bp.post("/activity/<int:activity_id>/start")
def activity_start(activity_id):
    redir = _require_login()
    if redir:
        return redir
    start_activity(_uid(), activity_id)
    if request.headers.get("Accept") == "application/json" or request.is_json:
        return jsonify({"ok": True})
    return redirect(url_for("coach.activity_view", activity_id=activity_id))


@coach_bp.post("/activity/<int:activity_id>/pause")
def activity_pause(activity_id):
    redir = _require_login()
    if redir:
        return redir
    pause_activity(_uid(), activity_id)
    if request.headers.get("Accept") == "application/json" or request.is_json:
        return jsonify({"ok": True})
    return redirect(url_for("dashboard.dashboard"))


@coach_bp.post("/activity/<int:activity_id>/step/<int:step_id>/complete")
def activity_complete_step(activity_id, step_id):
    redir = _require_login()
    if redir:
        return redir
    user_response = request.form.get("user_response", "") or (request.get_json(silent=True) or {}).get("user_response", "")
    complete_step(_uid(), activity_id, step_id, user_response)
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"ok": True})
    return redirect(url_for("coach.activity_view", activity_id=activity_id))


@coach_bp.post("/activity/<int:activity_id>/complete")
def activity_complete(activity_id):
    redir = _require_login()
    if redir:
        return redir
    complete_activity(_uid(), activity_id)
    if request.is_json:
        return jsonify({"ok": True})
    return redirect(url_for("dashboard.dashboard"))


@coach_bp.post("/activity/<int:activity_id>/blocked")
def activity_blocked(activity_id):
    redir = _require_login()
    if redir:
        return redir
    from app.extensions import get_db
    db = get_db()
    activity = db.query(CoachActivity).filter(
        CoachActivity.id == activity_id, CoachActivity.user_id == _uid()
    ).first()
    if activity:
        activity.status = "blocked"
        db.commit()
    if request.is_json:
        return jsonify({"ok": True})
    return redirect(url_for("coach.activity_view", activity_id=activity_id))


@coach_bp.post("/water")
def register_water():
    if not _uid():
        return jsonify({"ok": False}), 401
    mark_water(_uid())
    return jsonify({"ok": True, "message": "Pausa registrada"})


@activity_wizard_bp.get("/activity")
def activity_wizard():
    redir = _require_login()
    if redir:
        return redir
    return render_template("wizard_activity.html")


@activity_wizard_bp.post("/activity")
def activity_wizard_create():
    redir = _require_login()
    if redir:
        return redir

    data = request.form
    scheduled_date = None
    scheduled_time = None
    if data.get("scheduled_date"):
        scheduled_date = datetime.strptime(data["scheduled_date"], "%Y-%m-%d").date()
    if data.get("scheduled_time"):
        scheduled_time = datetime.strptime(data["scheduled_time"], "%H:%M").time()

    payload = {
        "title": data.get("title", "").strip(),
        "objective": data.get("objective", "").strip(),
        "project_key": data.get("project_key", "").strip(),
        "priority": data.get("priority", 2),
        "scheduled_date": scheduled_date or date_cls.today(),
        "scheduled_start_time": scheduled_time,
        "estimated_minutes": data.get("estimated_minutes", 30),
    }
    start_now = data.get("start_now") == "1"
    activity = create_activity_with_steps(_uid(), payload, start_now=start_now)
    return redirect(url_for("coach.activity_view", activity_id=activity.id))
