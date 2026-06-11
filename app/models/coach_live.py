# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..extensions import Base


class CoachActivity(Base):
    __tablename__ = "coach_activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    objective = Column(Text, nullable=True)
    project_key = Column(String(100), nullable=True)
    priority = Column(Integer, default=2, nullable=False)
    scheduled_date = Column(Date, nullable=True)
    scheduled_start_time = Column(Time, nullable=True)
    scheduled_end_time = Column(Time, nullable=True)
    estimated_minutes = Column(Integer, default=30, nullable=False)
    status = Column(String(20), default="draft", nullable=False)
    current_step_id = Column(Integer, nullable=True)
    last_interaction_at = Column(DateTime(timezone=True), nullable=True)
    ai_context = Column(Text, nullable=True)
    ai_recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    steps = relationship("CoachActivityStep", back_populates="activity", cascade="all, delete-orphan", order_by="CoachActivityStep.step_order")
    sessions = relationship("CoachWorkSession", back_populates="activity", cascade="all, delete-orphan")


class CoachActivityStep(Base):
    __tablename__ = "coach_activity_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey("coach_activities.id", ondelete="CASCADE"), nullable=False, index=True)
    step_order = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False)
    user_input_required = Column(Boolean, default=False, nullable=False)
    user_response = Column(Text, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    activity = relationship("CoachActivity", back_populates="steps")


class CoachWorkSession(Base):
    __tablename__ = "coach_work_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_id = Column(Integer, ForeignKey("coach_activities.id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    paused_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="active", nullable=False)
    current_step_id = Column(Integer, nullable=True)
    session_notes = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    activity = relationship("CoachActivity", back_populates="sessions")


class CoachHabitReminder(Base):
    __tablename__ = "coach_habit_reminders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    habit_type = Column(String(30), nullable=False)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    preferred_time = Column(Time, nullable=True)
    interval_minutes = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    last_triggered_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class CoachDailyState(Base):
    __tablename__ = "coach_daily_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    current_mode = Column(String(30), default="normal", nullable=False)
    energy_level = Column(Integer, nullable=True)
    focus_score = Column(Integer, nullable=True)
    agenda_summary = Column(Text, nullable=True)
    active_activity_id = Column(Integer, nullable=True)
    next_recommendation = Column(Text, nullable=True)
    daily_close_done = Column(Boolean, default=False, nullable=False)
    last_water_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class CoachMessage(Base):
    __tablename__ = "coach_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    msg_type = Column(String(20), default="info", nullable=False)
    message = Column(Text, nullable=False)
    suggested_action = Column(String(255), nullable=True)
    action_url = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
