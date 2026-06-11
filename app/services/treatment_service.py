# -*- coding: utf-8 -*-
import json
from typing import Any, Optional

from app.extensions import get_db
from app.models.coach_treatment_profile import CoachTreatmentProfile
from app.models.decisions import Decision
from app.models.roadmap_items import RoadmapItem
from app.models.daily_reflections import DailyReflection


def _loads(text: Optional[str], default: Any) -> Any:
    if not text:
        return default
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def treatment_to_dict(profile: CoachTreatmentProfile) -> dict:
    return {
        "id": profile.id,
        "current_situation": profile.current_situation or "",
        "main_problem": profile.main_problem or "",
        "primary_area": profile.primary_area or "",
        "goal_30_days": profile.goal_30_days or "",
        "goal_90_days": profile.goal_90_days or "",
        "success_definition": profile.success_definition or "",
        "obstacles": _loads(profile.obstacles, []),
        "current_routine": _loads(profile.current_routine, {}),
        "commitment_level": profile.commitment_level or "",
        "coaching_preferences": _loads(profile.coaching_preferences, {}),
        "status": profile.status,
        "wizard_step": profile.wizard_step,
    }


def get_active_treatment(user_id: int) -> Optional[CoachTreatmentProfile]:
    db = get_db()
    return db.query(CoachTreatmentProfile).filter(
        CoachTreatmentProfile.user_id == user_id,
        CoachTreatmentProfile.status == "active",
    ).first()


def get_latest_draft(user_id: int) -> Optional[CoachTreatmentProfile]:
    db = get_db()
    return db.query(CoachTreatmentProfile).filter(
        CoachTreatmentProfile.user_id == user_id,
        CoachTreatmentProfile.status == "draft",
    ).order_by(CoachTreatmentProfile.updated_at.desc()).first()


def build_prefill(user_id: int) -> dict:
    db = get_db()
    hints = {
        "decisions": [],
        "roadmap_blocked": [],
        "last_blocker": "",
        "suggested_area": "Económico",
    }

    decisions = db.query(Decision).filter(
        Decision.user_id == user_id,
        Decision.estado == "activa",
    ).order_by(Decision.decision_date.desc()).limit(3).all()
    hints["decisions"] = [d.title for d in decisions]

    blocked = db.query(RoadmapItem).filter(
        RoadmapItem.user_id == user_id,
        RoadmapItem.estado.in_(["bloqueado", "en_progreso"]),
    ).limit(3).all()
    hints["roadmap_blocked"] = [f"{r.nombre} ({r.estado})" for r in blocked]

    reflection = db.query(DailyReflection).filter(
        DailyReflection.user_id == user_id,
    ).order_by(DailyReflection.fecha.desc()).first()
    if reflection and reflection.que_bloqueo:
        hints["last_blocker"] = reflection.que_bloqueo

    return hints


def save_treatment(user_id: int, data: dict, profile_id: Optional[int] = None) -> CoachTreatmentProfile:
    db = get_db()
    profile = None

    if profile_id:
        profile = db.query(CoachTreatmentProfile).filter(
            CoachTreatmentProfile.id == profile_id,
            CoachTreatmentProfile.user_id == user_id,
            CoachTreatmentProfile.status == "draft",
        ).first()

    if not profile:
        profile = get_latest_draft(user_id) or CoachTreatmentProfile(user_id=user_id, status="draft")

    profile.current_situation = data.get("current_situation", profile.current_situation)
    profile.main_problem = data.get("main_problem", profile.main_problem)
    profile.primary_area = data.get("primary_area", profile.primary_area)
    profile.goal_30_days = data.get("goal_30_days", profile.goal_30_days)
    profile.goal_90_days = data.get("goal_90_days", profile.goal_90_days)
    profile.success_definition = data.get("success_definition", profile.success_definition)
    if "obstacles" in data:
        profile.obstacles = json.dumps(data["obstacles"], ensure_ascii=False)
    if "current_routine" in data:
        profile.current_routine = json.dumps(data["current_routine"], ensure_ascii=False)
    profile.commitment_level = data.get("commitment_level", profile.commitment_level)
    if "coaching_preferences" in data:
        profile.coaching_preferences = json.dumps(data["coaching_preferences"], ensure_ascii=False)
    profile.wizard_step = data.get("wizard_step", profile.wizard_step or 1)
    profile.status = "draft"

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def activate_treatment(user_id: int, profile_id: int, replace: bool = False) -> CoachTreatmentProfile:
    db = get_db()
    profile = db.query(CoachTreatmentProfile).filter(
        CoachTreatmentProfile.id == profile_id,
        CoachTreatmentProfile.user_id == user_id,
    ).first()
    if not profile:
        raise ValueError("Tratamiento no encontrado")

    active = get_active_treatment(user_id)
    if active and active.id != profile.id:
        if not replace:
            raise ValueError("ACTIVE_EXISTS")
        active.status = "archived"
        db.add(active)

    profile.status = "active"
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
