# ANALISIS_ACTUAL.md

## Auditoría Completa — Proyecto 1% Better Every Day

> Fecha: 2025-06-07  
> Auditor: EasyTech (Programador JR)  
> Objetivo: Entender estado actual antes de migrar a EasyCoach MVP

---

## 1. ARQUITECTURA

| Capa | Tecnología | Versión | Observación |
|------|-----------|---------|-------------|
| **Framework** | Flask | 3.0.2 | Aplicación monolítica Python |
| **Base de datos** | PostgreSQL | — | vía psycopg2-binary |
| **ORM** | SQLAlchemy | ≥2.0 | Modelo declarativo (Base) |
| **Migraciones** | Alembic | ≥1.13 | Configurado, 2 revisiones existentes |
| **Servidor WSGI** | Gunicorn | — | Logs presentes en `logs/` |
| **Entorno** | venv | Python 3.8 | Compatibilidad con backports.zoneinfo |

### Estructura de directorios
```
.
├── alembic.ini              # Configuración Alembic
├── client_secret.json       # Credenciales OAuth2 Google (root)
├── config.py                # Variables de entorno + configuración
├── extensions.py            # (duplicado root, no usado)
├── requirements.txt         # 9 dependencias
├── run.py                   # Entrypoint (host=127.0.0.1, port=5002)
├── .secrets/token.json      # Token OAuth2 usuario
├── app/
│   ├── __init__.py          # Factory create_app(), registra blueprints
│   ├── extensions.py        # Engine, SessionLocal, Base, get_db()
│   ├── models/              # 3 modelos: goals, habits, plan_day
│   ├── routes/              # 5 blueprints + backups
│   ├── services/            # AI Planner + Provider Factory
│   ├── static/              # CSS, JS, Imágenes
│   ├── templates/           # 6 templates HTML
│   └── utils/               # google_calendar.py
├── auth/                    # Blueprint OAuth2 independiente
├── credentials/             # client_secret.json (copia)
├── instance/                # client_secret de Google Cloud
├── logs/                    # gunicorn-access.log, gunicorn-error.log
├── migrations/              # Alembic env + 2 versiones
└── venv/                    # Entorno virtual
```

---

## 2. INVENTARIO DE MODELOS

### 2.1 `Goal` (`app/models/goals.py`)

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| `id` | Integer | PK |
| `user_id` | Integer | NOT NULL, índice |
| `area` | String(32) | NOT NULL |
| `titulo` | String(255) | NOT NULL |
| `kpi` | String(255) | nullable |
| `fecha_objetivo` | Date | nullable |
| `activo` | Boolean | nullable |

**Relaciones:** Ninguna (modelo aislado).

**Uso actual:** El modelo existe en DB pero **no tiene rutas ni UI** que lo gestionen. Solo se importa en `__init__.py`.

---

### 2.2 `Habit` (`app/models/habits.py`)

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| `id` | Integer | PK |
| `user_id` | Integer | NOT NULL, índice |
| `area` | String(32) | NOT NULL |
| `nombre` | String(255) | NOT NULL |
| `frecuencia` | String(1) | nullable |
| `hora_sugerida` | Time | nullable |
| `enabled` | Boolean | nullable |

**Relaciones:** Ninguna.

**Uso actual:** Igual que Goal — **existe en DB pero sin interfaz**.

---

### 2.3 `PlanDay` + `PlanItem` (`app/models/plan_day.py`)

#### PlanDay

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| `id` | Integer | PK |
| `user_id` | Integer | NOT NULL, índice |
| `fecha` | Date | NOT NULL, índice |

**Relaciones:** `items` → 1:N → `PlanItem` (cascade all, delete-orphan)

#### PlanItem

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| `id` | Integer | PK |
| `plan_id` | Integer | FK → plan_day.id, NOT NULL, índice, ON DELETE CASCADE |
| `titulo` | String(255) | NOT NULL |
| `categoria` | String(64) | nullable |
| `prioridad` | Integer | nullable (1..3) |
| `dur_min` | Integer | nullable |
| `from_calendar` | Boolean | default=False |

**Relaciones:** `plan` → N:1 → `PlanDay`

**Uso actual:** ✅ **Activo en dashboard**. Muestra plan del día, permite crear vía Wizard IA, mover a hoy vía API.

---

## 3. INVENTARIO DE RUTAS

### 3.1 Blueprint: `dashboard` (`app/routes/dashboard.py`)

| URL | Método | Función | Estado |
|-----|--------|---------|--------|
| `/` | GET | `dashboard()` | ✅ Activo — muestra calendario + plan |
| `/privacy` | GET | `privacy()` | ✅ Activo — placeholder |
| `/terms` | GET | `terms()` | ✅ Activo — placeholder |

**Observaciones:**
- Dashboard usa `user_id=1` hardcodeado.
- Stats hardcodeadas: `meta_dic=5000`, `prospeccion_min=30`.
- Fallback de eventos mock cuando no hay Google Calendar.
- No usa `Goal` ni `Habit` en la vista.

---

### 3.2 Blueprint: `auth` (`auth/routes.py` + `auth/__init__.py`)

| URL | Método | Función | Estado |
|-----|--------|---------|--------|
| `/google/connect` | GET | `google_connect()` | ✅ Activo — inicia OAuth2 |
| `/oauth2callback` | GET | `oauth2callback()` | ✅ Activo — callback OAuth2 |
| `/google/disconnect` | GET | *(referenciado en templates, no implementado)* | ⚠️ **Falta implementación** |

**Observaciones:**
- No hay logout general, solo desconexión de Google.
- No hay sistema de usuarios real (solo Google OAuth).
- `auth_bp` definido en `auth/__init__.py`, rutas en `auth/routes.py`.

---

### 3.3 Blueprint: `cal` (`app/routes/calendar_sync.py`)

| URL | Método | Función | Estado |
|-----|--------|---------|--------|
| `/sync/today` | GET | `sync_today()` | ⚠️ **Registrado pero NO importado en `create_app()`** |

**Observaciones:** El blueprint `cal_bp` existe pero **nunca se registra** en la aplicación. Código muerto funcional.

---

### 3.4 Blueprint: `ai_wizard` (`app/routes/wizard_ai_plan.py`)

| URL | Método | Función | Estado |
|-----|--------|---------|--------|
| `/wizard/ai-plan` | GET | `ai_plan()` | ✅ Activo — muestra wizard 7 pasos |

---

### 3.5 Blueprint: `api_ai` (`app/routes/api_ai_plan.py`)

| URL | Método | Función | Estado |
|-----|--------|---------|--------|
| `/api/ai/plan/suggest` | POST | `suggest()` | ✅ Activo — genera borrador IA |
| `/api/ai/plan/refine` | POST | `refine()` | ✅ Activo — refina borrador |
| `/api/ai/plan/move_to_today` | POST | `move_to_today()` | ✅ Activo — copia plan a hoy |

**Observaciones:**
- `/api/ai/plan/commit` — **referenciado en `coach.js` pero NO implementado** (retorna 404).
- Todos los endpoints usan `user_id=1` hardcodeado.
- No hay autenticación de API.

---

## 4. INVENTARIO DE TEMPLATES

| Nombre | Hereda de | Uso | Estado |
|--------|-----------|-----|--------|
| `base.html` | — (root) | Layout sidebar oscuro principal | ✅ Activo |
| `dashboard.html` | `base.html` | Vista principal | ✅ Activo |
| `wizard_ai_plan.html` | `base.html` | Wizard 7 pasos IA | ✅ Activo |
| `layout_nextro.html` | — (root alternativo) | Navbar Bootstrap básica | ⚠️ **Usado solo en terms/privacy** |
| `terms.html` | `layout_nextro.html` | Placeholder términos | ⚠️ Inconsistente |
| `privacy.html` | `layout_nextro.html` | Placeholder privacidad | ⚠️ Inconsistente |

**Observaciones:**
- **Dualidad de layouts:** `base.html` (sidebar moderno) vs `layout_nextro.html` (navbar antiguo).
- `terms` y `privacy` heredan del layout antiguo, creando inconsistencia visual.
- `base.html` tiene branding "1% Better Apps", `layout_nextro.html` tiene "1% Mejor Cada Día".

---

## 5. INTEGRACIONES

### 5.1 Google Calendar

| Aspecto | Estado |
|---------|--------|
| OAuth2 | ✅ Implementado |
| Scopes | `calendar.readonly` |
| Lectura | ✅ `get_events_range()`, `get_today_events()` |
| Escritura | ❌ No implementada |
| Categorización | ✅ Por keywords (Mariachi, Easytech, Personal) |
| Zona horaria | ✅ America/Panama |

**Riesgo:** Token guardado en archivo JSON plano (`.secrets/token.json`). No en base de datos.

### 5.2 OAuth2 / Autenticación

| Aspecto | Estado |
|---------|--------|
| Proveedor | Google OAuth2 |
| Flask secret | `"dev-secret-change-me"` (default inseguro) |
| Gestión usuarios | ❌ No existe |
| Sesiones | Solo OAuth state en Flask session |
| RBAC / roles | ❌ No existe |

### 5.3 IA (Inteligencia Artificial)

| Aspecto | Estado |
|---------|--------|
| Provider Factory | ✅ Implementado |
| Adaptador local | ✅ `LocalAdapter` (simulación) |
| OpenAI | ❌ Comentado |
| API endpoints | ✅ `/api/ai/plan/suggest`, `/refine` |
| Wizard UI | ✅ 7 pasos |
| Guardado real | ❌ `/commit` no implementado |

**Observación:** La IA actual es un **mock/simulación**. No conecta con LLM real.

### 5.4 APIs Externas

| API | Uso | Estado |
|-----|-----|--------|
| Google Calendar API | Leer eventos | ✅ Activo |
| Ninguna otra | — | — |

---

## 6. RIESGOS ENCONTRADOS

### 🔴 CRÍTICO

| # | Riesgo | Impacto |
|---|--------|---------|
| 1 | **SECRET_KEY hardcodeada** (`"dev-secret-change-me"`) | Sesiones vulnerables, posible hijacking |
| 2 | **Sin sistema de usuarios** | `user_id=1` hardcodeado en TODO el código |
| 3 | **Token OAuth en archivo plano** | Exposición de credenciales Google |
| 4 | **Credenciales Google en múltiples lugares** | `client_secret.json` en root, credentials/, instance/ |

### 🟠 ALTO

| # | Riesgo | Impacto |
|---|--------|---------|
| 5 | **Modelos Goal y Habit sin uso** | Deuda técnica, tablas huérfanas |
| 6 | **Blueprint `cal` no registrado** | Código muerto confuso |
| 7 | **Endpoint `/api/ai/plan/commit` no existe** | Wizard roto en paso final |
| 8 | **No hay tests** | Cero cobertura, regresiones inevitables |
| 9 | **CSS duplicado/fragmentado** | `style.css` en root + `css/brand.css` + inline en templates |

### 🟡 MEDIO

| # | Riesgo | Impacto |
|---|--------|---------|
| 10 | **Dos layouts inconsistentes** | UX fragmentada |
| 11 | **Stats hardcodeadas** | No reflejan datos reales |
| 12 | **Alembic.ini con `sqlalchemy.url` vacío** | Configuración incompleta |
| 13 | **Backups de archivos (`*.bak`)** | `dashboard.py.bak`, `layout_nextro.html.bak`, `google_calendar.py.bak` |

---

## 7. RECOMENDACIONES

### Para EasyCoach MVP

#### A. SEGURIDAD (Antes de cualquier deploy)
1. **Mover SECRET_KEY a variable de entorno** inmediatamente.
2. **Eliminar/ignorar** todos los `client_secret.json` del repo (usar `.gitignore`).
3. **Mover token OAuth a base de datos** (encriptado) o usar sesiones Flask.

#### B. ARQUITECTURA
4. **Unificar layouts:** Eliminar `layout_nextro.html`, migrar todo a `base.html`.
5. **Limpiar código muerto:** Eliminar `cal_bp` (calendar_sync.py) o registrarlo. Eliminar backups `.bak`.
6. **Implementar `/api/ai/plan/commit`** o quitar el botón del wizard.

#### C. MODELO DE DATOS
7. **Revisar `Goal` y `Habit`:** Decidir si se reutilizan, renombran o eliminan para EasyCoach.
8. **Agregar tabla `users`:** Mínimo: `id`, `email`, `nombre`, `created_at`. Reemplazar `user_id=1` hardcodeado.

#### D. REUTILIZACIÓN MVP
| Componente | Reutilizar | Notas |
|------------|-----------|-------|
| Flask + SQLAlchemy + Alembic | ✅ SÍ | Base sólida |
| Estructura de blueprints | ✅ SÍ | Ampliar, no reescribir |
| Google Calendar utils | ✅ SÍ | Refactorizar categorías |
| PlanDay / PlanItem | ✅ SÍ | Renombrar a `daily_focus` |
| Wizard IA UI | ⚠️ PARCIAL | Rediseñar, eliminar dependencia IA |
| Goal / Habit modelos | ❌ NO | Reemplazar por `visions`, `projects`, `objectives` |
| Auth actual | ❌ NO | Rehacer con tabla users real |

#### E. ARCHIVOS A ELIMINAR
- `app/routes/calendar_sync.py` (o registrar el blueprint)
- `app/routes/dashboard.py.bak`
- `app/templates/layout_nextro.html.bak`
- `app/utils/google_calendar.py.bak`
- `extensions.py` (root, duplicado no usado)
- `logo_1percent_better.png` (rebranding)
- `.secrets/token.json` (del repo, ignorar)

---

## 8. RESUMEN EJECUTIVO

| Aspecto | Estado |
|---------|--------|
| **Framework base** | Flask + SQLAlchemy, estable y reutilizable |
| **Funcionalidad actual** | Dashboard con calendario, plan diario básico, wizard IA simulado |
| **Deuda técnica** | Alta — código huérfano, sin tests, hardcodeos |
| **Seguridad** | Débil — secrets expuestos, sin autenticación real |
| **Escalabilidad** | Baja — `user_id=1` en todo lado |
| **Reutilizable para MVP** | ~60% del scaffold (Flask, DB, migraciones, base templates) |

**Veredicto:** El proyecto tiene una base Flask sólida que puede servir para EasyCoach MVP, pero requiere:
1. Limpieza de deuda técnica
2. Implementación de autenticación real
3. Rediseño del modelo de datos
4. Eliminación de funcionalidad IA mock
5. Rebranding completo

---

*Fin del análisis. Listo para crear rama y continuar con tareas de diseño MVP.*