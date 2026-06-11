# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..extensions import Base


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    prioridad = Column(Integer, default=2, nullable=False)  # 1=Alta, 2=Media, 3=Baja
    estado = Column(String(20), default="planeado", nullable=False)  # planeado, en_progreso, bloqueado, completado
    proxima_accion = Column(Text, nullable=True)
    bloqueado_por = Column(Text, nullable=True)
    fecha_objetivo = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User")