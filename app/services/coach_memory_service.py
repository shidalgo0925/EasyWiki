# -*- coding: utf-8 -*-
"""Memoria de conversaciones del coach."""
from typing import Optional, List

from app.extensions import get_db
from app.models.coach_conversation import CoachConversation, CoachChatMessage


def get_or_create_conversation(
    user_id: int,
    source: str = "floating_chat",
    activity_id: Optional[int] = None,
    treatment_id: Optional[int] = None,
    conversation_id: Optional[int] = None,
    title: str = "",
) -> CoachConversation:
    db = get_db()
    if conversation_id:
        conv = db.query(CoachConversation).filter(
            CoachConversation.id == conversation_id,
            CoachConversation.user_id == user_id,
        ).first()
        if conv:
            return conv

    conv = CoachConversation(
        user_id=user_id,
        title=title[:255] if title else "Conversación coach",
        source=source,
        screen_context=source,
        activity_id=activity_id,
        treatment_id=treatment_id,
    )
    db.add(conv)
    db.flush()
    return conv


def save_message(
    conversation_id: int,
    role: str,
    content: str,
    user_id: int = None,
    provider: str = None,
    model: str = None,
    latency_ms: int = 0,
    tokens_input: int = 0,
    tokens_output: int = 0,
    error_code: str = None,
) -> CoachChatMessage:
    db = get_db()
    msg = CoachChatMessage(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        provider=provider,
        model=model,
        latency_ms=latency_ms,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        error_code=error_code,
    )
    db.add(msg)
    return msg


def get_history(conversation_id: int, limit: int = 12) -> List[dict]:
    db = get_db()
    msgs = db.query(CoachChatMessage).filter(
        CoachChatMessage.conversation_id == conversation_id,
        CoachChatMessage.role.in_(["user", "assistant"]),
    ).order_by(CoachChatMessage.created_at.desc()).limit(limit).all()
    return [{"role": m.role, "content": m.content} for m in reversed(msgs)]


def get_latest_conversation(user_id: int, source: str = None) -> Optional[CoachConversation]:
    db = get_db()
    q = db.query(CoachConversation).filter(CoachConversation.user_id == user_id)
    if source:
        q = q.filter(CoachConversation.source == source)
    return q.order_by(CoachConversation.updated_at.desc()).first()
