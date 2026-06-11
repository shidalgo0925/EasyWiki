# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..extensions import Base


class Win(Base):
    __tablename__ = "wins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    objective_id = Column(Integer, ForeignKey("objectives.id", ondelete="SET NULL"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    daily_focus_id = Column(Integer, ForeignKey("daily_focus.id", ondelete="SET NULL"), nullable=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha = Column(Date, nullable=False)
    impacto = Column(String(20), default="medio", nullable=False)  # bajo, medio, alto
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")
    objective = relationship("Objective")
    project = relationship("Project")
    daily_focus = relationship("DailyFocus")