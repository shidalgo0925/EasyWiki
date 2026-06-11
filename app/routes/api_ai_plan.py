# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from datetime import date
from ..services.ai_planner import AIPlanner
from ..extensions import get_db, get_current_user_id
from ..models.plan_day import PlanDay, PlanItem
from ..models.daily_focus import DailyFocus, FocusItem
from app.utils.google_calendar import sync_focus_items_to_calendar
from app.routes.auth import get_credentials

api_ai_bp = Blueprint("api_ai", __name__, url_prefix="/api/ai/plan")
planner = AIPlanner()

@api_ai_bp.post("/suggest")
def suggest():
    data = request.get_json(force=True, silent=True) or {}
    goals_raw = data.get("metas_crudas", "")
    horizonte = data.get("horizonte", "90d")
    restricciones = data.get("restricciones", {})
    agenda = data.get("agenda", [])
    user_id = get_current_user_id() or int(data.get("user_id", 1))
    draft = planner.suggest(goals_raw, horizonte, restricciones, agenda, user_id)
    return jsonify({"ok": True, "draft": draft})

@api_ai_bp.post("/refine")
def refine():
    data = request.get_json(force=True, silent=True) or {}
    draft = data.get("draft", {})
    feedback = data.get("feedback", "")
    refined = planner.refine(draft, feedback)
    return jsonify({"ok": True, "draft": refined})

@api_ai_bp.post("/move_to_today")
def move_to_today():
    data = request.get_json(force=True, silent=True) or {}
    user_id = get_current_user_id() or int(data.get("user_id", 1))
    from_fecha = data.get("from_fecha")
    if not from_fecha:
        return jsonify({"ok": False, "error": "from_fecha requerido"}), 400

    db = get_db()
    try:
        src = db.query(PlanDay).filter(
            PlanDay.user_id == user_id,
            PlanDay.fecha == date.fromisoformat(from_fecha)
        ).first()
        if not src:
            return jsonify({"ok": False, "error": "Plan origen no existe"}), 404

        # upsert de hoy
        today = date.today()
        dst = db.query(PlanDay).filter(
            PlanDay.user_id == user_id,
            PlanDay.fecha == today
        ).first()
        if not dst:
            dst = PlanDay(user_id=user_id, fecha=today)
            db.add(dst)
            db.flush()

        # limpiar y copiar items
        db.query(PlanItem).filter(PlanItem.plan_id == dst.id).delete()
        for it in src.items:
            db.add(PlanItem(
                plan_id=dst.id,
                titulo=it.titulo,
                categoria=it.categoria,
                prioridad=it.prioridad,
                dur_min=it.dur_min,
                from_calendar=it.from_calendar,
            ))
        db.commit()
        return jsonify({"ok": True, "moved_from": from_fecha, "to": today.isoformat()})
    except Exception as e:
        db.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500


@api_ai_bp.post("/sync_calendar")
def sync_calendar():
    """
    Sincroniza los FocusItem del día con Google Calendar.
    Crea eventos para items que tengan hora_inicio y no tengan google_event_id.
    """
    user_id = get_current_user_id()
    if not user_id:
        user_id = int(request.get_json(force=True, silent=True).get("user_id", 0))
    if not user_id:
        return jsonify({"ok": False, "error": "Usuario no autenticado"}), 401

    creds = get_credentials()
    if not creds:
        return jsonify({"ok": False, "error": "Google Calendar no conectado"}), 400

    db = get_db()
    today = date.today()

    daily = db.query(DailyFocus).filter(
        DailyFocus.user_id == user_id,
        DailyFocus.fecha == today
    ).first()

    if not daily:
        return jsonify({"ok": False, "error": "No hay foco diario para hoy"}), 404

    items_to_sync = [it for it in daily.items if it.hora_inicio and not it.google_event_id]
    if not items_to_sync:
        return jsonify({"ok": True, "message": "No hay items para sincronizar", "created": 0})

    try:
        created = sync_focus_items_to_calendar(creds, items_to_sync, today)
        db.commit()
        return jsonify({
            "ok": True,
            "message": f"{len(created)} eventos creados en Google Calendar",
            "created": len(created),
        })
    except Exception as e:
        db.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500


@api_ai_bp.post("/commit")
def commit():
    """
    Guarda el borrador generado por la IA en DailyFocus + FocusItem.
    Se espera: { draft: {...}, user_id: int? }
    """
    data = request.get_json(force=True, silent=True) or {}
    draft = data.get("draft", {})
    if not draft:
        return jsonify({"ok": False, "error": "draft requerido"}), 400

    # Autenticación: sesión primero, body como fallback
    user_id = get_current_user_id()
    if not user_id:
        user_id = int(data.get("user_id", 0))
    if not user_id:
        return jsonify({"ok": False, "error": "Usuario no autenticado"}), 401

    microacciones = draft.get("microacciones", {})
    if not microacciones:
        return jsonify({"ok": False, "error": "No hay microacciones para guardar"}), 400

    db = get_db()
    created_count = 0

    try:
        for fecha_str, items in microacciones.items():
            if not items:
                continue

            daily = db.query(DailyFocus).filter(
                DailyFocus.user_id == user_id,
                DailyFocus.fecha == date.fromisoformat(fecha_str)
            ).first()

            if not daily:
                daily = DailyFocus(user_id=user_id, fecha=date.fromisoformat(fecha_str))
                db.add(daily)
                db.flush()

            for it in items:
                db.add(FocusItem(
                    daily_focus_id=daily.id,
                    titulo=it.get("titulo", "(Sin título)"),
                    categoria=it.get("categoria"),
                    prioridad=it.get("prioridad"),
                    duracion_min=it.get("dur_min"),
                    estado="pendiente",
                    from_calendar=False,
                ))
                created_count += 1

        db.commit()
        return jsonify({
            "ok": True,
            "message": "Plan guardado en DailyFocus",
            "days": len(microacciones),
            "items": created_count,
        })
    except Exception as e:
        db.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500
