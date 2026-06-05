# Modecosa (cliente)

**Modecosa** es un cliente de [[01_Empresa/easytechnology|Easy Technology Services]] con **ERP Odoo** en `erp.modecosa.com`, integrado con [[03_Productos/en1_platform|EN1]] para catálogo de **matriz de seguridad** y permisos (conector EN1 ↔ Odoo).

## Qué es Modecosa (negocio)

Empresa que opera su gestión en **Odoo 19** y utiliza EN1 como pieza del ecosistema Easy para:

- Sincronizar / consultar **catálogo de seguridad** (roles, permisos, módulos).  
- Alinear permisología entre Odoo y la plataforma EN1.  
- Mantener **una fuente maestra** en Odoo con exposición vía API hacia EN1.

## Qué entregamos

| Entrega | Descripción |
|---------|-------------|
| Módulo Odoo `en1_connector` | API REST de catálogo de seguridad. |
| Configuración EN1 | Cliente HTTP hacia Odoo (`ODOO_CATALOG_URL`, credenciales). |
| Admin EN1 | Pantallas de matriz de seguridad importada / sincronizada. |
| Soporte conjunto | Coordinación Odoo (cliente) + EN1 (Easy Technology). |

## Cómo se explica al cliente

“Modecosa sigue trabajando en Odoo; EN1 lee el catálogo de seguridad oficial desde Odoo para no duplicar permisos a mano.”

## Proyecto interno

`05_Proyectos/modecosa/`

## Integraciones

Ver [[03_Productos/integrations]] y arquitectura `06_Arquitectura/arquitectura_api.md` *(ampliar).*

## Estado

Fase 1 del conector **implementada** (catálogo v1). Evoluciones en [[10_Roadmap/roadmap_2026]].

---

**Otros clientes:** [[04_Clientes/iius]] · [[04_Clientes/rycom]]
