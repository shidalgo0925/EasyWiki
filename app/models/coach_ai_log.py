# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..extensions import Base


class CoachAICallLog(Base):
    __tablename__ = "coach_ai_call_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(30), nullable=True)
    model = Column(String(100), nullable=True)
    latency_ms = Column(Integer, default=0, nullable=False)
    tokens_input = Column(Integer, default=0, nullable=False)
    tokens_output = Column(Integer, default=0, nullable=False)
    source = Column(String(50), nullable=True)
    success = Column(Boolean, default=False, nullable=False)
    error_code = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
