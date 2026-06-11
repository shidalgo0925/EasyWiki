# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Boolean, UniqueConstraint, func
from sqlalchemy.orm import relationship
from ..extensions import Base


class DailyFocus(Base):
    __tablename__ = "daily_focus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    intencion = Column(String(255), nullable=True)
    energia_nivel = Column(Integer, nullable=True)  # 1..5
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "fecha", name="uq_daily_focus_user_fecha"),
    )

    user = relationship("User")
    items = relationship("FocusItem", back_populates="daily_focus", cascade="all, delete-orphan")


class FocusItem(Base):
    __tablename__ = "focus_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_focus_id = Column(Integer, ForeignKey("daily_focus.id", ondelete="CASCADE"), nullable=False, index=True)
    objective_id = Column(Integer, ForeignKey("objectives.id", ondelete="SET NULL"), nullable=True)
    titulo = Column(String(255), nullable=False)
    categoria = Column(String(64), nullable=True)
    hora_inicio = Column(Time, nullable=True)
    duracion_min = Column(Integer, nullable=True)
    prioridad = Column(Integer, default=2, nullable=False)  # 1=Alta, 2=Media, 3=Baja
    estado = Column(String(20), default="pendiente", nullable=False)  # pendiente, en_progreso, completada, pospuesta
    from_calendar = Column(Boolean, default=False, nullable=False)
    google_event_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    daily_focus = relationship("DailyFocus", back_populates="items")
    objective = relationship("Objective")