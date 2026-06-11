# -*- coding: utf-8 -*-
"""Coach vivo — contexto diario, actividades guiadas, hábitos."""
from datetime import datetime, date, time, timedelta
from typing import Optional, List, Dict, Any

import os
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from app.extensions import get_db
from app.models.coach_live import (
    CoachActivity, CoachActivityStep, CoachWorkSession,
    CoachHabitReminder, CoachDailyState, CoachMessage,
)
from app.models.daily_focus import DailyFocus
from app.models.daily_reflections import DailyReflection

LOCAL_TZ = os.environ.get("LOCAL_TZ", "America/Panama")

DEFAULT_STEPS = [
    ("Aclarar objetivo", "Define con claridad qué significa completar esta actividad.", "Objetivo escrito en una frase"),
    ("Reunir información", "Recopila lo que necesitas antes de ejecutar.", "Lista de insumos o contexto listo"),
    ("Ejecutar acción principal", "Haz el trabajo central de esta actividad.", "Acción principal completada"),
    ("Validar resultado", "Confirma que el resultado cumple lo esperado.", "Validación registrada"),
    ("Registrar cierre", "Documenta el cierre y próximo paso si aplica.", "Cierre registrado"),
]

DEFAULT_HABITS = [
    ("water", "Tomar agua", "Toma agua antes de seguir.", 120),
    ("break", "Pausa activa", "Haz una pausa de 5 minutos.", 90),
    ("daily_close", "Cierre diario", "Cierra el día y deja lista la primera acción de mañana.", None),
    ("sleep", "Preparar descanso", "No abras un nuevo frente técnico. Prepara descanso.", None),
]


def _tz():
    try:
        return ZoneInfo(LOCAL_TZ)
    except Exception:
        import pytz
        return pytz.timezone(LOCAL_TZ)


def _now() -> datetime:
    return datetime.now(_tz())


def ensure_default_habits(user_id: int) -> None:
    db = get_db()
    existing = db.query(CoachHabitReminder).filter(CoachHabitReminder.user_id == user_id).count()
    if existing:
        return
    for habit_type, title, message, interval in DEFAULT_HABITS:
        preferred = None
        if habit_type == "daily_close":
            preferred = time(21, 0)
        elif habit_type == "sleep":
            preferred = time(22, 0)
        db.add(CoachHabitReminder(
            user_id=user_id,
            habit_type=habit_type,
            title=title,
            message=message,
            interval_minutes=interval,
            preferred_time=preferred,
            enabled=True,
        ))
    db.commit()


def get_or_create_daily_state(user_id: int) -> CoachDailyState:
    db = get_db()
    today = _now().date()
    state = db.query(CoachDailyState).filter(
        CoachDailyState.user_id == user_id,
        CoachDailyState.date == today,
    ).first()
    if not state:
        state = CoachDailyState(user_id=user_id, date=today)
        db.add(state)
        db.commit()
        db.refresh(state)
    return state


def get_active_session(user_id: int) -> Optional[CoachWorkSession]:
    db = get_db()
    return db.query(CoachWorkSession).filter(
        CoachWorkSession.user_id == user_id,
        CoachWorkSession.status == "active",
    ).order_by(CoachWorkSession.started_at.desc()).first()


def get_paused_session(user_id: int) -> Optional[CoachWorkSession]:
    db = get_db()
    return db.query(CoachWorkSession).filter(
        CoachWorkSession.user_id == user_id,
        CoachWorkSession.status == "paused",
    ).order_by(CoachWorkSession.paused_at.desc()).first()


def get_current_step(activity: CoachActivity) -> Optional[CoachActivityStep]:
    if not activity.steps:
        return None
    for s in activity.steps:
        if s.status in ("active", "pending"):
            return s
    return activity.steps[-1]


def get_last_completed_step(activity: CoachActivity) -> Optional[CoachActivityStep]:
    completed = [s for s in activity.steps if s.status == "completed"]
    return completed[-1] if completed else None


def _parse_event_start(hora: str) -> Optional[time]:
    if not hora or len(hora) < 5:
        return None
    try:
        parts = hora[:5].split(":")
        return time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


def _activity_dict(a: Optional[CoachActivity]) -> Optional[Dict[str, Any]]:
    if not a:
        return None
    return {
        "id": a.id,
        "title": a.title,
        "objective": a.objective,
        "status": a.status,
        "project_key": a.project_key,
        "scheduled_date": a.scheduled_date.isoformat() if a.scheduled_date else None,
        "scheduled_start_time": a.scheduled_start_time.strftime("%H:%M") if a.scheduled_start_time else None,
    }


def _step_dict(s: Optional[CoachActivityStep]) -> Optional[Dict[str, Any]]:
    if not s:
        return None
    return {
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "expected_output": s.expected_output,
        "order": s.step_order,
        "status": s.status,
    }


def _greeting(user_name: str) -> str:
    h = _now().hour
    if h < 12:
        prefix = "Buenos días"
    elif h < 18:
        prefix = "Buenas tardes"
    else:
        prefix = "Buenas noches"
    return f"{prefix}, {user_name}" if user_name else prefix


def build_daily_coach_context(
    user_id: int,
    user_name: str = "",
    events_today: Optional[List[dict]] = None,
) -> Dict[str, Any]:
    db = get_db()
    ensure_default_habits(user_id)
    state = get_or_create_daily_state(user_id)
    now = _now()
    today = now.date()
    events_today = events_today or []

    ctx = {
        "greeting": _greeting(user_name),
        "current_status": "",
        "recommended_action": "",
        "next_activity": None,
        "current_activity": None,
        "current_step": None,
        "last_completed_step": None,
        "warning": "",
        "habit_reminder": "",
        "cta_primary": None,
        "cta_secondary": None,
        "case": "default",
        "progress_label": "",
    }

    # Cierre diario hecho hoy?
    reflection_today = db.query(DailyReflection).filter(
        DailyReflection.user_id == user_id,
        DailyReflection.fecha == today,
    ).first()
    daily_close_done = reflection_today is not None
    state.daily_close_done = daily_close_done

    session = get_active_session(user_id) or get_paused_session(user_id)

    # --- Caso: actividad activa/pausada ---
    if session:
        activity = db.query(CoachActivity).filter(CoachActivity.id == session.activity_id).first()
        if activity:
            current_step = get_current_step(activity)
            last_done = get_last_completed_step(activity)
            ctx["current_activity"] = _activity_dict(activity)
            ctx["current_step"] = _step_dict(current_step)
            ctx["last_completed_step"] = _step_dict(last_done)
            ctx["case"] = "active" if session.status == "active" else "paused"
            status_word = "trabajando en" if session.status == "active" else "pausaste"
            ctx["current_status"] = f"Estás {status_word}: {activity.title}"
            if last_done:
                ctx["recommended_action"] = f"Último paso completado: {last_done.title}"
            if current_step and current_step.status != "completed":
                ctx["recommended_action"] += f"\nSiguiente paso: {current_step.title}"
                if current_step.description:
                    ctx["recommended_action"] += f" — {current_step.description}"
            ctx["progress_label"] = f"Paso {_step_num(activity, current_step)} de {len(activity.steps)}"
            ctx["cta_primary"] = {"label": "Continuar actividad", "url": f"/coach/activity/{activity.id}"}
            ctx["cta_secondary"] = {"label": "Pausar", "action": "pause", "activity_id": activity.id}
            if session.status == "paused":
                ctx["cta_primary"] = {"label": "Reanudar actividad", "url": f"/coach/activity/{activity.id}"}
            _persist_state(state, activity.id, ctx["recommended_action"])
            db.commit()
            return ctx

    # --- Hora de descanso (22:00+) ---
    if now.hour >= 22 and not daily_close_done:
        ctx["case"] = "wind_down"
        ctx["current_status"] = f"Son las {now.strftime('%I:%M %p')}."
        ctx["recommended_action"] = "Ya no recomiendo abrir tareas técnicas nuevas. Haz cierre diario, toma agua y prepara descanso."
        ctx["warning"] = "Modo descanso activo"
        ctx["habit_reminder"] = "Cierra el día y deja lista la primera acción de mañana."
        ctx["cta_primary"] = {"label": "Hacer cierre diario", "url": "/daily/close"}
        ctx["cta_secondary"] = {"label": "Tomar agua", "action": "water"}
        db.commit()
        return ctx

    if now.hour >= 22 and daily_close_done:
        ctx["case"] = "sleep"
        ctx["current_status"] = "Cierre diario completado."
        ctx["recommended_action"] = "Buen trabajo hoy. Prepara descanso — mañana retomamos con claridad."
        ctx["habit_reminder"] = "Toma agua y desconéctate del trabajo técnico."
        ctx["cta_primary"] = {"label": "Ver dashboard mañana", "url": "/"}
        db.commit()
        return ctx

    # --- Recordatorio agua (2h sin pausa) ---
    last_interaction = state.last_water_at or state.updated_at
    if last_interaction:
        if last_interaction.tzinfo is None:
            try:
                last_interaction = last_interaction.replace(tzinfo=_tz())
            except Exception:
                pass
        hours_since = (now - last_interaction).total_seconds() / 3600
        if hours_since >= 2 and now.hour < 22:
            ctx["habit_reminder"] = "Hace más de 2 horas sin pausa. Toma agua y vuelve en 5 minutos."
            ctx["cta_secondary"] = {"label": "Registré pausa", "action": "water"}

    # --- Actividad atrasada ---
    overdue = db.query(CoachActivity).filter(
        CoachActivity.user_id == user_id,
        CoachActivity.scheduled_date == today,
        CoachActivity.status.in_(["scheduled", "draft"]),
        CoachActivity.scheduled_start_time.isnot(None),
    ).all()

    for act in overdue:
        if act.scheduled_start_time and now.time() > act.scheduled_start_time:
            delay = _minutes_late(now.time(), act.scheduled_start_time)
            if delay >= 15:
                ctx["case"] = "late"
                ctx["current_activity"] = _activity_dict(act)
                ctx["current_status"] = f"Tenías programado: {act.title}"
                ctx["recommended_action"] = (
                    f"Programado a las {act.scheduled_start_time.strftime('%H:%M')}. "
                    f"Vas {delay} minutos tarde. Te recomiendo iniciar ahora o reprogramar."
                )
                ctx["warning"] = f"{delay} min de retraso"
                ctx["cta_primary"] = {"label": "Iniciar actividad", "action": "start", "activity_id": act.id}
                ctx["cta_secondary"] = {"label": "Ver actividad", "url": f"/coach/activity/{act.id}"}
                db.commit()
                return ctx

    # --- Agenda: evento actual ---
    for ev in events_today:
        if ev.get("fecha") != today.isoformat():
            continue
        start = _parse_event_start(ev.get("hora", ""))
        if not start:
            continue
        end_str = ev.get("hora", "")
        if " - " in end_str:
            end = _parse_event_start(end_str.split(" - ")[1])
        else:
            end = None
        if end and start <= now.time() <= end:
            ctx["case"] = "agenda"
            ctx["current_status"] = f"Ahora deberías estar en: {ev.get('actividad', 'Evento')}"
            ctx["recommended_action"] = f"Bloque de agenda ({ev.get('hora', '')}). Enfócate en esto o ajusta tu plan."
            ctx["cta_primary"] = {"label": "Crear actividad guiada", "url": "/wizard/activity"}
            db.commit()
            return ctx

    # --- Sin plan diario ---
    daily = db.query(DailyFocus).filter(
        DailyFocus.user_id == user_id,
        DailyFocus.fecha == today,
    ).first()
    if not daily or not daily.items:
        ctx["case"] = "no_plan"
        ctx["current_status"] = "Aún no tienes plan para hoy."
        ctx["recommended_action"] = "Te recomiendo generar tus acciones críticas antes de comenzar."
        ctx["cta_primary"] = {"label": "Crear plan con IA", "url": "/wizard/ai-plan"}
        ctx["cta_secondary"] = {"label": "Nueva actividad guiada", "url": "/wizard/activity"}
        db.commit()
        return ctx

    # --- Próxima actividad programada ---
    next_act = db.query(CoachActivity).filter(
        CoachActivity.user_id == user_id,
        CoachActivity.scheduled_date == today,
        CoachActivity.status.in_(["scheduled", "draft"]),
    ).order_by(CoachActivity.scheduled_start_time.asc().nullslast()).first()

    if next_act:
        ctx["case"] = "scheduled"
        ctx["next_activity"] = _activity_dict(next_act)
        ctx["current_status"] = f"Próxima actividad: {next_act.title}"
        when = next_act.scheduled_start_time.strftime("%H:%M") if next_act.scheduled_start_time else "hoy"
        ctx["recommended_action"] = f"Programada para las {when}. ¿Listo para iniciar?"
        ctx["cta_primary"] = {"label": "Iniciar actividad", "action": "start", "activity_id": next_act.id}
        ctx["cta_secondary"] = {"label": "Ver detalle", "url": f"/coach/activity/{next_act.id}"}
        db.commit()
        return ctx

    # --- Default: crear actividad ---
    ctx["case"] = "ready"
    ctx["current_status"] = "Tienes plan para hoy. ¿En qué quieres enfocarte ahora?"
    ctx["recommended_action"] = "Elige una actividad o crea una nueva con pasos guiados."
    ctx["cta_primary"] = {"label": "Nueva actividad guiada", "url": "/wizard/activity"}
    ctx["cta_secondary"] = {"label": "Ver plan de hoy", "url": "/"}
    db.commit()
    return ctx


def _step_num(activity: CoachActivity, step: Optional[CoachActivityStep]) -> int:
    if not step:
        return 0
    for i, s in enumerate(activity.steps, 1):
        if s.id == step.id:
            return i
    return 0


def _minutes_late(now_t: time, scheduled_t: time) -> int:
    now_m = now_t.hour * 60 + now_t.minute
    sch_m = scheduled_t.hour * 60 + scheduled_t.minute
    return max(0, now_m - sch_m)


def _persist_state(state: CoachDailyState, activity_id: int, recommendation: str) -> None:
    state.active_activity_id = activity_id
    state.next_recommendation = (recommendation or "")[:500]


def create_activity_with_steps(user_id: int, data: dict, start_now: bool = False) -> CoachActivity:
    db = get_db()
    activity = CoachActivity(
        user_id=user_id,
        title=data["title"],
        objective=data.get("objective"),
        project_key=data.get("project_key"),
        priority=int(data.get("priority", 2)),
        scheduled_date=data.get("scheduled_date"),
        scheduled_start_time=data.get("scheduled_start_time"),
        estimated_minutes=int(data.get("estimated_minutes", 30)),
        status="scheduled" if data.get("scheduled_date") else "draft",
        last_interaction_at=_now(),
    )
    db.add(activity)
    db.flush()

    steps_data = data.get("steps") or DEFAULT_STEPS
    for i, item in enumerate(steps_data, 1):
        if isinstance(item, dict):
            title, desc, expected = item.get("title", ""), item.get("description", ""), item.get("expected_output", "")
        else:
            title, desc, expected = item[0], item[1], item[2]
        step = CoachActivityStep(
            activity_id=activity.id,
            step_order=i,
            title=title,
            description=desc,
            expected_output=expected,
            status="pending",
        )
        db.add(step)
    db.flush()

    if activity.steps:
        activity.steps[0].status = "active"
        activity.current_step_id = activity.steps[0].id

    if start_now:
        start_activity(user_id, activity.id)

    db.commit()
    db.refresh(activity)
    return activity


def start_activity(user_id: int, activity_id: int) -> CoachWorkSession:
    db = get_db()
    activity = db.query(CoachActivity).filter(
        CoachActivity.id == activity_id,
        CoachActivity.user_id == user_id,
    ).first()
    if not activity:
        raise ValueError("Actividad no encontrada")

    # Pausar otras sesiones activas
    for s in db.query(CoachWorkSession).filter(
        CoachWorkSession.user_id == user_id,
        CoachWorkSession.status == "active",
    ).all():
        s.status = "paused"
        s.paused_at = _now()

    current_step = get_current_step(activity)
    if current_step and current_step.status == "pending":
        current_step.status = "active"

    session = CoachWorkSession(
        user_id=user_id,
        activity_id=activity_id,
        status="active",
        current_step_id=current_step.id if current_step else None,
    )
    activity.status = "active"
    activity.last_interaction_at = _now()
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def pause_activity(user_id: int, activity_id: int) -> None:
    db = get_db()
    session = db.query(CoachWorkSession).filter(
        CoachWorkSession.user_id == user_id,
        CoachWorkSession.activity_id == activity_id,
        CoachWorkSession.status == "active",
    ).first()
    if session:
        session.status = "paused"
        session.paused_at = _now()
    activity = db.query(CoachActivity).filter(CoachActivity.id == activity_id).first()
    if activity:
        activity.status = "paused"
        activity.last_interaction_at = _now()
    db.commit()


def complete_step(user_id: int, activity_id: int, step_id: int, user_response: str = "") -> CoachActivityStep:
    db = get_db()
    step = db.query(CoachActivityStep).join(CoachActivity).filter(
        CoachActivityStep.id == step_id,
        CoachActivity.id == activity_id,
        CoachActivity.user_id == user_id,
    ).first()
    if not step:
        raise ValueError("Paso no encontrado")

    step.status = "completed"
    step.completed_at = _now()
    if user_response:
        step.user_response = user_response

    activity = step.activity
    activity.last_interaction_at = _now()

    next_step = db.query(CoachActivityStep).filter(
        CoachActivityStep.activity_id == activity_id,
        CoachActivityStep.step_order > step.step_order,
        CoachActivityStep.status == "pending",
    ).order_by(CoachActivityStep.step_order).first()

    if next_step:
        next_step.status = "active"
        activity.current_step_id = next_step.id
    else:
        activity.current_step_id = None

    db.commit()
    db.refresh(step)
    return step


def complete_activity(user_id: int, activity_id: int) -> CoachActivity:
    db = get_db()
    activity = db.query(CoachActivity).filter(
        CoachActivity.id == activity_id,
        CoachActivity.user_id == user_id,
    ).first()
    if not activity:
        raise ValueError("Actividad no encontrada")

    activity.status = "completed"
    activity.last_interaction_at = _now()

    for s in db.query(CoachWorkSession).filter(
        CoachWorkSession.activity_id == activity_id,
        CoachWorkSession.user_id == user_id,
        CoachWorkSession.status.in_(["active", "paused"]),
    ).all():
        s.status = "completed"
        s.completed_at = _now()

    db.commit()
    db.refresh(activity)
    return activity


def mark_water(user_id: int) -> None:
    state = get_or_create_daily_state(user_id)
    state.last_water_at = _now()
    db = get_db()
    db.commit()
