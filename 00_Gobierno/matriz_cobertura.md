# Matriz de cobertura — Easy Wiki

**Auditoría Fase 2** · junio 2026 · commit de referencia: `d8f7d9d` (pre-auditoría)

Criterios:

- **Existe:** hay al menos un `.md` en el área que cubre el tema.
- **Completo (área):** ≥ 70 % de los documentos del área en estado *Completo* o *Parcial útil*; los estratégicos del MVP no están *Vacíos*.
- **Completo (doc):** contenido operativo usable sin placeholder crítico (ver catálogo en [[00_Gobierno/auditoria_easywiki#Tarea 2 – Catálogo documental]]).

| Área | Existe | Completo | Observaciones |
|------|--------|----------|---------------|
| **Empresa** | Sí | Parcial | `easytechnology` y `servicios` sólidos; `historia` y `organigrama` breves; misión/visión/valores con pie «completar con dirección». |
| **Easy Suite** | Sí | Sí | `easy_suite`, `mapa_suite` y `naming_standards` cubren oferta y marca. |
| **Productos** | Sí | Parcial | EN1, ePosOne, EClassOne e `integrations` completos; EThesisOne y EPayRoll en visión/comercial sin piloto documentado. |
| **Clientes** | Sí | Parcial | IIUS y Modecosa completos; Rycom solo plantilla; `clientes_generales` es índice. |
| **Arquitectura** | Sí | Parcial | `arquitectura_en1` y `arquitectura_api` completos; `arquitectura_apps` y `arquitectura_ia` vacíos (placeholder). |
| **Operaciones** | Sí | Sí | Deploy, taller, soporte, QA y alta de cliente con contenido EN1 operativo. |
| **IA** | Sí | Parcial | `equipo_virtual` completo; ChatGPT/Cursor mínimos útiles; Kimi y Easy Operator casi vacíos (Operator = planeado). |
| **Marketing** | Sí | Parcial | `marketing_hub` completo; `campanas`, `redes_sociales`, `productos_promocionables` son stubs (5 líneas). |
| **Roadmap** | Sí | Parcial | `roadmap_2026` completo y alineado a Fase 1; `backlog` y `roadmap_2027` esbozo. |
| **Gobierno** | Sí | Parcial | Principios en `gobierno_tecnologico`; falta organigrama formal y políticas extendidas antes de «Gobierno Tecnológico» pleno. |
| **Proyectos** (`05_`) | Sí | Parcial | EN1 / IIUS / Modecosa con alcance; ePosOne y EPayRoll README vacíos; tablas de contacto sin rellenar. |
| **Recursos** (`99_`) | Sí | No | Solo `README` índice (11 líneas). |

## Documentos estratégicos (Tarea 3)

| Tema requerido | Archivo | Existe | Completo |
|----------------|---------|--------|----------|
| Easy Technology Services | `01_Empresa/easytechnology.md` | Sí | Sí |
| Misión | `00_Gobierno/mision.md` | Sí | Parcial |
| Visión | `00_Gobierno/vision.md` | Sí | Parcial |
| Servicios | `01_Empresa/servicios.md` | Sí | Sí |
| Easy Suite | `02_Suite/easy_suite.md` | Sí | Sí |
| Mapa general | `02_Suite/mapa_suite.md` | Sí | Sí |
| EN1 Platform | `03_Productos/en1_platform.md` | Sí | Sí |
| ePosOne | `03_Productos/eposone.md` | Sí | Sí |
| EClassOne | `03_Productos/eclassone.md` | Sí | Sí |
| EThesisOne | `03_Productos/ethesisone.md` | Sí | Parcial |
| EPayRoll | `03_Productos/epayroll.md` | Sí | Parcial |
| Modecosa | `04_Clientes/modecosa.md` | Sí | Sí |
| IIUS | `04_Clientes/iius.md` | Sí | Sí |
| Marketing Hub | `09_Marketing/marketing_hub.md` | Sí | Sí |
| ChatGPT | `08_IA/chatgpt_analista.md` | Sí | Parcial |
| Cursor | `08_IA/cursor_programador.md` | Sí | Parcial |
| Kimi | `08_IA/kimi_mobile.md` | Sí | Vacío |
| Easy Operator | `08_IA/easy_operator.md` | Sí | Vacío |
| Roadmap 2026 | `10_Roadmap/roadmap_2026.md` | Sí | Sí |

## Bloqueantes para siguientes iniciativas

| Iniciativa | Estado wiki hoy | Qué falta (sin cambiar arquitectura) |
|------------|-----------------|--------------------------------------|
| **Easy Operator** | IA + wiki indexables; Operator vacío | Política de datos, fuentes permitidas, enlaces a `00_Inicio` y proyectos; no requiere mover archivos. |
| **Marketing Hub** | Hub completo; satélites vacíos | Rellenar `campanas`, `redes_sociales`, `productos_promocionables` con aprobación marketing. |
| **Gobierno Tecnológico** | Borrador 24 líneas | Aprobar misión/visión/valores; ampliar `gobierno_tecnologico` + `organigrama`; enlazar deploy y IA. |

---

Informe completo: [[00_Gobierno/auditoria_easywiki]]
