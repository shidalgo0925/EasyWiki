# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..extensions import Base


class CoachAIConfig(Base):
    __tablename__ = "coach_ai_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    api_provider = Column(String(30), default="rules", nullable=False)
    use_custom_base_url = Column(Boolean, default=False, nullable=False)
    base_url = Column(String(500), nullable=True)
    api_key = Column(String(500), nullable=True)
    model = Column(String(120), default="gpt-4o-mini", nullable=False)
    context_window = Column(Integer, default=4096, nullable=False)
    request_timeout_ms = Column(Integer, default=180000, nullable=False)
    use_compact_prompt = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
