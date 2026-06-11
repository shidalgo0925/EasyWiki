# EasyWiki — Documentación del Proyecto EasyCoach

> Última actualización: 2026-06-10  
> Commit código: `8e97aab` — rama `feature/mvp-stabilization`  
> Wiki oficial (main): `05_Proyectos/EasyCoach/` en [EasyWiki](https://github.com/shidalgo0925/EasyWiki)

---

## Estado actual

| Aspecto | Detalle |
|---------|---------|
| **URL local** | http://127.0.0.1:5002 |
| **Fase** | MVP en estabilización — Caso 0 activo (Seul) |
| **Branch código** | `feature/mvp-stabilization` (repo EasyWiki) |
| **Branch wiki** | `main` (documentación markdown) |
| **Servidor** | Flask development (host=127.0.0.1, port=5002) |
| **Base de datos dev** | SQLite `easycoach_dev.db` |
| **Zona horaria** | `America/Panama` |

### Implementado (2026-06-10)

- **Coach ahora** — bloque contextual en dashboard (actividad activa, atrasos, noche, agua, sin plan)
- **Coach IA** — panel flotante con chat, memoria y fallback sin IA
- **Capa IA central** — `CoachAssistantService` → `CoachContextBuilder` → `CoachPromptBuilder` → `AIProviderRouter`
- **Multi-proveedor** — OpenAI, Kimi, Claude, Gemini, Ollama (`/settings/ai` + `.env`)
- **Actividades guiadas** — pasos, sesiones, wizard `/wizard/activity`
- **Tratamiento activo** — wizard `/wizard/treatment`, 1 perfil activo por usuario
- **Plan diario IA**, cierre diario, decisiones, roadmap, Google Calendar

### Pendiente (Fase 8)

- Agenda Google profunda en context builder
- IA generando pasos en wizard actividad
- Resumen diario/semanal, Daily Brief
- Migraciones Alembic unificadas, tests automatizados
- `user_id` hardcodeado en endpoints legacy

---

## Arquitectura IA

```
UI / Dashboard / Wizard / Chat
        ↓
CoachAssistantService
        ↓
CoachContextBuilder
        ↓
CoachPromptBuilder
        ↓
AIProviderRouter
        ↓
OpenAI / Kimi / Claude / Gemini / Ollama
```

**Regla:** las pantallas no llaman al modelo directamente.

Documentación extendida en EasyWiki: `05_Proyectos/EasyCoach/Coach_IA_Implementacion.md`

---

## Estructura del proyecto

```
EasyCoach/
├── .env / .env.example
├── config.py
├── run.py                         # Puerto 5002
├── seed_admin.py
├── EASYWIKI.md                    # Este archivo (espejo operativo del wiki)
├── scripts/
│   ├── ensure_coach_live_tables.py
│   ├── ensure_coach_chat_tables.py
│   ├── ensure_coach_ai_config_table.py
│   └── ensure_ai_layer_tables.py
├── app/
│   ├── models/
│   │   ├── coach_live.py          # Activity, Step, Session, Habit, DailyState
│   │   ├── coach_treatment_profile.py
│   │   ├── coach_conversation.py
│   │   ├── coach_ai_config.py
│   │   └── coach_ai_log.py
│   ├── routes/
│   │   ├── dashboard.py
│   │   ├── coach_ai.py            # /api/coach/*
│   │   ├── coach_activity.py      # /coach/activity/*, /wizard/activity
│   │   ├── wizard_treatment.py
│   │   ├── settings.py            # /settings/ai
│   │   ├── wizard_ai_plan.py
│   │   ├── api_ai_plan.py
│   │   ├── daily_close.py
│   │   ├── strategy.py
│   │   └── calendar_sync.py
│   ├── services/
│   │   ├── coach_assistant_service.py
│   │   ├── coach_context_builder.py
│   │   ├── coach_prompt_builder.py
│   │   ├── coach_fallback_rules.py
│   │   ├── coach_memory_service.py
│   │   ├── coach_live_service.py
│   │   ├── ai_provider_router.py
│   │   ├── treatment_service.py
│   │   └── ai_config_service.py
│   ├── static/css/coach.css
│   ├── static/js/live_coach.js
│   └── templates/
│       ├── dashboard.html         # Coach ahora
│       ├── base.html              # Panel flotante Coach IA
│       ├── coach/activity.html
│       ├── wizard_activity.html
│       ├── wizard_treatment.html
│       └── settings/ai.html
└── migrations/
```

---

## Rutas principales

### App

| Ruta | Descripción |
|------|-------------|
| `/` | Dashboard + Coach ahora |
| `/login`, `/register`, `/logout` | Autenticación |
| `/wizard/ai-plan` | Plan diario con IA |
| `/wizard/activity` | Nueva actividad guiada |
| `/wizard/treatment` | Wizard de tratamiento |
| `/coach/activity/<id>` | Actividad paso a paso |
| `/daily/close` | Cierre diario |
| `/settings/ai` | Configuración de modelos IA |
| `/strategy/decisions`, `/strategy/roadmap` | Estrategia |

### API Coach

| Método | Ruta |
|--------|------|
| POST | `/api/coach/message` |
| GET | `/api/coach/context` |
| GET | `/api/coach/conversation` |
| POST | `/api/coach/activity/<id>/message` |
| POST | `/api/coach/daily-recommendation` |
| GET | `/api/coach/models` |

### API Plan IA (legacy)

| Método | Ruta |
|--------|------|
| POST | `/api/ai/plan/suggest` |
| POST | `/api/ai/plan/refine` |
| POST | `/api/ai/plan/commit` |

---

## Comandos útiles

```bash
# Migrar tablas coach (SQLite dev)
python scripts/ensure_coach_live_tables.py
python scripts/ensure_coach_chat_tables.py
python scripts/ensure_coach_ai_config_table.py
python scripts/ensure_ai_layer_tables.py

# Ejecutar app
python run.py

# Usuarios seed
python seed_admin.py

# Reiniciar servidor (si puerto 5002 ocupado)
# Matar proceso viejo antes de run.py
```

---

## Variables de entorno (IA)

Ver `.env.example`. Mínimo:

```env
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
OPENAI_API_KEY=
AI_FALLBACK_ENABLED=true
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

También configurable por usuario en `/settings/ai`. **No subir `.env` ni tokens al repo.**

---

## Usuarios seed

| Email | Contraseña | Rol |
|-------|-----------|-----|
| `shidalgo@easytech.services` | `easy2026` | Caso 0 — Seul |
| `admin@easycoach.app` | `admin123` | Administrador |
| `test@example.com` | `test123` | Prueba |

---

## Historial relevante

### Sesión 2026-06-10 — Capa IA interactiva

- `8e97aab` feat(coach): capa IA, actividades guiadas, tratamiento, config multi-modelo
- Push limpio a `origin/feature/mvp-stabilization` (sin secretos en historial)
- Wiki actualizado en `main`: `d5906f3` docs(EasyCoach)

### Sesión 2026-06-08 — Fixes MVP

- `/register` — template faltante → `register.html`
- `/api/ai/plan/commit` — `server_default="now()"` → `func.now()` en `daily_focus.py`

---

## Issues conocidos

| Issue | Prioridad | Estado |
|-------|-----------|--------|
| `user_id=1` hardcodeado en endpoints legacy | Alta | Pendiente |
| Alembic desincronizado (scripts manuales) | Media | Pendiente |
| Sin tests automatizados | Media | Pendiente |
| Servidor viejo en :5002 sirve código antiguo | Media | Reiniciar proceso + Ctrl+F5 |

---

## Sincronización wiki ↔ código

| Qué | Dónde |
|-----|-------|
| Documentación estratégica | EasyWiki `main` → `05_Proyectos/EasyCoach/` |
| Código de la app | EasyWiki `feature/mvp-stabilization` |
| Espejo operativo local | `EASYWIKI.md` (este archivo, en repo de código) |

Al cerrar una sesión de desarrollo: actualizar **ambos** — wiki en `main` y `EASYWIKI.md` en la rama de código.

---

*EasyCoach — La IA da la voz. La aplicación mantiene la memoria, el control y la ejecución.*
