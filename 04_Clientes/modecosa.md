# Modecosa (cliente)

**Modecosa** opera su ERP en **Odoo 19** (`erp.modecosa.com`) e integra con [[03_Productos/en1_platform|EN1]] para **catálogo de seguridad** (usuarios, grupos, permisos) sin duplicar la matriz a mano en dos sistemas.

## Qué es Modecosa (negocio)

Empresa con gestión central en Odoo que usa EN1 en el ecosistema Easy para:

- **Leer** desde Odoo el catálogo oficial de usuarios, grupos y membresías.
- **Visualizar y validar** la matriz de permisos en EN1 (importación, preview, Excel).
- **Fase futura:** aplicar cambios aprobados en Odoo desde EN1 (coordinado, otra API key).

**Importante:** los **pagos** que EN1 envía hacia Odoo (webhooks) son un flujo **distinto**; no se mezcla con el conector de catálogo de seguridad.

## Fase 1 — entregada

| Pieza | Estado |
|-------|--------|
| Módulo Odoo `en1_connector` v **19.0.1.0.0** | En producción Odoo |
| Endpoint catálogo | `GET …/api/en1/v1/security-catalog` |
| Autenticación | `Authorization: Bearer <API_KEY_SOLO_LECTURA>` + header `X-Odoo-Database: modecosa` |
| EN1 | Cliente HTTP configurado (`ODOO_CATALOG_URL`, credenciales en entorno) |
| Prueba de aceptación | ~28 usuarios, ~111 grupos, ~153 membresías, HTTP 200 |

### Qué trae el JSON del catálogo (obligatorio)

- **users**: id, login, name, active, group_ids (+ email/departamento si HR existe).
- **groups**: id, name, **xml_id** (clave para la matriz Excel).
- **memberships**: cada vínculo usuario–grupo directo.
- **critical_groups**: grupos sensibles (contabilidad manager, inventario manager, administrador, etc.).

### Qué NO hace Fase 1

- No se entregan credenciales de usuario admin de Odoo a EN1.
- No se cambian ACL, reglas ni menús desde EN1.
- No se usa XML-RPC masivo desde el servidor EN1.

## Fase 2 — planificada

Endpoint separado con **otra** API key de ejecución:

```http
POST /api/en1/v1/security-matrix/apply
```

Solo acciones `add` / `remove` de usuario en grupo (`res.groups`), con log en Odoo y **aprobación humana** en pantalla admin EN1 antes de llamar.

## Qué entregamos al cliente

| Entrega | Responsable |
|---------|-------------|
| Módulo y API en Odoo | Equipo ERP del cliente (programador Odoo) |
| Pantallas matriz / importación EN1 | Easy Technology |
| Configuración y pruebas de conexión | Easy Technology |
| Documentación de especificación | Compartida (JSON Schema + ejemplo en repo producto) |

## Cómo se explica al cliente

*«Modecosa sigue siendo dueño de permisos en Odoo. EN1 descarga el catálogo oficial por HTTPS para mostrarlo, validar Excel y, más adelante, aplicar cambios que ustedes aprueben.»*

## Módulo EN1 implicado

Código SaaS: **`security_matrix`** («Matriz de permisos Odoo»).

Relacionado: **`rbac_matrix`** para la permisología nativa de EN1 (roles del tenant).

## Proyecto interno wiki

[[05_Proyectos/modecosa/README]] — contactos, hitos, notas de reunión.

## Integraciones

[[03_Productos/integrations]] · [[06_Arquitectura/arquitectura_api]]

## Roadmap

Evolución Fase 2 y mejoras de matriz: [[10_Roadmap/roadmap_2026]]

---

**Otros clientes:** [[04_Clientes/iius]] · [[04_Clientes/rycom]]
