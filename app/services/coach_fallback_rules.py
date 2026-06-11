# -*- coding: utf-8 -*-
"""Respuestas por reglas cuando la IA externa falla o no está configurada."""
from app.services.coach_live_service import build_daily_coach_context, _now


def fallback_response(user_id: int, user_message: str, user_name: str = "") -> str:
    ctx = build_daily_coach_context(user_id, user_name=user_name)
    msg = user_message.lower().strip()
    name = user_name or "amigo"

    if any(w in msg for w in ["agua", "pausa", "descanso"]):
        return "Toma agua, respira 5 minutos y vuelve. El coach registró tu pausa."

    if any(w in msg for w in ["plan", "hoy", "acciones"]):
        if ctx["case"] == "no_plan":
            return f"{name}, aún no tienes plan para hoy. Ve a 'Crear plan con IA' o crea una actividad guiada."
        return f"{name}, {ctx['current_status']}. {ctx['recommended_action']}"

    if ctx["case"] == "active":
        lines = [f"{name}, {ctx['current_status']}."]
        last = ctx.get("last_completed_step")
        if last:
            lines.append(f"Último paso: {last.get('title', '')}.")
        current = ctx.get("current_step")
        if current:
            lines.append(f"Siguiente paso: {current.get('title', '')}.")
        lines.append("¿Quieres continuar? Usa el botón Continuar actividad.")
        return "\n".join(lines)

    if ctx["case"] == "late":
        return f"{name}, {ctx['recommended_action']}"

    if ctx["case"] in ("wind_down", "sleep"):
        return f"{name}, {ctx['recommended_action']}"

    if ctx.get("habit_reminder"):
        return f"{name}. {ctx['habit_reminder']}"

    hour = _now().hour
    if hour >= 22:
        return f"{name}, es tarde. Te sugiero cierre diario y descanso. Mañana retomamos con claridad."

    return (
        f"{name}, {ctx['current_status']}\n\n"
        f"{ctx['recommended_action']}\n\n"
        "(Modo reglas — IA externa no disponible. Configura AI_PROVIDER en .env)"
    )
