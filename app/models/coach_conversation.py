# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..extensions import Base


class CoachConversation(Base):
    __tablename__ = "coach_conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    source = Column(String(50), default="floating_chat", nullable=True)
    screen_context = Column(String(100), nullable=True)
    activity_id = Column(Integer, nullable=True)
    treatment_id = Column(Integer, nullable=True)
    provider_used = Column(String(30), nullable=True)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    messages = relationship("CoachChatMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="CoachChatMessage.created_at")


class CoachChatMessage(Base):
    __tablename__ = "coach_chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("coach_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    provider = Column(String(30), nullable=True)
    model = Column(String(100), nullable=True)
    latency_ms = Column(Integer, default=0, nullable=False)
    tokens_input = Column(Integer, default=0, nullable=False)
    tokens_output = Column(Integer, default=0, nullable=False)
    error_code = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("CoachConversation", back_populates="messages")
