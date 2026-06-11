# EasyCoach

## Origen

Evolución del proyecto **1% Better Every Day**.

## Visión

Asistente personal de coaching impulsado por IA que ayuda a convertir metas grandes en acciones diarias ejecutables.

La IA no es un chatbot aislado: opera sobre datos reales del sistema (tratamiento activo, actividades guiadas, agenda, roadmap, decisiones, cierre diario, hábitos).

## Principios

- No obliga.
- No juzga.
- No controla.
- Acompaña.
- Recuerda.
- Sugiere.

## Problema que resuelve

Las personas conocen sus metas pero no saben qué hacer hoy para acercarse a ellas.

## Objetivo

Guiar al usuario desde:

```
Visión → Objetivos → Metas → Plan semanal → Plan diario → Acciones concretas → Seguimiento → Mejora continua
```

---

## Estado actual (2026-06-10)

| Aspecto | Detalle |
|---------|---------|
| **Fase** | MVP en estabilización |
| **Branch código** | `feature/mvp-stabilization` (repo EasyWiki) |
| **Commit** | `8e97aab` — capa IA interactiva, actividades guiadas y tratamiento |
| **URL local** | http://127.0.0.1:5002 |
| **Usuario Caso 0** | `shidalgo@easytech.services` (Seul) |
| **Stack** | Flask, SQLAlchemy, SQLite dev / PostgreSQL prod, Google Calendar, IA multi-proveedor |

### Implementado

- Dashboard con bloque **Coach ahora** (contexto ejecutivo en tiempo real)
- Panel flotante **Coach IA** (chat con memoria y fallback sin IA)
- Capa central: `CoachAssistantService` → `CoachContextBuilder` → `CoachPromptBuilder` → `AIProviderRouter`
- Proveedores IA: OpenAI, Kimi, Claude, Gemini, Ollama (configurable en `/settings/ai` y `.env`)
- Actividades guiadas paso a paso (`/coach/activity/<id>`, wizard `/wizard/activity`)
- Wizard de tratamiento (`/wizard/treatment`) con perfil activo por usuario
- API coach: `/api/coach/message`, `/api/coach/context`, `/api/coach/daily-recommendation`
- Decisiones, roadmap, cierre diario, Google Calendar, plan diario IA

### Pendiente (Fase 6)

- Agenda Google profunda en context builder
- IA generando pasos automáticos en wizard actividad
- Resumen diario/semanal automatizado
- Daily Brief (6 preguntas diarias)
- Migraciones Alembic unificadas
- Tests automatizados

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

**Regla clave:** las pantallas no llaman al modelo directamente. Toda interacción IA pasa por la capa central.

Documentación técnica: [[Coach_IA_Implementacion]]

---

## Roadmap (actualizado)

### ✅ Fase 0–1 — Base MVP
- Análisis, rebranding, plan diario, commit IA

### ✅ Fase 2–3 — Modelo diario y cierre
- DailyFocus, DailyReflection, Wins

### ✅ Fase 4–5 — Estrategia e integraciones
- Decisiones, roadmap, Google Calendar real

### ✅ Fase 6 — IA real
- OpenAI con contexto de EasyCoach

### ✅ Fase 7 — Coach vivo (2026-06-10)
- Capa IA interactiva, actividades guiadas, tratamiento, config multi-modelo

### 🔜 Fase 8 — Inteligencia contextual
- Agenda en contexto, resúmenes, hábitos avanzados

---

## Arquitectura base

**Proyecto origen:** 1% Better Every Day

### Tecnologías

- Flask
- PostgreSQL / SQLite (dev)
- SQLAlchemy + Alembic
- Google Calendar OAuth2
- IA multi-proveedor (OpenAI-compatible, Anthropic, Gemini, Ollama)

### Repositorio

- **Código app:** rama `feature/mvp-stabilization` en [EasyWiki](https://github.com/shidalgo0925/EasyWiki/tree/feature/mvp-stabilization)
- **Documentación:** carpeta `05_Proyectos/EasyCoach/` en `main`

---

## Prioridad

**Alta** — Caso 0 activo (Seul / EasyTech)

## Responsable

Programador JR + Seul (producto / validación)
