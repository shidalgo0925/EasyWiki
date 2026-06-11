# -*- coding: utf-8 -*-
"""Construye contexto estructurado del usuario para el coach IA."""
import json
from datetime import date
from typing import Optional, Dict, Any

from app.extensions import get_db
from app.models.users import User
from app.models.coach_treatment_profile import CoachTreatmentProfile
from app.models.coach_live import CoachActivity, CoachHabitReminder
from app.models.decisions import Decision
from app.models.roadmap_items import RoadmapItem
from app.models.daily_focus import DailyFocus
from app.models.daily_reflections import DailyReflection
from app.services.coach_live_service import (
    get_active_session, get_current_step, get_last_completed_step,
    build_daily_coach_context, _now,
)


def _day_period(hour: int) -> str:
    if hour < 12:
        return "morning"
    if hour < 18:
        return "afternoon"
    if hour < 22:
        return "evening"
    return "night"


def build_context(
    user_id: int,
    screen_context: str = None,
    activity_id: int = None,
    user_name: str = "",
) -> Dict[str, Any]:
    db = get_db()
    now = _now()
    user = db.query(User).filter(User.id == user_id).first()
    name = user_name or (user.nombre if user else "") or "Usuario"

    ctx: Dict[str, Any] = {
        "user": {"name": name, "id": user_id},
        "screen_context": screen_context or "dashboard",
        "active_treatment": None,
        "active_activity": None,
        "current_step": None,
        "last_completed_step": None,
        "today_activities": [],
        "overdue_activities": [],
        "today_plan": [],
        "decisions": [],
        "roadmap": [],
        "habit_reminders": [],
        "daily_close_done": False,
        "coach_now": {},
        "time_context": {
            "local_time": now.strftime("%H:%M"),
            "local_date": now.date().isoformat(),
            "day_period": _day_period(now.hour),
        },
    }

    treatment = db.query(CoachTreatmentProfile).filter(
        CoachTreatmentProfile.user_id == user_id,
        CoachTreatmentProfile.status == "active",
    ).first()
    if treatment:
        ctx["active_treatment"] = {
            "id": treatment.id,
            "primary_area": treatment.primary_area,
            "main_problem": treatment.main_problem,
            "goal_30_days": treatment.goal_30_days,
            "goal_90_days": treatment.goal_90_days,
            "commitment_level": treatment.commitment_level,
        }

    session = get_active_session(user_id)
    target = None
    if activity_id:
        target = db.query(CoachActivity).filter(
            CoachActivity.id == activity_id, CoachActivity.user_id == user_id
        ).first()
    elif session:
        target = db.query(CoachActivity).filter(CoachActivity.id == session.activity_id).first()

    if target:
        last = get_last_completed_step(target)
        current = get_current_step(target)
        ctx["active_activity"] = {
            "id": target.id,
            "title": target.title,
            "objective": target.objective,
            "status": target.status,
            "project_key": target.project_key,
        }
        if last:
            ctx["last_completed_step"] = {"title": last.title, "order": last.step_order}
        if current:
            ctx["current_step"] = {
                "id": current.id,
                "title": current.title,
                "description": current.description,
                "expected_output": current.expected_output,
                "order": current.step_order,
            }

    today = date.today()
    activities = db.query(CoachActivity).filter(
        CoachActivity.user_id == user_id,
        CoachActivity.scheduled_date == today,
        CoachActivity.status.in_(["scheduled", "draft", "active", "paused"]),
    ).all()
    for a in activities:
        item = {"id": a.id, "title": a.title, "status": a.status, "start": str(a.scheduled_start_time or "")}
        ctx["today_activities"].append(item)
        if a.scheduled_start_time and now.time() > a.scheduled_start_time and a.status in ("scheduled", "draft"):
            ctx["overdue_activities"].append(item)

    daily = db.query(DailyFocus).filter(DailyFocus.user_id == user_id, DailyFocus.fecha == today).first()
    if daily and daily.items:
        ctx["today_plan"] = [{"title": it.titulo, "status": it.estado} for it in daily.items[:8]]

    ctx["decisions"] = [
        {"title": d.title, "date": str(d.decision_date)}
        for d in db.query(Decision).filter(Decision.user_id == user_id, Decision.estado == "activa").limit(5).all()
    ]
    ctx["roadmap"] = [
        {"name": r.nombre, "status": r.estado}
        for r in db.query(RoadmapItem).filter(
            RoadmapItem.user_id == user_id,
            RoadmapItem.estado.in_(["bloqueado", "en_progreso"]),
        ).limit(5).all()
    ]
    ctx["habit_reminders"] = [
        {"type": h.habit_type, "message": h.message, "enabled": h.enabled}
        for h in db.query(CoachHabitReminder).filter(
            CoachHabitReminder.user_id == user_id, CoachHabitReminder.enabled == True
        ).all()
    ]
    ctx["daily_close_done"] = db.query(DailyReflection).filter(
        DailyReflection.user_id == user_id, DailyReflection.fecha == today
    ).first() is not None

    ctx["coach_now"] = build_daily_coach_context(user_id, user_name=name, events_today=[])
    return ctx


def context_to_text(ctx: Dict[str, Any]) -> str:
    """Serializa contexto dict a texto para el prompt."""
    return json.dumps(ctx, ensure_ascii=False, indent=2, default=str)


def build_user_context(user_id: int, activity_id: int = None, screen_context: str = "") -> str:
    """Compatibilidad con código existente."""
    return context_to_text(build_context(user_id, screen_context=screen_context, activity_id=activity_id))
