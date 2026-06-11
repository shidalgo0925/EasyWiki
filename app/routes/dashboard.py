# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from datetime import datetime, timedelta, date
import os

from app.utils.google_calendar import get_events_range
from app.routes.auth import get_credentials
from app.extensions import get_db, get_current_user_id
from app.models.daily_focus import DailyFocus, FocusItem
from app.models.daily_reflections import DailyReflection
from app.models.wins import Win
from app.models.decisions import Decision
from app.models.roadmap_items import RoadmapItem
from app.services.treatment_service import get_active_treatment
from app.services.coach_live_service import build_daily_coach_context

dashboard_bp = Blueprint("dashboard", __name__)
misc_bp = Blueprint("misc", __name__)

@dashboard_bp.route("/")
def dashboard():
    hoy_date = datetime.now().date()
    manana_date = hoy_date + timedelta(days=1)

    stats = {
        "meta_dic": 5000,
        "prospeccion_min": 30,
        "hoy": hoy_date.strftime("%Y-%m-%d"),
    }

    events_by_day = {hoy_date.isoformat(): [], manana_date.isoformat(): []}
    google_connected = get_credentials() is not None

    if google_connected:
        creds = get_credentials()
        if creds:
            try:
                events_by_day.update(get_events_range(creds, days=2))
            except Exception:
                pass
        else:
            google_connected = False

    # Fallback si no hay eventos reales
    if not any(events_by_day.values()):
        events_by_day[hoy_date.isoformat()] = [
            {"hora": "07:30 - 08:30", "actividad": "Proyecto Odoo (Import Center)", "categoria": "Easytech", "done": False},
            {"hora": "08:30 - 09:00", "actividad": "Curso Big Data (capsula diaria)", "categoria": "Personal", "done": False},
            {"hora": "09:00 - 09:30", "actividad": "Prospeccion Mariachi", "categoria": "Mariachi", "done": False},
        ]

    # Aplana y ordena
    def parse_hora_val(h: str) -> str:
        if not h:
            return "23:59"
        h_l = h.lower()
        if h_l.startswith("todo el día"):
            return "00:00"
        if len(h) >= 5 and h[2] == ":":
            return h[:5]
        return "23:59"

    events_flat = []
    for day, evs in events_by_day.items():
        for e in evs:
            events_flat.append({
                "fecha": day,
                "hora": e.get("hora", ""),
                "actividad": e.get("actividad", ""),
                "categoria": e.get("categoria", ""),
                "done": e.get("done", False),
                "_sort_hora": parse_hora_val(e.get("hora", "")),
            })

    events_flat.sort(key=lambda x: (x["fecha"], x["_sort_hora"]))
    for e in events_flat:
        e.pop("_sort_hora", None)

    stats["total_eventos"] = len(events_flat)
    stats["completados"] = sum(1 for e in events_flat if e.get("done"))

    # -------------------
    # BLOQUE DAILY FOCUS (EasyCoach MVP)
    db = get_db()
    user_id = get_current_user_id() or 1

    daily = db.query(DailyFocus).filter(
        DailyFocus.user_id == user_id,
        DailyFocus.fecha == date.today()
    ).first()

    plan_date = date.today()
    is_today = True

    if not daily:
        daily = db.query(DailyFocus).filter(
            DailyFocus.user_id == user_id,
            DailyFocus.fecha >= date.today()
        ).order_by(DailyFocus.fecha.asc()).first()
        if daily:
            plan_date = daily.fecha
            is_today = (daily.fecha == date.today())

    plan_items = daily.items if daily else []
    # -------------------

    # Estadísticas de cierre diario
    completion_pct = 0
    if plan_items:
        completed = sum(1 for it in plan_items if it.estado == "completada")
        completion_pct = round((completed / len(plan_items)) * 100)

    latest_reflection = db.query(DailyReflection).filter(
        DailyReflection.user_id == user_id
    ).order_by(DailyReflection.fecha.desc()).first()

    latest_wins = db.query(Win).filter(
        Win.user_id == user_id
    ).order_by(Win.fecha.desc()).limit(5).all()

    active_decisions = db.query(Decision).filter(
        Decision.user_id == user_id,
        Decision.estado == "activa"
    ).order_by(Decision.decision_date.desc()).limit(3).all()

    roadmap_alert = db.query(RoadmapItem).filter(
        RoadmapItem.user_id == user_id,
        RoadmapItem.estado.in_(["bloqueado", "en_progreso"])
    ).order_by(RoadmapItem.prioridad.asc()).limit(3).all()

    active_treatment = get_active_treatment(user_id)

    user_name = ""
    from flask import g
    if getattr(g, "current_user", None):
        user_name = g.current_user.nombre or g.current_user.email.split("@")[0]

    today_events = [e for e in events_flat if e.get("fecha") == hoy_date.isoformat()]
    coach_now = build_daily_coach_context(user_id, user_name=user_name, events_today=today_events)

    return render_template(
        "dashboard.html",
        events_flat=events_flat,
        stats=stats,
        google_connected=google_connected,
        plan_items_today=plan_items,
        plan_date=plan_date,
        plan_is_today=is_today,
        completion_pct=completion_pct,
        latest_reflection=latest_reflection,
        latest_wins=latest_wins,
        active_decisions=active_decisions,
        roadmap_alert=roadmap_alert,
        active_treatment=active_treatment,
        coach_now=coach_now,
    )

@misc_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@misc_bp.route("/terms")
def terms():
    return render_template("terms.html")
