# EThesisOne

**EThesisOne** es el producto de [[02_Suite/easy_suite|Easy Suite]] orientado a **flujos académicos de investigación y tesis**: protocolos, revisiones, entregas y trazabilidad entre alumno, tutor y comité.

## Estado en suite

Producto de marca **Easy Suite** con **implementación desplegada en CODITO** (jun 2026) en modo **laboratorio / demo operativa** — no es el mismo paquete comercial cerrado que IIUS/campus EN1.

## Presencia en CODITO (jun 2026)

| Campo | Valor |
|-------|-------|
| Ruta | `/opt/easythesis/app` |
| Repo | `github.com/shidalgo0925/Ethesis` · rama `main` |
| BD | `easythesis_dev` |
| Dominios | `ethesis.site`, `ethesis.etsrv.site` |
| Servicio | `easythesis-dev.service` (Gunicorn :9201) |

Detalle: [[02_Suite/inventario_easy_suite]] · handoff EN1: `/opt/handoff-plataformas/`.

## Para qué sirve (visión)

| Necesidad | Solución |
|-----------|----------|
| Institución con posgrado / tesis | Workflow de estados (borrador → revisión → aprobación) |
| Trazabilidad | Historial de versiones y comentarios del tutor |
| Coherencia | Misma identidad de usuario que [[03_Productos/en1_platform|EN1]] o [[03_Productos/eclassone|EClassOne]] |

## Relación con EN1

Cuando el cliente ya usa EN1, EThesisOne puede apoyarse en:

- Usuarios y organizaciones existentes.
- Módulo `academic` o extensiones a medida.
- Permisos RBAC del tenant.

## Próximos pasos comerciales

Definir alcance en `05_Proyectos/` cuando haya cliente piloto. Prioridad en [[10_Roadmap/roadmap_2026]].

---

**Mapa:** [[02_Suite/mapa_suite]]
