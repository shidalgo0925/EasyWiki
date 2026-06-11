# -*- coding: utf-8 -*-
"""Orquestador principal — toda IA pasa por aquí."""
from typing import Optional

from app.extensions import get_db
from app.services.coach_context_builder import build_context
from app.services.coach_prompt_builder import (
    build_dashboard_prompt, build_activity_prompt, build_daily_plan_prompt,
)
from app.services.coach_fallback_rules import fallback_response
from app.services.ai_provider_router import build_router_for_user, log_ai_call
from app.services.coach_memory_service import get_or_create_conversation, save_message, get_history
from app.services.ai_model_catalog import MODEL_CATALOG
from app.models.coach_treatment_profile import CoachTreatmentProfile


class CoachAssistantService:

    def send_message(
        self,
        user_id: int,
        message: str,
        source: str = "floating_chat",
        activity_id: Optional[int] = None,
        screen_context: Optional[str] = None,
        conversation_id: Optional[int] = None,
        user_name: str = "",
        provider: str = None,
        model: str = None,
    ) -> dict:
        message = (message or "").strip()
        if not message:
            return {"ok": False, "error": "Mensaje vacío"}

        screen = screen_context or source
        treatment_id = None
        db = get_db()
        t = db.query(CoachTreatmentProfile).filter(
            CoachTreatmentProfile.user_id == user_id,
            CoachTreatmentProfile.status == "active",
        ).first()
        if t:
            treatment_id = t.id

        conv = get_or_create_conversation(
            user_id, source=source, activity_id=activity_id,
            treatment_id=treatment_id, conversation_id=conversation_id, title=message[:80],
        )
        history = get_history(conv.id)
        save_message(conv.id, "user", message, user_id=user_id)

        ctx = build_context(user_id, screen_context=screen, activity_id=activity_id, user_name=user_name)

        if activity_id:
            prompt_msgs = build_activity_prompt(ctx, message, history)
        else:
            prompt_msgs = build_dashboard_prompt(ctx, message, history)

        used_fallback = False
        provider_used = "rules"
        model_used = "fallback"
        latency_ms = 0
        reply = ""

        try:
            router = build_router_for_user(user_id, provider=provider, model=model)
            ai_resp = router.generate(prompt_msgs)
            log_ai_call(user_id, ai_resp, source=source)
            if ai_resp.ok:
                reply = ai_resp.content
                provider_used = ai_resp.provider
                model_used = ai_resp.model
                latency_ms = ai_resp.latency_ms
                used_fallback = ai_resp.used_fallback
            else:
                raise RuntimeError(ai_resp.error or "empty")
        except Exception:
            reply = fallback_response(user_id, message, user_name=user_name)
            used_fallback = True
            if "recomendaciones básicas" not in reply:
                reply += "\n\n(El coach está usando recomendaciones básicas por ahora.)"

        save_message(
            conv.id, "assistant", reply, user_id=user_id,
            provider=provider_used, model=model_used, latency_ms=latency_ms,
            error_code="fallback" if used_fallback else None,
        )
        conv.provider_used = provider_used
        conv.model_used = model_used
        db.commit()

        return {
            "ok": True,
            "message": reply,
            "reply": reply,
            "conversation_id": conv.id,
            "provider": provider_used,
            "model": model_used,
            "fallback": used_fallback,
            "used_fallback": used_fallback,
            "latency_ms": latency_ms,
        }

    def chat(self, **kwargs) -> dict:
        if "screen_context" in kwargs and "source" not in kwargs:
            kwargs["source"] = kwargs.get("screen_context") or "floating_chat"
        return self.send_message(**kwargs)

    def get_context(self, user_id: int, screen_context: str = "dashboard", activity_id: int = None, user_name: str = "") -> dict:
        return build_context(user_id, screen_context=screen_context, activity_id=activity_id, user_name=user_name)

    def daily_recommendation(self, user_id: int, user_name: str = "") -> dict:
        ctx = build_context(user_id, user_name=user_name)
        try:
            router = build_router_for_user(user_id)
            ai_resp = router.generate(build_daily_plan_prompt(ctx))
            if ai_resp.ok:
                return {"ok": True, "message": ai_resp.content, "fallback": False}
        except Exception:
            pass
        msg = fallback_response(user_id, "plan diario", user_name=user_name)
        return {"ok": True, "message": msg, "fallback": True}

    def list_models(self) -> list:
        return MODEL_CATALOG

    def get_history(self, user_id: int, conversation_id: int) -> list:
        from app.models.coach_conversation import CoachConversation, CoachChatMessage
        db = get_db()
        conv = db.query(CoachConversation).filter(
            CoachConversation.id == conversation_id,
            CoachConversation.user_id == user_id,
        ).first()
        if not conv:
            return []
        return [{"role": m.role, "content": m.content, "at": m.created_at.isoformat()} for m in conv.messages]


assistant = CoachAssistantService()
