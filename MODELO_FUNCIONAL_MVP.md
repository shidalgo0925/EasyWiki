# MODELO_FUNCIONAL_MVP.md

## Modelo de Datos — EasyCoach MVP

> Versión: 1.1 (Ajustado con EasyTech Advisor)  
> Estado: DISEÑO APROBADO — listo para Sprint 1  
> Objetivo: Reemplazar modelo actual por entidades orientadas a coaching personal + advisor.

---

## VISIÓN GENERAL

```
┌─────────────┐     1:N     ┌─────────────┐     1:N     ┌─────────────┐
│   users     │◄────────────│   visions   │◄────────────│   areas     │
└─────────────┘             └─────────────┘             └──────┬──────┘
                                                               │
                                                               │ 1:N
                                                               ▼
                                                        ┌─────────────┐
                                                        │  projects   │
                                                        └──────┬──────┘
                                                               │
                                                               │ 1:N
                                                               ▼
                                                        ┌─────────────┐
                                                        │  objectives │
                                                        └─────────────┘

┌─────────────┐     1:N     ┌─────────────┐     1:N     ┌─────────────┐
│   users     │◄────────────│ daily_focus │◄───────────│ focus_items │
└─────────────┘             └─────────────┘            └─────────────┘

┌─────────────┐     1:N     ┌─────────────────┐
│   users     │◄────────────│ daily_reflections│
└─────────────┘             └─────────────────┘

┌─────────────┐     1:N     ┌─────────────┐
│   users     │◄────────────│  decisions  │
└─────────────┘             └─────────────┘

┌─────────────┐     1:N     ┌─────────────────┐
│   users     │◄────────────│  roadmap_items  │
└─────────────┘             └─────────────────┘

┌─────────────┐     1:N     ┌─────────────┐
│   users     │◄────────────│    wins     │
└─────────────┘             └─────────────┘
```

---

## ENTIDADES

### 1. `users`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador único |
| `email` | String(255) | NOT NULL, UNIQUE | Email del usuario |
| `nombre` | String(100) | nullable | Nombre visible |
| `avatar_url` | String(500) | nullable | URL de imagen de perfil |
| `timezone` | String(50) | DEFAULT 'America/Panama' | Zona horaria |
| `google_refresh_token` | String(500) | nullable | Token OAuth2 Google (encriptado) |
| `created_at` | DateTime | DEFAULT now() | Fecha de registro |
| `updated_at` | DateTime | DEFAULT now() | Última actualización |
| `is_active` | Boolean | DEFAULT True | Cuenta activa |

**Índices:** `idx_users_email` (UNIQUE), `idx_users_active`

---

### 2. `visions`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `titulo` | String(255) | NOT NULL | Título de la visión |
| `descripcion` | Text | nullable | Descripción detallada |
| `horizonte` | String(20) | DEFAULT '5y' | Horizonte temporal (1y, 3y, 5y, 10y) |
| `color` | String(7) | DEFAULT '#1f6feb' | Color identificativo |
| `is_active` | Boolean | DEFAULT True | Visión activa |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `updated_at` | DateTime | DEFAULT now() | Última modificación |

**Relaciones:** `areas` → 1:N

**Índices:** `idx_visions_user_id`, `idx_visions_active`

---

### 3. `areas` — Áreas de Vida / Negocio

> Áreas estratégicas bajo una visión. Ej: EasyTech, Personal, Familia, Salud.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `vision_id` | Integer | NOT NULL, FK → visions.id, ON DELETE CASCADE | Visión padre |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `nombre` | String(100) | NOT NULL | Nombre del área |
| `descripcion` | Text | nullable | Descripción |
| `color` | String(7) | DEFAULT '#6c757d' | Color identificativo |
| `orden` | Integer | DEFAULT 0 | Orden visual |
| `is_active` | Boolean | DEFAULT True | Activa |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `updated_at` | DateTime | DEFAULT now() | Última modificación |

**Relaciones:** `projects` → 1:N

**Índices:** `idx_areas_vision_id`, `idx_areas_user_id`, `idx_areas_active`

---

### 4. `projects` — Proyectos Concretos

> Proyectos dentro de un área. Ej: EN1, IIUS, Relatic, EasyCoach.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `area_id` | Integer | NOT NULL, FK → areas.id, ON DELETE CASCADE | Área padre |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `nombre` | String(150) | NOT NULL | Nombre del proyecto |
| `descripcion` | Text | nullable | Descripción |
| `color` | String(7) | DEFAULT '#0d6efd' | Color identificativo |
| `orden` | Integer | DEFAULT 0 | Orden visual |
| `is_active` | Boolean | DEFAULT True | Activo |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `updated_at` | DateTime | DEFAULT now() | Última modificación |

**Relaciones:** `objectives` → 1:N

**Índices:** `idx_projects_area_id`, `idx_projects_user_id`, `idx_projects_active`

---

### 5. `objectives` — Objetivos SMART

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `project_id` | Integer | NOT NULL, FK → projects.id, ON DELETE CASCADE | Proyecto padre |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `titulo` | String(255) | NOT NULL | Título |
| `descripcion` | Text | nullable | Descripción |
| `kpi` | String(255) | nullable | Métrica de éxito |
| `fecha_inicio` | Date | DEFAULT today() | Inicio |
| `fecha_objetivo` | Date | NOT NULL | Fecha límite |
| `progreso_pct` | Integer | DEFAULT 0 | 0-100 |
| `estado` | String(20) | DEFAULT 'activo' | activo, completado, pausado, cancelado |
| `prioridad` | Integer | DEFAULT 2 | 1=Alta, 2=Media, 3=Baja |
| `is_active` | Boolean | DEFAULT True | Activo |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `updated_at` | DateTime | DEFAULT now() | Última modificación |

**Relaciones:** `focus_items` → 1:N (opcional)

**Índices:** `idx_objectives_project_id`, `idx_objectives_estado`, `idx_objectives_fecha`, `idx_objectives_prioridad`

---

### 6. `daily_focus` — Enfoque Diario

> Reemplaza `PlanDay`.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `fecha` | Date | NOT NULL | Día del plan |
| `intencion` | String(255) | nullable | Intención/frase del día |
| `energia_nivel` | Integer | nullable | 1-5 |
| `reviewed_at` | DateTime | nullable | Cuándo se revisó |
| `created_at` | DateTime | DEFAULT now() | Creación |

**Restricción:** UNIQUE (`user_id`, `fecha`)

**Relaciones:** `items` → 1:N → `focus_items`

**Índices:** `idx_daily_focus_user_fecha` (UNIQUE), `idx_daily_focus_fecha`

---

### 7. `focus_items` — Acciones del Plan Diario

> Reemplaza `PlanItem`.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `daily_focus_id` | Integer | NOT NULL, FK → daily_focus.id, ON DELETE CASCADE | Plan padre |
| `objective_id` | Integer | nullable, FK → objectives.id, ON DELETE SET NULL | Vinculación |
| `titulo` | String(255) | NOT NULL | Descripción |
| `categoria` | String(64) | nullable | Categoría |
| `hora_inicio` | Time | nullable | Hora planificada |
| `duracion_min` | Integer | nullable | Duración estimada |
| `prioridad` | Integer | DEFAULT 2 | 1=Alta, 2=Media, 3=Baja |
| `estado` | String(20) | DEFAULT 'pendiente' | pendiente, en_progreso, completada, pospuesta |
| `from_calendar` | Boolean | DEFAULT False | Proviene de Google Calendar |
| `google_event_id` | String(255) | nullable | ID evento Google |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `completed_at` | DateTime | nullable | Cuándo se completó |

**Índices:** `idx_focus_items_daily_focus`, `idx_focus_items_estado`, `idx_focus_items_prioridad`

---

### 8. `daily_reflections` — Reflexión Diaria

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `fecha` | Date | NOT NULL | Día |
| `logro_principal` | Text | nullable | ¿Qué logré hoy? |
| `desafio` | Text | nullable | ¿Qué me costó? |
| `aprendizaje` | Text | nullable | ¿Qué aprendí? |
| `gratitud` | Text | nullable | ¿Por qué estoy agradecido? |
| `manana_intencion` | Text | nullable | ¿Qué quiero para mañana? |
| `energia_nivel` | Integer | nullable | 1-5 |
| `productividad_nivel` | Integer | nullable | 1-5 |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `updated_at` | DateTime | DEFAULT now() | Última modificación |

**Restricción:** UNIQUE (`user_id`, `fecha`)

**Índices:** `idx_reflections_user_fecha` (UNIQUE), `idx_reflections_fecha`

---

### 9. `decisions` — Decisiones Estratégicas

> EasyTech Advisor debe recordar decisiones tomadas para no re-discutirlas.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `decision_date` | Date | NOT NULL | Fecha de la decisión |
| `title` | String(255) | NOT NULL | Título / resumen |
| `reason` | Text | nullable | Razón / contexto |
| `expected_result` | Text | nullable | Resultado esperado |
| `status` | String(20) | DEFAULT 'active' | active, superseded, completed |
| `review_date` | Date | nullable | Fecha de revisión programada |
| `created_at` | DateTime | DEFAULT now() | Creación |

**Índices:** `idx_decisions_user_id`, `idx_decisions_status`, `idx_decisions_review_date`

---

### 10. `roadmap_items` — Items de Roadmap (EasyTech Advisor)

> Proyectos/etapas del roadmap global.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `project` | String(150) | NOT NULL | Nombre del proyecto/etapa |
| `priority` | Integer | DEFAULT 2 | 1=Alta, 2=Media, 3=Baja |
| `status` | String(20) | DEFAULT 'planned' | planned, in_progress, blocked, done |
| `next_action` | Text | nullable | Próxima acción concreta |
| `blocked_by` | Text | nullable | ¿Por qué está bloqueado? |
| `target_date` | Date | nullable | Fecha objetivo |
| `created_at` | DateTime | DEFAULT now() | Creación |
| `updated_at` | DateTime | DEFAULT now() | Última modificación |

**Índices:** `idx_roadmap_user_id`, `idx_roadmap_status`, `idx_roadmap_priority`

---

### 11. `wins` — Logros / Victorias

> Registrar avances para no perderlos psicológicamente.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincrement | Identificador |
| `user_id` | Integer | NOT NULL, FK → users.id, ON DELETE CASCADE | Propietario |
| `fecha` | Date | NOT NULL | Fecha del logro |
| `descripcion` | String(500) | NOT NULL | Descripción |
| `categoria` | String(50) | nullable | Categoría (Negocio, Personal, Cliente, etc.) |
| `impacto` | Text | nullable | Impacto del logro |
| `created_at` | DateTime | DEFAULT now() | Creación |

**Índices:** `idx_wins_user_id`, `idx_wins_fecha`, `idx_wins_categoria`

---

## MAPEO CON MODELO ANTERIOR

| Modelo Viejo | Modelo Nuevo | Acción |
|--------------|--------------|--------|
| `Goal` | `visions` | **Reemplazar** |
| `Habit` | Eliminado (fuera de MVP) | **Eliminar** |
| — | `areas` | **Agregar** |
| — | `projects` (nuevo nivel) | **Agregar** |
| `PlanDay` | `daily_focus` | **Renombrar/Extender** |
| `PlanItem` | `focus_items` | **Renombrar/Extender** |
| — | `users` | **Agregar** |
| — | `objectives` | **Agregar** |
| — | `daily_reflections` | **Agregar** |
| — | `decisions` | **Agregar** |
| — | `roadmap_items` | **Agregar** |
| — | `wins` | **Agregar** |

---

## DECISIONES DE DISEÑO

1. **Jerarquía 4 niveles:** `visions` → `areas` → `projects` → `objectives`. Permite agrupar proyectos del mismo ámbito estratégico.
2. **Denormalización `user_id`:** Presente en todas las tablas hijas para queries directos del dashboard.
3. **Soft delete:** `is_active` en entidades persistentes; estado enumerado en items operativos.
4. **Decisiones inmutables:** `decisions` registra decisiones con `review_date` para no re-discutir.
5. **Wins aislados:** `wins` no vincula a objetivos — es libre para registrar cualquier avance.

---

## RESTRICCIONES MVP

- ✅ Sí: Todas las tablas definidas arriba
- ❌ No: Tracking de hábitos diarios
- ❌ No: Notificaciones push
- ❌ No: Integración con IA real
- ❌ No: Múltiples visiones activas simultáneas
- ❌ No: Colaboración / múltiples usuarios
- ❌ No: App móvil / PWA

---

*Modelo aprobado. Listo para Sprint 1 de implementación.*