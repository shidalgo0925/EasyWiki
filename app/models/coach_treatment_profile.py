# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..extensions import Base


class CoachTreatmentProfile(Base):
    __tablename__ = "coach_treatment_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    current_situation = Column(Text, nullable=True)
    main_problem = Column(Text, nullable=True)
    primary_area = Column(String(100), nullable=True)
    goal_30_days = Column(Text, nullable=True)
    goal_90_days = Column(Text, nullable=True)
    success_definition = Column(Text, nullable=True)
    obstacles = Column(Text, nullable=True)  # JSON array
    current_routine = Column(Text, nullable=True)  # JSON object
    commitment_level = Column(String(20), nullable=True)
    coaching_preferences = Column(Text, nullable=True)  # JSON object
    status = Column(String(20), default="draft", nullable=False)  # draft, active, archived
    wizard_step = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User")
