# EasyCoach — Capa IA Interactiva

> Última actualización: 2026-06-10  
> Commit: `8e97aab` — rama `feature/mvp-stabilization`

---

## Objetivo

Conectar modelos de IA a datos reales del sistema para que EasyCoach actúe como coach personal, ejecutivo y contextual.

El coach puede decir al usuario:

- dónde va
- qué estaba haciendo
- qué falta
- qué espera del usuario
- qué actividad toca según la agenda
- cuándo debe cerrar el día
- cuándo debe tomar agua o hacer pausa

---

## Flujo técnico

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

Si todos los proveedores fallan → `coach_fallback_rules.py` (sin error técnico al usuario).

---

## Servicios principales

| Archivo | Responsabilidad |
|---------|-----------------|
| `ai_provider_router.py` | Llamadas multi-proveedor, fallback chain, logging |
| `coach_assistant_service.py` | Orquestador `send_message()` |
| `coach_context_builder.py` | Contexto estructurado (dict JSON) |
| `coach_prompt_builder.py` | Prompts por modo (dashboard, activity, treatment, etc.) |
| `coach_fallback_rules.py` | Respuestas sin IA |
| `coach_memory_service.py` | Conversaciones y mensajes |
| `coach_live_service.py` | Coach ahora, actividades, sesiones, hábitos |
| `treatment_service.py` | Perfil de tratamiento activo |

---

## Modelos de base de datos

| Modelo | Uso |
|--------|-----|
| `CoachTreatmentProfile` | Tratamiento activo del usuario (1 activo por usuario) |
| `CoachActivity` | Actividad guiada |
| `CoachActivityStep` | Paso dentro de actividad |
| `CoachWorkSession` | Sesión de trabajo sobre actividad |
| `CoachConversation` | Hilo de conversación |
| `CoachChatMessage` | Mensajes con provider/model/latency/tokens |
| `CoachHabitReminder` | Recordatorios (agua, pausa, cierre, etc.) |
| `CoachDailyState` | Estado diario del coach |
| `CoachAICallLog` | Log de llamadas IA (sin API keys) |
| `CoachAIConfig` | Config por usuario en `/settings/ai` |

Scripts de migración manual: `scripts/ensure_*.py`

---

## API

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/coach/message` | Enviar mensaje al coach |
| POST | `/api/coach/chat` | Alias retrocompatible |
| GET | `/api/coach/context` | Contexto estructurado del usuario |
| GET | `/api/coach/conversation` | Última conversación |
| POST | `/api/coach/activity/<id>/message` | Mensaje en contexto de actividad |
| POST | `/api/coach/daily-recommendation` | Recomendación del día |
| GET | `/api/coach/models` | Catálogo de modelos |
| GET | `/api/coach/history/<id>` | Historial de conversación |

---

## Rutas de actividades guiadas

| Método | Ruta |
|--------|------|
| GET | `/coach/activity/<id>` |
| POST | `/coach/activity/<id>/start` |
| POST | `/coach/activity/<id>/pause` |
| POST | `/coach/activity/<id>/complete` |
| POST | `/coach/activity/<id>/blocked` |
| POST | `/coach/activity/<id>/step/<step_id>/complete` |
| GET | `/wizard/activity` |
| GET | `/wizard/treatment` |

---

## Variables de entorno

Ver `.env.example` en el repo de código. Claves mínimas:

```env
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
OPENAI_API_KEY=
AI_TIMEOUT_SECONDS=60
AI_MAX_TOKENS=1200
AI_TEMPERATURE=0.4
AI_FALLBACK_ENABLED=true
```

También: Kimi, Anthropic, Gemini, Ollama. **No subir llaves al repositorio.**

---

## UI

- **Coach ahora** — bloque superior en dashboard
- **Coach IA** — panel flotante (esquina inferior derecha) en dashboard, actividades, roadmap, decisiones
- **Configuración IA** — `/settings/ai` (estilo CLINE: proveedor, modelo, test de conexión)

---

## Reglas de seguridad

La IA **recomienda**. El sistema **ejecuta** solo con confirmación del usuario.

La IA no puede:

- borrar datos
- ejecutar acciones críticas sin confirmación
- cambiar agenda sin confirmación
- marcar actividades completadas sin acción explícita
- inventar datos de roadmap, decisiones o agenda

---

## Criterios de aceptación (cumplidos)

1. ✅ AIProviderRouter
2. ✅ CoachAssistantService
3. ✅ CoachContextBuilder
4. ✅ CoachPromptBuilder
5. ✅ Fallback sin IA
6. ✅ Mensaje desde UI
7. ✅ Conversación guardada
8. ✅ Dashboard Coach ahora
9. ✅ Actividad activa y paso actual
10. ✅ Fallback útil si IA falla
11. ✅ No rompe módulos existentes
12. ✅ Modelo configurable por env / settings
13. ✅ Logs de proveedor/modelo/error
14. ✅ Sin API keys en Git

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
```

---

*EasyCoach — La IA da la voz. La aplicación mantiene la memoria, el control y la ejecución.*
