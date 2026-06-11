# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from ..extensions import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    nombre = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    timezone = Column(String(50), default="America/Panama", nullable=False)
    google_refresh_token = Column(String(500), nullable=True)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    visions = relationship("Vision", back_populates="user", cascade="all, delete-orphan")
    areas = relationship("Area", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    objectives = relationship("Objective", back_populates="user", cascade="all, delete-orphan")
