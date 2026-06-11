# EasyWiki — Documentación del Proyecto EasyCoach

> Última actualización: 2026-06-09 10:46 UTC-5

---

## 🚀 Estado Actual del Servidor

| Aspecto | Estado |
|---------|--------|
| **URL** | http://127.0.0.1:5002 |
| **Branch** | `feature/mvp-stabilization` |
| **Servidor** | Flask development (host=127.0.0.1, port=5002) |
| **Estado** | ✅ Corriendo |

---

## 📋 Cambios Realizados (Sesión 2026-06-08)

> **Branch:** `feature/mvp-stabilization`  
> *Último commit: ver `git log --oneline`*

### 1. Diagnóstico y corrección de error `/register`

| Campo | Detalle |
|-------|---------|
| **Problema** | `http://127.0.0.1:5002/register` devolvía **500 Internal Server Error** |
| **Causa raíz** | Faltaba el archivo de template `app/templates/register.html` |
| **Impacto** | Los usuarios no podían acceder al formulario de registro |

**Error original:** `jinja2.exceptions.TemplateNotFound: register.html`

**Solución:** Crear `app/templates/register.html` extendiendo `base.html` con campos: nombre, email, password, confirm.

**Verificación:** ✅ La página carga correctamente en `http://127.0.0.1:5002/register`

### 2. Corrección crítica: Error "Invalid isoformat string: 'now()'" en `/api/ai/plan/commit`

| Campo | Detalle |
|-------|---------|
| **Problema** | Wizard IA paso 7/7 fallaba al guardar: **"Error al guardar"** |
| **Error API** | `{"error":"Invalid isoformat string: 'now()'","ok":false}` |
| **Causa raíz** | En `app/models/daily_focus.py`, las columnas `created_at` usaban `server_default="now()"` (string literal en vez de función SQL) |
| **Impacto** | Insert fallaba en SQLite porque SQLAlchemy no podía parsear `"now()"` como fecha |

**Archivo modificado:** `app/models/daily_focus.py`

**Cambio:**
```python
# ANTES (incorrecto):
created_at = Column(DateTime(timezone=True), server_default="now()", nullable=False)

# DESPUÉS (correcto):
from sqlalchemy import func
created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
```

**Nota:** El problema solo afectó `daily_focus.py`. Los demás modelos ya usaban `func.now()` correctamente.

**Pasos para aplicar fix:**
1. Corregir modelo: cambiar `server_default="now()"` → `server_default=func.now()`
2. Borrar base de datos SQLite (`easycoach_dev.db`) — `create_all` no actualiza columnas existentes
3. Recrear base de datos con `Base.metadata.create_all(bind=engine)`
4. Crear usuario de prueba: `test@example.com` / `test123`

**Verificación:** ✅ `curl -X POST /api/ai/plan/commit` ahora responde:
```json
{"days":1,"items":1,"message":"Plan guardado en DailyFocus","ok":true}
```

---

## 🗂️ Estructura del Proyecto (Snapshot Actual)

```
EasyCoach/
├── .env / .env.example          # Variables de entorno
├── alembic.ini                  # Migraciones Alembic
├── config.py                    # Configuración central
├── requirements.txt             # Dependencias Python
├── run.py                       # Entrypoint (puerto 5002)
├── seed_admin.py                # Script para crear usuarios seed (admin, test, shidalgo)
├── ANALISIS_ACTUAL.md           # Auditoría completa (legacy)
├── MODELO_FUNCIONAL_MVP.md      # Modelo funcional MVP
├── EASYWIKI.md                  # ⬅️ Este archivo
├── app/
│   ├── __init__.py              # Factory create_app()
│   ├── models/                  # Modelos SQLAlchemy
│   ├── routes/                  # Blueprints Flask
│   │   ├── auth.py              # Login, register, OAuth2 Google
│   │   ├── dashboard.py         # Dashboard principal
│   │   ├── wizard_ai_plan.py    # Wizard IA 7 pasos
│   │   ├── api_ai_plan.py       # API endpoints IA
│   │   ├── daily_close.py       # Cierre diario
│   │   ├── strategy.py          # Decisiones y roadmap
│   │   ├── visions.py           # Visiones estratégicas
│   │   └── calendar_sync.py     # Sync Google Calendar
│   ├── services/                # Lógica de negocio + IA
│   ├── static/                  # CSS, JS, imágenes
│   ├── templates/               # Plantillas Jinja2
│   │   ├── base.html            # Layout sidebar principal
│   │   ├── login.html           # Inicio de sesión
│   │   ├── register.html        # ⬅️ NUEVO: Registro de usuarios
│   │   ├── dashboard.html       # Dashboard
│   │   ├── wizard_ai_plan.html  # Wizard IA
│   │   └── ...                  # Otras vistas
│   └── utils/                   # Utilidades (google_calendar, etc.)
├── migrations/                  # Scripts de migración Alembic
└── venv/                        # Entorno virtual Python
```

---

## 🔗 Rutas Principales

| Ruta | Método | Descripción | Estado |
|------|--------|-------------|--------|
| `/` | GET | Dashboard principal | ✅ Activo |
| `/login` | GET, POST | Inicio de sesión | ✅ Activo |
| `/register` | GET, POST | Registro de nuevos usuarios | ✅ **Corregido** |
| `/logout` | GET | Cerrar sesión | ✅ Activo |
| `/google/connect` | GET | Conectar Google Calendar (OAuth2) | ✅ Activo |
| `/oauth2callback` | GET | Callback OAuth2 Google | ✅ Activo |
| `/google/disconnect` | GET | Desconectar Google Calendar | ✅ Activo |
| `/wizard/ai-plan` | GET | Wizard IA 7 pasos | ✅ Activo |
| `/api/ai/plan/suggest` | POST | Sugerir plan IA | ✅ Activo |
| `/api/ai/plan/refine` | POST | Refinar plan IA | ✅ Activo |
| `/api/ai/plan/commit` | POST | Guardar plan en DailyFocus | ✅ **Corregido** |
| `/api/ai/plan/move_to_today` | POST | Mover plan a hoy | ✅ Activo |

---

## 🛠️ Comandos Útiles

```bash
# Ejecutar la aplicación
python run.py

# Ejecutar en navegador
start http://127.0.0.1:5002

# Ver estado de git
git status

# Ver logs del servidor (si corre en background)
type C:\Users\shidalgo\AppData\Local\Temp\cline\background-*.log
```

---

## 🐛 Issues Conocidos (Resueltos y Pendientes)

### ✅ Resueltos
| Issue | Fecha | Solución |
|-------|-------|----------|
| `/register` — 500 Internal Server Error | 2026-06-08 | Crear `app/templates/register.html` |
| `/api/ai/plan/commit` — "Invalid isoformat string: 'now()'" | 2026-06-08 | Cambiar `server_default="now()"` → `func.now()` en `daily_focus.py` + recrear DB |

### 🔄 Pendientes (de auditoría previa)
| Issue | Prioridad | Notas |
|-------|-----------|-------|
| `user_id=1` hardcodeado en todo el código | 🔴 Alta | Reemplazar con sistema de sesiones real |
| `SECRET_KEY` default insegura | 🔴 Alta | Usar variable de entorno |
| Sin tests automatizados | 🟠 Media | Agregar pytest |
| Modelos `Goal` y `Habit` sin uso | 🟠 Media | Decidir: reutilizar o eliminar |
| Layout inconsistente (`base.html` vs `layout_nextro.html`) | 🟡 Baja | Unificar branding |

---

## 📊 Historial de Commits (Branch `feature/mvp-stabilization`)

```
4e220b2  QA MVP: corregir import date faltante en google_calendar.py
2cc2a67  Fase 6: IA real — proveedor OpenAI con contexto completo
c3e33b2  Fase 5: Google Calendar real — tokens en DB, scopes escritura
ab9b0cf  Fase 4: Decisiones y roadmap — modelos, rutas, templates
2ae4d0e  Fase 3: Agregar cierre diario con DailyReflection y Wins
9677a4f  Fase 2: Normalizar modelo diario — DailyFocus + FocusItem
71092fd  Fase 1: Agregar endpoint /api/ai/plan/commit
e6d35ea  Fase 0: Limpieza repo — eliminar auth viejo, backups, credenciales
155338a  feat: base funcional EasyCoach con usuarios y estructura estratégica
2e4373d  chore: saneamiento inicial y modelo funcional EasyCoach MVP
```

---

## 👤 Usuarios Seed

Ejecutar: `python seed_admin.py`

| Email | Contraseña | Rol |
|-------|-----------|-----|
| `admin@easycoach.app` | `admin123` | Administrador |
| `shidalgo@easytech.services` | `easy2026` | Usuario principal |
| `test@example.com` | `test123` | Usuario de prueba |

> **Nota:** `shidalgo@easytech.services` también puede registrarse vía `/register` en la UI.

---

## 📝 Notas Técnicas

- **Puerto:** 5002 (evita conflicto con otros servicios en 5000/5001)
- **Debug mode:** `False` en producción
- **Base de datos:** SQLite (`easycoach_dev.db`) o PostgreSQL (según `.env`)
- **OAuth2:** Requiere `client_secret.json` configurado
- **IA:** Proveedor OpenAI configurado vía variable de entorno `OPENAI_API_KEY`

---

*EasyCoach — Productividad estratégica para coaches y emprendedores*