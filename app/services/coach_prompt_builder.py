# -*- coding: utf-8 -*-
"""Prompts controlados del coach — sin improvisación desde UI."""
from typing import Dict, Any, List

COACH_TONE = "Directo, ejecutivo, motivador, breve, orientado a acción. Sin tono médico. Sin inventar datos."

SYSTEM_BASE = f"""Eres EasyCoach, coach personal ejecutivo.
{COACH_TONE}

REGLAS:
- Responde en español.
- Máximo 3 recomendaciones.
- Siempre indica la siguiente acción concreta.
- Si no hay datos en el contexto, dilo explícitamente.
- No inventes roadmap, decisiones ni agenda.
- Si es de noche (day_period=night), prioriza cierre diario y descanso.
- Si hay actividad activa, prioriza continuarla.
- Si hay actividad atrasada, recomienda iniciar o reprogramar.
- Si no hay plan diario, recomienda crearlo.
"""


def _messages(system: str, context: Dict[str, Any], user_message: str = "", history: List = None) -> list:
    from app.services.coach_context_builder import context_to_text
    msgs = [{"role": "system", "content": system}]
    msgs.append({"role": "system", "content": f"CONTEXTO:\n{context_to_text(context)}"})
    for h in (history or [])[-8:]:
        msgs.append({"role": h["role"], "content": h["content"]})
    if user_message:
        msgs.append({"role": "user", "content": user_message})
    return msgs


def build_dashboard_prompt(context: Dict[str, Any], user_message: str = "", history: List = None) -> list:
    sys = SYSTEM_BASE + "\nModo: dashboard. Resume estado y di qué hacer ahora."
    if not user_message:
        user_message = "¿Qué debo hacer ahora?"
    return _messages(sys, context, user_message, history)


def build_activity_prompt(context: Dict[str, Any], user_message: str, history: List = None) -> list:
    sys = SYSTEM_BASE + "\nModo: actividad guiada. Guía paso a paso. Indica paso actual y qué se espera."
    return _messages(sys, context, user_message, history)


def build_treatment_prompt(context: Dict[str, Any], user_message: str, history: List = None) -> list:
    sys = SYSTEM_BASE + "\nModo: tratamiento. Conecta metas del tratamiento con acciones de hoy."
    return _messages(sys, context, user_message, history)


def build_daily_plan_prompt(context: Dict[str, Any]) -> list:
    sys = SYSTEM_BASE + "\nModo: plan diario. Sugiere 3-5 acciones críticas para hoy basadas en contexto real."
    return _messages(sys, context, "Genera recomendaciones de plan para hoy.", [])


def build_daily_close_prompt(context: Dict[str, Any]) -> list:
    sys = SYSTEM_BASE + "\nModo: cierre diario. Ayuda a reflexionar y definir primera acción de mañana."
    return _messages(sys, context, "Guíame en mi cierre diario.", [])


def build_habit_prompt(context: Dict[str, Any]) -> list:
    sys = SYSTEM_BASE + "\nModo: hábito. Recordatorio breve de agua, pausa o descanso."
    return _messages(sys, context, "¿Qué hábito debo atender ahora?", [])


def build_messages(user_context: str, user_message: str, history: list = None) -> list:
    """Compatibilidad legacy — user_context es texto JSON."""
    import json
    try:
        ctx = json.loads(user_context) if user_context.strip().startswith("{") else {"raw": user_context}
    except json.JSONDecodeError:
        ctx = {"raw": user_context}
    return build_dashboard_prompt(ctx, user_message, history)
