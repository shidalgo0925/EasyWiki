# Roadmap 2026 — Easy Technology Services

**Estado:** Operativo — actualización junio 2026  
**Dueño:** Dirección Tecnológica  
**Revisión:** Trimestral

---

## Contexto Ejecutivo

IIUS se encuentra aproximadamente al **92% de avance**.

La prioridad inmediata continúa siendo:

1. **Cierre Modecosa**
2. **Cierre IIUS**
3. **Estabilización EN1**

> **Restricción crítica:** No se autoriza iniciar desarrollo de mejoras del backlog estratégico hasta finalizar las prioridades anteriores.

---

## Estado Actual de Prioridades

### PRIORIDAD 1 — MODECOSA

| | |
|---|---|
| **Objetivo** | Cierre operativo definitivo |
| **Estado** | EN PROCESO |

**Pendientes:**

- [ ] NCR Facturación Electrónica
- [ ] Validación reversas NCR
- [ ] Apertura sucursal El Roble
- [ ] Validación facturación sucursal
- [ ] Reportes contables pendientes
- [ ] Cierre operativo

---

### PRIORIDAD 2 — IIUS

| | |
|---|---|
| **Objetivo** | Entrega operativa completa |
| **Estado** | EN PROCESO |

**Pendientes:**

- [ ] QA final
- [ ] Catálogo académico
- [ ] Pagos
- [ ] Accesos
- [ ] Ajustes visuales
- [ ] Cierre funcional restante (~8%)

---

### PRIORIDAD 3 — EN1 COMERCIAL

| | |
|---|---|
| **Objetivo** | Convertir EN1 en una plataforma comercial multi-producto |
| **Estado** | PLANIFICADO |

**Incluye:**

- Landing comercial
- Checkout
- CRM
- Facturación
- Integración de productos

---

### PRIORIDAD 5 — EasyCoach

| | |
|---|---|
| **Objetivo** | Transformar 1% Better Every Day en una plataforma de coaching personal con IA |
| **Estado** | **EN DESARROLLO** — MVP estabilización, Caso 0 activo (Seul) |
| **Branch código** | `feature/mvp-stabilization` en EasyWiki |
| **Último hito** | Capa IA interactiva, actividades guiadas, tratamiento (2026-06-10) |

**Fases completadas:**

1. ✅ MVP base (plan diario, cierre, decisiones, roadmap)
2. ✅ Google Calendar real
3. ✅ IA real (OpenAI + multi-proveedor)
4. ✅ Coaching guiado (actividades paso a paso, Coach ahora, chat flotante)
5. ✅ Tratamiento activo + memoria de conversación

**Siguiente:**

- Fase 8: agenda en contexto, resúmenes diario/semanal, Daily Brief

**Responsable:** Programador JR + Seul (validación)

**Documentación:** [[05_Proyectos/EasyCoach/EasyCoach]] · [[05_Proyectos/EasyCoach/Coach_IA_Implementacion]]

---

## BACKLOG ESTRATÉGICO

| Iniciativa | Estado | Prioridad | Dependencias | Documento |
|------------|--------|-----------|--------------|-----------|
| **EN1 Navigation & Commerce Hub** | BACKLOG APROBADO | MEDIA | Finalización Modecosa, IIUS y estabilización EN1 | [[10_Roadmap/en1_navigation_commerce_hub]] |
| **EPayRoll** | PENDIENTE | BAJA | Estabilización EN1 | *(por crear)* |
| **Marketing Hub** | PENDIENTE | BAJA | Estabilización EN1 | *(por crear)* |
| **EasyAgents** | PENDIENTE | BAJA | Estabilización EN1 | *(por crear)* |
| **Gobierno Tecnológico** | PENDIENTE | BAJA | Estabilización EN1 | *(por crear)* |
| **EasyCoach** | **EN DESARROLLO** | **ALTA** | Caso 0 activo | [[05_Proyectos/EasyCoach/EasyCoach]] |

---

## Estructura del Roadmap

```
10_Roadmap/
│
├── roadmap_2026.md              ← Este documento (maestro)
├── roadmap_2027.md              ← Visión futura
├── backlog.md                   ← Ideas no comprometidas
│
├── en1_navigation_commerce_hub.md  ← Iniciativa estratégica #1
├── epayroll_roadmap.md           ← Iniciativa estratégica #2 (pendiente)
├── marketing_hub.md              ← Iniciativa estratégica #3 (pendiente)
├── easyagents.md                 ← Iniciativa estratégica #4 (pendiente)
├── gobierno_tecnologico.md       ← Iniciativa estratégica #5 (pendiente)
└── easycoach.md                  ← Iniciativa estratégica #6 (pendiente)
```

> **Nota arquitectural:** Cada iniciativa estratégica tiene su propio documento para mantener el roadmap maestro limpio y preparar EasyWiki como fuente oficial de conocimiento para futuros agentes IA.

---

## Fases del Año

### Q1–Q2 2026 (en curso / reciente)

| Prioridad | Tema | Resultado esperado |
|-----------|------|-------------------|
| Alta | **EN1 — ERP y operación** | Menú Odoo, contactos, pagos Yappy, taller SLA, eventos/certificados desplegados en clientes. |
| Alta | **Easy Wiki MVP** | 10+ documentos + estructura; repo Git; flujo de actualización. |
| Alta | **Estabilidad prod** | Deploy con migraciones; sin pérdida de datos cliente. |
| Media | **IIUS / campus** | Programas en BD, campus cerrado, pagos alineados (92%). |
| Media | **Modecosa / Odoo** | Catálogo seguridad v1 operativo; FE en progreso. |
| Media | **Factura electrónica PA** | Fase A en clientes que contraten FE. |

### Q3 2026 (planificado)

| Prioridad | Tema |
|-----------|------|
| Media | Ampliar **ePosOne** (ficha comercial + pilotos). |
| Media | **Easy Wiki** fase 2: proyectos y operaciones completos. |
| Media | **Marketing** campañas coordinadas ([[09_Marketing/campanas]]). |
| Baja | **Easy Operator** (IA) — prototipo interno ([[08_IA/easy_operator]]). |

### Q4 2026 (visión)

| Prioridad | Tema |
|-----------|------|
| Media | Publicación wiki (sitio estático o intranet). |
| Media | **EPayRoll** / **EThesisOne** — según demanda comercial. |
| Baja | Integraciones adicionales ([[03_Productos/integrations]]). |

---

## Gobierno del Roadmap

| Rol | Responsabilidad |
|-----|-----------------|
| Dirección | Aprueba prioridades y backlog estratégico |
| Producto | Define alcance y dependencias por iniciativa |
| Desarrollo | Ejecuta sprints alineados a filas "Alta" |
| Operaciones | Valida cierres en clientes antes de mover prioridad |
| Cliente | Solo se comunican ítems **cerrados y desplegados** |

---

**Mapa de productos:** [[02_Suite/mapa_suite]] · **Backlog:** [[10_Roadmap/backlog]] · **2027:** [[10_Roadmap/roadmap_2027]]