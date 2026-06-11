# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from ..extensions import Base


class Objective(Base):
    __tablename__ = "objectives"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    kpi = Column(String(255), nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_objetivo = Column(Date, nullable=False)
    progreso_pct = Column(Integer, default=0, nullable=False)
    estado = Column(String(20), default="activo", nullable=False)
    prioridad = Column(Integer, default=2, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="objectives")
    user = relationship("User", back_populates="objectives")