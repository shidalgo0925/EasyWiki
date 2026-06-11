# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..extensions import Base


class DailyReflection(Base):
    __tablename__ = "daily_reflections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    daily_focus_id = Column(Integer, ForeignKey("daily_focus.id", ondelete="SET NULL"), nullable=True)
    fecha = Column(Date, nullable=False)
    que_funciono = Column(Text, nullable=True)
    que_bloqueo = Column(Text, nullable=True)
    aprendizaje = Column(Text, nullable=True)
    ajuste_manana = Column(Text, nullable=True)
    estado_animo = Column(String(50), nullable=True)
    energia_final = Column(Integer, nullable=True)  # 1..5
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "fecha", name="uq_reflections_user_fecha"),
    )

    user = relationship("User")
    daily_focus = relationship("DailyFocus")