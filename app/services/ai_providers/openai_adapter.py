# -*- coding: utf-8 -*-
import os
import json
from datetime import date, timedelta
from typing import List, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

import config as app_config


class OpenAIAdapter:
    """
    Adaptador OpenAI que lee el contexto completo de EasyCoach
    (visiones, áreas, proyectos, objetivos, historial diario)
    y genera un plan diario accionable.
    """

    SYSTEM_PROMPT = """\
Eres EasyCoach, un coach personal estratégico.
Tu trabajo es analizar el contexto del usuario y generar un plan diario accionable.

REGLAS:
1. Lee las visiones, áreas, proyectos y objetivos del usuario.
2. Considera su historial de microacciones, reflexiones y logros recientes.
3. Genera 3-6 microacciones concretas para MAÑANA.
4. Cada microacción debe tener: titulo, categoria, prioridad (1=alta, 2=media, 3=baja), duracion_min.
5. Responde ÚNICAMENTE en JSON válido con esta estructura:
{
  "metas_smart": [{"area": "...", "titulo": "...", "kpi": "...", "fecha_objetivo": "YYYY-MM-DD"}],
  "rocas_semanales": [{"semana": 1, "titulo": "..."}],
  "microacciones": {
    "YYYY-MM-DD": [
      {"titulo": "...", "categoria": "...", "prioridad": 1, "duracion_min": 30}
    ]
  }
}
"""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or app_config.OPENAI_API_KEY
        self.model = model or app_config.AI_MODEL
        self.client = OpenAI(api_key=self.api_key) if OpenAI and self.api_key else None

    def _call(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        if not self.client:
            raise RuntimeError("OpenAI no configurado. Revisa OPENAI_API_KEY.")
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000,
        )
        return resp.choices[0].message.content

    def _build_context(self, user_id: int) -> str:
        """
        Construye el contexto del usuario consultando la base de datos.
        """
        from app.extensions import get_db
        from app.models.visions import Vision
        from app.models.areas import Area
        from app.models.projects import Project
        from app.models.objectives import Objective
        from app.models.daily_focus import DailyFocus, FocusItem
        from app.models.daily_reflections import DailyReflection
        from app.models.wins import Win
        from app.models.decisions import Decision
        from app.models.roadmap_items import RoadmapItem

        db = get_db()

        ctx = []

        # Visión
        visions = db.query(Vision).filter(Vision.user_id == user_id, Vision.is_active == True).all()
        if visions:
            ctx.append("=== VISIÓN ===")
            for v in visions:
                ctx.append(f"- {v.titulo} ({v.horizonte}): {v.descripcion or ''}")

        # Áreas
        areas = db.query(Area).filter(Area.user_id == user_id, Area.is_active == True).order_by(Area.orden).all()
        if areas:
            ctx.append("\n=== ÁREAS ===")
            for a in areas:
                ctx.append(f"- {a.nombre} ({a.color})")

        # Proyectos
        projects = db.query(Project).filter(Project.user_id == user_id, Project.is_active == True).all()
        if projects:
            ctx.append("\n=== PROYECTOS ===")
            for p in projects:
                area_name = p.area.nombre if p.area else "Sin área"
                ctx.append(f"- {p.nombre} [{area_name}]")

        # Objetivos activos
        objectives = db.query(Objective).filter(
            Objective.user_id == user_id,
            Objective.is_active == True,
            Objective.estado == "activo"
        ).order_by(Objective.prioridad).all()
        if objectives:
            ctx.append("\n=== OBJETIVOS ACTIVOS ===")
            for o in objectives:
                ctx.append(f"- {o.titulo} (prioridad {o.prioridad}, {o.progreso_pct}%, vence {o.fecha_objetivo})")

        # Decisiones activas
        decisions = db.query(Decision).filter(
            Decision.user_id == user_id,
            Decision.estado == "activa"
        ).limit(5).all()
        if decisions:
            ctx.append("\n=== DECISIONES ACTIVAS ===")
            for d in decisions:
                ctx.append(f"- {d.title}")

        # Roadmap alertas
        roadmap = db.query(RoadmapItem).filter(
            RoadmapItem.user_id == user_id,
            RoadmapItem.estado.in_(["bloqueado", "en_progreso"])
        ).limit(5).all()
        if roadmap:
            ctx.append("\n=== ROADMAP ALERTA ===")
            for r in roadmap:
                ctx.append(f"- {r.nombre}: {r.estado}")

        # Últimos logros
        wins = db.query(Win).filter(Win.user_id == user_id).order_by(Win.fecha.desc()).limit(5).all()
        if wins:
            ctx.append("\n=== ÚLTIMOS LOGROS ===")
            for w in wins:
                ctx.append(f"- {w.titulo} ({w.impacto})")

        # Última reflexión
        last_reflection = db.query(DailyReflection).filter(
            DailyReflection.user_id == user_id
        ).order_by(DailyReflection.fecha.desc()).first()
        if last_reflection:
            ctx.append("\n=== ÚLTIMA REFLEXIÓN ===")
            if last_reflection.que_funciono:
                ctx.append(f"Funcionó: {last_reflection.que_funciono}")
            if last_reflection.que_bloqueo:
                ctx.append(f"Bloqueó: {last_reflection.que_bloqueo}")

        # Últimas microacciones
        last_daily = db.query(DailyFocus).filter(
            DailyFocus.user_id == user_id
        ).order_by(DailyFocus.fecha.desc()).first()
        if last_daily and last_daily.items:
            ctx.append("\n=== ÚLTIMAS MICROACCIONES ===")
            for it in last_daily.items:
                ctx.append(f"- {it.titulo} ({it.estado})")

        # Tratamiento activo
        from app.models.coach_treatment_profile import CoachTreatmentProfile
        import json as _json
        treatment = db.query(CoachTreatmentProfile).filter(
            CoachTreatmentProfile.user_id == user_id,
            CoachTreatmentProfile.status == "active",
        ).first()
        if treatment:
            ctx.append("\n=== TRATAMIENTO ACTIVO ===")
            if treatment.current_situation:
                ctx.append(f"Situación: {treatment.current_situation}")
            if treatment.main_problem:
                ctx.append(f"Problema principal: {treatment.main_problem}")
            if treatment.primary_area:
                ctx.append(f"Área prioritaria: {treatment.primary_area}")
            if treatment.goal_30_days:
                ctx.append(f"Meta 30 días: {treatment.goal_30_days}")
            if treatment.goal_90_days:
                ctx.append(f"Meta 90 días: {treatment.goal_90_days}")
            if treatment.success_definition:
                ctx.append(f"Definición de éxito: {treatment.success_definition}")
            if treatment.obstacles:
                try:
                    obs = _json.loads(treatment.obstacles)
                    ctx.append(f"Obstáculos: {', '.join(obs)}")
                except Exception:
                    ctx.append(f"Obstáculos: {treatment.obstacles}")
            if treatment.commitment_level:
                ctx.append(f"Compromiso: {treatment.commitment_level}")

        return "\n".join(ctx) if ctx else "Usuario nuevo sin contexto previo."

    def suggest(self, goals_raw: str, user_id: int) -> Dict[str, Any]:
        context = self._build_context(user_id)
        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        user_msg = f"""\
CONTEXTO DEL USUARIO:
{context}

META DEL USUARIO:
{goals_raw}

Genera un plan para mañana ({tomorrow}).
"""

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]

        try:
            content = self._call(messages)
            # Extraer JSON de la respuesta
            content = content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception:
            # Fallback: retorna estructura mínima
            return {
                "metas_smart": [],
                "rocas_semanales": [],
                "microacciones": {
                    tomorrow: [
                        {"titulo": "Revisar objetivos principales", "categoria": "Personal", "prioridad": 1, "duracion_min": 30},
                        {"titulo": "Bloque de trabajo enfocado", "categoria": "Easytech", "prioridad": 2, "duracion_min": 60},
                    ]
                }
            }

    def normalize_goals(self, goals_raw: str):
        return self.suggest(goals_raw, 1).get("metas_smart", [])

    def breakdown_weekly(self, metas_smart: list):
        return self.suggest("", 1).get("rocas_semanales", [])

    def microactions_daily(self, metas_smart: list, agenda: list, tz: str):
        return self.suggest("", 1).get("microacciones", {})

    def refine_draft(self, draft: dict, feedback: str) -> dict:
        messages = [
            {"role": "system", "content": "Refina el borrador de plan según el feedback del usuario. Responde en JSON con la misma estructura."},
            {"role": "user", "content": f"BORRADOR:\n{json.dumps(draft, ensure_ascii=False)}\n\nFEEDBACK:\n{feedback}"},
        ]
        try:
            content = self._call(messages, temperature=0.5)
            content = content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception:
            draft["nota_refinado"] = feedback[:200]
            return draft