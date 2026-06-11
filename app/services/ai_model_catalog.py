# -*- coding: utf-8 -*-
"""Catálogo de modelos para pruebas en EasyCoach."""
MODEL_CATALOG = [
    {"use": "Coach diario rápido", "model": "gpt-4o-mini", "provider": "openai", "priority": 1},
    {"use": "Tratamiento / planes complejos", "model": "gpt-4o", "provider": "openai", "priority": 2},
    {"use": "Backup económico", "model": "moonshot-v1-8k", "provider": "kimi", "priority": 3},
    {"use": "Alternativa potente", "model": "claude-sonnet-4-20250514", "provider": "claude", "priority": 4},
    {"use": "Backup adicional", "model": "gemini-2.0-flash", "provider": "gemini", "priority": 5},
    {"use": "Local / documentación", "model": "qwen2.5:7b", "provider": "ollama", "priority": 6},
]

DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"
PLAN_MODEL = "gpt-4o"
