# Auditoría Easy Wiki — Fase 2

**Proyecto:** Easy Wiki — Auditoría y consolidación  
**Empresa:** Easy Technology Services  
**Fecha:** junio 2026  
**Repositorio:** `git@github.com:shidalgo0925/EasyWiki.git`  
**Ruta servidor:** `/opt/easynodeone/dev/EasyWiki`  
**Commit auditado:** `d8f7d9d` (rama `main`)  
**Alcance:** inventario y estado; **sin** mover, borrar, renombrar ni editar documentos preexistentes.

---

## Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Archivos `.md` (total al auditar) | **52** (incluye `README.md` raíz) → **54** tras esta auditoría (+2) |
| Carpetas de contenido | **12** (`00` … `10`, `99`) |
| Subcarpetas en `05_Proyectos` | **5** |
| Líneas Markdown (aprox.) | **~1.730** |
| Documentos *Completo* | **22** |
| Documentos *Parcial* | **24** |
| Documentos *Vacío* | **7** |
| Documentos estratégicos Tarea 3 | **18/18 existen** · **12 completos** · **4 parciales** · **2 vacíos** |

**Conclusión:** la Fase 1 MVP **está desplegada y en Git**. La wiki es usable en Obsidian para EN1, IIUS, Modecosa, operaciones y marketing central. Los vacíos concentran **gobierno formal**, **marketing satélite**, **IA Kimi/Operator**, **arquitectura apps/IA**, **Rycom** y **proyectos POS/nómina**. El detalle técnico de EN1 **debe seguir** en `Easy-NodeOne/backend/docs/` (no duplicar).

Matriz resumida: [[00_Gobierno/matriz_cobertura]]

---

## Tarea 1 – Inventario completo

### Árbol del repositorio (equivalente `tree -L 3`)

```text
EasyWiki/
├── README.md
├── 00_Inicio.md
├── 00_Gobierno/                    [4 docs + esta auditoría]
│   ├── gobierno_tecnologico.md
│   ├── mision.md
│   ├── valores.md
│   └── vision.md
├── 01_Empresa/                     [4 docs]
│   ├── easytechnology.md
│   ├── historia.md
│   ├── organigrama.md
│   └── servicios.md
├── 02_Suite/                       [3 docs]
│   ├── easy_suite.md
│   ├── mapa_suite.md
│   └── naming_standards.md
├── 03_Productos/                   [6 docs]
│   ├── eclassone.md
│   ├── en1_platform.md
│   ├── epayroll.md
│   ├── eposone.md
│   ├── ethesisone.md
│   └── integrations.md
├── 04_Clientes/                    [4 docs]
│   ├── clientes_generales.md
│   ├── iius.md
│   ├── modecosa.md
│   └── rycom.md
├── 05_Proyectos/                   [1 + 5 subcarpetas]
│   ├── README.md
│   ├── en1/README.md
│   ├── epayroll/README.md
│   ├── eposone/README.md
│   ├── iius/README.md
│   └── modecosa/README.md
├── 06_Arquitectura/                [4 docs]
│   ├── arquitectura_api.md
│   ├── arquitectura_apps.md
│   ├── arquitectura_en1.md
│   └── arquitectura_ia.md
├── 07_Operaciones/                 [6 docs]
│   ├── crear_cliente.md
│   ├── crear_proyecto.md
│   ├── deploy.md
│   ├── modulo_taller.md
│   ├── qa.md
│   └── soporte.md
├── 08_IA/                          [5 docs]
│   ├── chatgpt_analista.md
│   ├── cursor_programador.md
│   ├── easy_operator.md
│   ├── equipo_virtual.md
│   └── kimi_mobile.md
├── 09_Marketing/                   [4 docs]
│   ├── campanas.md
│   ├── marketing_hub.md
│   ├── productos_promocionables.md
│   └── redes_sociales.md
├── 10_Roadmap/                     [3 docs]
│   ├── backlog.md
│   ├── roadmap_2026.md
│   └── roadmap_2027.md
└── 99_Recursos/                    [1 doc]
    └── README.md
```

### Resumen por carpeta

| Carpeta | Subcarpetas | Archivos `.md` | Rol |
|---------|-------------|----------------|-----|
| *(raíz)* | — | 2 | Índice Git + inicio wiki |
| `00_Gobierno` | — | 4 (+2 auditoría) | Misión, visión, valores, gobierno |
| `01_Empresa` | — | 4 | Identidad y servicios |
| `02_Suite` | — | 3 | Oferta y mapa |
| `03_Productos` | — | 6 | Fichas de producto |
| `04_Clientes` | — | 4 | Fichas cliente |
| `05_Proyectos` | 5 | 6 | Notas de proyecto |
| `06_Arquitectura` | — | 4 | EN1 e integraciones |
| `07_Operaciones` | — | 6 | Deploy, soporte, taller |
| `08_IA` | — | 5 | Equipo virtual |
| `09_Marketing` | — | 4 | Hub y canales |
| `10_Roadmap` | — | 3 | Planificación |
| `99_Recursos` | — | 1 | Enlaces y plantillas |
| **Total** | **5** | **52** (+2 auditoría = **54**) | |

---

## Tarea 2 – Catálogo documental

### Criterios de estado

| Estado | Regla aplicada |
|--------|----------------|
| **Completo** | ≥ 35 líneas útiles **o** cubre MVP/operación sin depender de «completar» crítico; listo para consulta. |
| **Parcial** | Estructura y contenido útil, pero placeholders, &lt; 35 líneas, o falta aprobación formal / datos de contacto. |
| **Vacío** | ≤ 5 líneas **o** solo placeholder / «añadir aquí». |

### Catálogo (documentos preexistentes al cierre de auditoría)

| Documento | Categoría | Líneas | Estado |
|-----------|-----------|--------|--------|
| `README.md` | Índice / Repo | 50 | Completo |
| `00_Inicio.md` | Índice | 34 | Completo |
| `00_Gobierno/gobierno_tecnologico.md` | Gobierno | 24 | Parcial |
| `00_Gobierno/mision.md` | Gobierno | 13 | Parcial |
| `00_Gobierno/valores.md` | Gobierno | 13 | Parcial |
| `00_Gobierno/vision.md` | Gobierno | 17 | Parcial |
| `01_Empresa/easytechnology.md` | Empresa | 48 | Completo |
| `01_Empresa/historia.md` | Empresa | 17 | Parcial |
| `01_Empresa/organigrama.md` | Empresa | 15 | Parcial |
| `01_Empresa/servicios.md` | Empresa | 17 | Completo |
| `02_Suite/easy_suite.md` | Suite | 40 | Completo |
| `02_Suite/mapa_suite.md` | Suite | 60 | Completo |
| `02_Suite/naming_standards.md` | Suite | 23 | Parcial |
| `03_Productos/en1_platform.md` | Producto | 109 | Completo |
| `03_Productos/eposone.md` | Producto | 42 | Completo |
| `03_Productos/eclassone.md` | Producto | 37 | Completo |
| `03_Productos/ethesisone.md` | Producto | 31 | Parcial |
| `03_Productos/epayroll.md` | Producto | 29 | Parcial |
| `03_Productos/integrations.md` | Producto / Arquitectura | 52 | Completo |
| `04_Clientes/iius.md` | Cliente | 82 | Completo |
| `04_Clientes/modecosa.md` | Cliente | 81 | Completo |
| `04_Clientes/rycom.md` | Cliente | 17 | Parcial |
| `04_Clientes/clientes_generales.md` | Cliente | 27 | Parcial |
| `05_Proyectos/README.md` | Proyecto | 13 | Parcial |
| `05_Proyectos/en1/README.md` | Proyecto | 32 | Parcial |
| `05_Proyectos/iius/README.md` | Proyecto | 42 | Parcial |
| `05_Proyectos/modecosa/README.md` | Proyecto | 42 | Parcial |
| `05_Proyectos/eposone/README.md` | Proyecto | 5 | Vacío |
| `05_Proyectos/epayroll/README.md` | Proyecto | 5 | Vacío |
| `06_Arquitectura/arquitectura_en1.md` | Arquitectura | 101 | Completo |
| `06_Arquitectura/arquitectura_api.md` | Arquitectura | 54 | Completo |
| `06_Arquitectura/arquitectura_apps.md` | Arquitectura | 3 | Vacío |
| `06_Arquitectura/arquitectura_ia.md` | Arquitectura | 5 | Vacío |
| `07_Operaciones/deploy.md` | Operación | 85 | Completo |
| `07_Operaciones/modulo_taller.md` | Operación | 67 | Completo |
| `07_Operaciones/soporte.md` | Operación | 44 | Completo |
| `07_Operaciones/qa.md` | Operación | 46 | Completo |
| `07_Operaciones/crear_cliente.md` | Operación | 40 | Completo |
| `07_Operaciones/crear_proyecto.md` | Operación | 7 | Parcial |
| `08_IA/equipo_virtual.md` | IA | 50 | Completo |
| `08_IA/chatgpt_analista.md` | IA | 17 | Parcial |
| `08_IA/cursor_programador.md` | IA | 24 | Parcial |
| `08_IA/kimi_mobile.md` | IA | 3 | Vacío |
| `08_IA/easy_operator.md` | IA | 5 | Vacío |
| `09_Marketing/marketing_hub.md` | Marketing | 49 | Completo |
| `09_Marketing/campanas.md` | Marketing | 5 | Vacío |
| `09_Marketing/redes_sociales.md` | Marketing | 5 | Vacío |
| `09_Marketing/productos_promocionables.md` | Marketing | 5 | Vacío |
| `10_Roadmap/roadmap_2026.md` | Roadmap | 54 | Completo |
| `10_Roadmap/roadmap_2027.md` | Roadmap | 7 | Parcial |
| `10_Roadmap/backlog.md` | Roadmap | 11 | Parcial |
| `99_Recursos/README.md` | Recursos | 11 | Parcial |

### Documentos añadidos por esta auditoría (autorizados)

| Documento | Categoría | Estado |
|-----------|-----------|--------|
| `00_Gobierno/auditoria_easywiki.md` | Gobierno / Auditoría | Completo |
| `00_Gobierno/matriz_cobertura.md` | Gobierno / Auditoría | Completo |

---

## Tarea 3 – Validación documentos estratégicos

| # | Tema | Archivo | Existe | Contenido mínimo | Estado |
|---|------|---------|--------|------------------|--------|
| 1 | Easy Technology Services | `01_Empresa/easytechnology.md` | Sí | Qué hace, líneas de negocio, forma de trabajo | **Completo** |
| 2 | Misión | `00_Gobierno/mision.md` | Sí | Enunciado + 3 pilares; pie «completar con dirección» | **Parcial** |
| 3 | Visión | `00_Gobierno/vision.md` | Sí | Horizonte LATAM + suite; pie formal pendiente | **Parcial** |
| 4 | Servicios | `01_Empresa/servicios.md` | Sí | Tabla implementación → soporte | **Completo** |
| 5 | Easy Suite | `02_Suite/easy_suite.md` | Sí | Tabla productos + idea modular | **Completo** |
| 6 | Mapa general | `02_Suite/mapa_suite.md` | Sí | Diagrama ASCII + tabla por tipo cliente | **Completo** |
| 7 | EN1 Platform | `03_Productos/en1_platform.md` | Sí | Módulos SaaS, pagos, clientes ref. | **Completo** |
| 8 | ePosOne | `03_Productos/eposone.md` | Sí | POS, audiencia, relación EN1 | **Completo** |
| 9 | EClassOne | `03_Productos/eclassone.md` | Sí | Campus / EN1 academic | **Completo** |
| 10 | EThesisOne | `03_Productos/ethesisone.md` | Sí | Visión; sin piloto en `05_Proyectos` | **Parcial** |
| 11 | EPayRoll | `03_Productos/epayroll.md` | Sí | Visión; sin piloto en `05_Proyectos` | **Parcial** |
| 12 | Modecosa | `04_Clientes/modecosa.md` | Sí | Odoo Fase 1/2, API, módulo EN1 | **Completo** |
| 13 | IIUS | `04_Clientes/iius.md` | Sí | Campus cerrado, matrícula, flujo | **Completo** |
| 14 | Marketing Hub | `09_Marketing/marketing_hub.md` | Sí | Mensaje, pitches, audiencias | **Completo** |
| 15 | ChatGPT | `08_IA/chatgpt_analista.md` | Sí | Rol y límites | **Parcial** |
| 16 | Cursor | `08_IA/cursor_programador.md` | Sí | Rol, reglas dev/deploy | **Parcial** |
| 17 | Kimi | `08_IA/kimi_mobile.md` | Sí | 1 párrafo | **Vacío** |
| 18 | Easy Operator | `08_IA/easy_operator.md` | Sí | 3 líneas «planeado» | **Vacío** |
| 19 | Roadmap 2026 | `10_Roadmap/roadmap_2026.md` | Sí | Q1–Q4, wiki, EN1, IIUS, Modecosa | **Completo** |

**No faltan archivos** de la lista estratégica. Sí faltan **contenidos** en Kimi, Easy Operator y piezas de gobierno/marketing.

---

## Tarea 4 – Matriz de cobertura

Ver archivo dedicado (sin duplicar tablas): [[00_Gobierno/matriz_cobertura]]

---

## Tarea 5 – Identificación de vacíos

### 1. Documentos faltantes (temas sin archivo dedicado)

| Tema sugerido | Prioridad | Nota |
|---------------|-----------|------|
| Índice único «Productos» (además de `mapa_suite`) | Baja | Opcional; `mapa_suite` ya cumple. |
| Ficha **Rycom** completa | Media | Hoy solo plantilla en `04_Clientes/rycom.md`. |
| `05_Proyectos/rycom/` | Baja | No existe carpeta. |
| Política de datos / secretos para IA | Alta (pre-Operator) | Puede vivir en `08_IA` o ampliar `gobierno_tecnologico`. |
| Comunicado «Novedades EN1» para clientes (resumen) | Media | Existe en repo EN1, **no** en wiki (ver restricción no copiar). Enlace desde `99_Recursos` sería suficiente. |

### 2. Documentos duplicados

| Tipo | Detalle | Acción recomendada |
|------|---------|-------------------|
| **Nombres duplicados** | Ninguno | — |
| **Contenido solapado** | `04_Clientes/iius.md` ↔ `05_Proyectos/iius/README.md` | **Mantener:** ficha comercial vs. operación interna (no es duplicado inválido). |
| **Contenido solapado** | `03_Productos/en1_platform.md` ↔ `06_Arquitectura/arquitectura_en1.md` | **Mantener:** producto vs. arquitectura (audiencias distintas). |
| **Contenido solapado** | `09_Marketing/marketing_hub.md` ↔ tabla en `productos_promocionables.md` | **Ampliar** satélite cuando marketing apruebe; hoy el stub no duplica el hub. |

### 3. Documentos obsoletos

| Documento | Veredicto |
|-----------|-----------|
| Ninguno marcado obsoleto | Los pies «*Completar*» indican **borrador**, no retiro. |
| `10_Roadmap/roadmap_2027.md` | Esbozo intencional (7 líneas), no obsoleto. |

### 4. Documentos técnicos que deben permanecer solo en EN1 Docs

Repositorio: `/opt/easynodeone/dev/app/backend/docs/` (Easy-NodeOne). **No copiar** a Easy Wiki.

| Archivo EN1 | Motivo |
|-------------|--------|
| `EN1_ARCHITECTURE.md` | Capas, rutas código, mermaid técnico |
| `EN1_MODELS.md` | ORM y tablas |
| `EN1_ROUTES.md` | Inventario endpoints |
| `EN1_SAAS_GUARDS.md` | Implementación guards |
| `EN1_API_CONTRACT.md` | Contratos API |
| `FLUTTER_SYNC.md` | Sincronización móvil |
| `EN1_OPERACIONES_TALLER.md` | Manual L2 con rutas `/api/workshop` |
| `EN1_NUEVAS_FUNCIONALIDADES_Y_CORRECCIONES.md` | Changelog técnico |
| `ODOO_MODULO_EN1_ESPECIFICACION.md` | Spec JSON Schema |
| `EN1_ODOO_CATALOG_CONFIG.md` | Variables entorno |
| `INSTRUCCION_PROGRAMADOR_ODOO.md` | Handoff técnico Odoo |
| `EN1_IIUS_ACADEMIC_CLOSED.md` | Scripts Python y SQL |
| `IIUS_*` (8 archivos) | Runbooks, PayPal, QA, handoff |
| `ETAPA1_*`, `ETAPA2_*` | Checklists migración |
| `BITACORA_CAMBIOS_PLATAFORMAS.md` | Bitácora infra |

### 5. Documentos que ya están resumidos en Easy Wiki (correcto)

| Fuente EN1 (referencia) | Resumen en Easy Wiki |
|-------------------------|----------------------|
| `saas_catalog_defaults` / guards | `03_Productos/en1_platform.md` (tabla módulos) |
| `EN1_IIUS_ACADEMIC_CLOSED.md` | `04_Clientes/iius.md` |
| `INSTRUCCION_PROGRAMADOR_ODOO.md` | `04_Clientes/modecosa.md` |
| `EN1_OPERACIONES_TALLER.md` | `07_Operaciones/modulo_taller.md` |
| Política Git / deploy | `07_Operaciones/deploy.md` |
| `EN1_ARCHITECTURE.md` (alto nivel) | `06_Arquitectura/arquitectura_en1.md` |

### 6. Candidatos a resumir en wiki (fase posterior, con aprobación)

| Fuente EN1 | Propuesta wiki | Formato |
|------------|----------------|---------|
| `EN1_NOVEDADES_PARA_CLIENTE.md` | Enlace en `99_Recursos` o 1 página «Novedades cliente» | Resumen ejecutivo, no volcado |
| `EN1_NOVEDADES` / comunicados trimestrales | `09_Marketing/` | Versión marketing |
| Checklist deploy cliente | Ampliar `07_Operaciones/deploy.md` | Solo pasos visibles al cliente |

---

## Recomendaciones de mejora (sin cambiar arquitectura)

Prioridad alineada al objetivo: **Easy Operator**, **Marketing Hub** y **Gobierno Tecnológico**.

### Prioridad alta (antes de Easy Operator)

1. **Aprobar** misión, visión y valores en `00_Gobierno/` (sustituir pies «completar con dirección»).
2. **Ampliar** `00_Gobierno/gobierno_tecnologico.md`: política de datos, IA, acceso a repos (sin mover archivos).
3. **Definir** en `08_IA/easy_operator.md` alcance MVP: qué lee (wiki + ¿Git?), qué no (secretos, prod).
4. **Enlace** en `99_Recursos/README.md` al repo EN1 para docs técnicos (URL interna acordada).

### Prioridad media (Marketing Hub operativo)

5. Rellenar `09_Marketing/campanas.md`, `redes_sociales.md`, `productos_promocionables.md` (contenido aprobado por marketing).
6. Completar **Rycom** en `04_Clientes/rycom.md` + carpeta `05_Proyectos/rycom/` si aplica contrato.
7. Rellenar tablas de **contacto/URL** en `05_Proyectos/iius`, `modecosa`, `en1` (datos solo humanos).

### Prioridad media-baja (productos y arquitectura)

8. `06_Arquitectura/arquitectura_apps.md` — stack ePosOne / Flutter (resumen, no spec API).
9. `06_Arquitectura/arquitectura_ia.md` — flujo equipo virtual + futuro Operator.
10. `05_Proyectos/eposone`, `epayroll` — cuando exista piloto comercial.
11. `07_Operaciones/crear_proyecto.md` — ampliar checklist (hoy 7 líneas).

### Prioridad baja

12. `01_Empresa/historia.md`, `organigrama.md` — datos institucionales.
13. `08_IA/kimi_mobile.md` — política de uso o marcar «no adoptado».
14. Publicación estática de wiki (roadmap Q4 2026).

### Qué no hacer (restricciones confirmadas)

- No mover ni renombrar carpetas `00`–`99`.
- No copiar `backend/docs` → Easy Wiki.
- No editar contenido existente sin aprobación explícita (esta auditoría solo **añade** estos dos archivos en `00_Gobierno/`).

---

## Estado para iniciativas posteriores

| Iniciativa | ¿Listo para arrancar? | Condición |
|------------|----------------------|-----------|
| **Easy Wiki Fase 2 contenido** | Sí (con plan) | Matriz y vacíos definidos; ampliar por área con aprobación. |
| **Marketing Hub** | Parcial | Hub listo; ejecutar campañas en archivos satélite. |
| **Gobierno Tecnológico** | No pleno | Falta gobierno formal + organigrama. |
| **Easy Operator** | No | Definir política y fuentes; archivos Operator/Kimi vacíos. |

---

## Control de cambios de esta auditoría

| Acción | Archivos |
|--------|----------|
| Creados | `00_Gobierno/auditoria_easywiki.md`, `00_Gobierno/matriz_cobertura.md` |
| Modificados | Ninguno (preexistente) |
| Eliminados | Ninguno |

---

*Easy Technology Services — auditoría interna Fase 2. Próximo paso sugerido: `git commit` + `git push` en EasyWiki tras revisión de dirección.*
