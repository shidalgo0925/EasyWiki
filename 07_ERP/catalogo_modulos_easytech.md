# Catálogo de Módulos EasyTech

| Campo | Valor |
|---|---|
| **Servidor referencia** | TAMAL — `/opt/odoo/custom-addons/` |
| **Fecha inventario** | 2026-06-04 |
| **Total directorios top-level** | 48 (incluye colecciones OCA, backups, terceros) |

---

## Módulos propios EasyTech

### Facturación y documentos

| Módulo | Versión | Autor | Función | Cliente / BD | Estado disco | Estado BD |
|---|---|---|---|---|---|---|
| **FE_HKA_OCI** | 18.0.1.1.0 | Easytech Services | FE Panamá — The Factory HKA (CUFE, XML, PDF, anulación) | SMRC, Sanadb, TTTourism | Producción | Instalado (3 BD) |
| **Fact_Asp_Ebi** | 18.0.1.0.0 | Easy Technology Services | FE alternativa gateway ASP/EBI | — | En disco | No instalado |
| **invoice_import_center** | 2.0 | Easy Technology Services | Centro importación facturas Excel/CSV (pandas) | — | En disco | No instalado |
| **invoice_import_massive** | 1.0.0 | Easy Technology Services | Importación masiva con validación y creación clientes/productos | La Huaca | En disco | Instalado |
| **carga_factura_automatizada** | 1.0 | TuNombre* | Carga automatizada desde carpeta/XLS | — | En disco | No instalado |
| **simple_invoice_import** | — | — | Importación simple | — | **Directorio vacío** | — |
| **cuentas_por_cobrar** | 1.0 | — | Reporte estado de cuenta / cuentas por cobrar | — | En disco | No instalado |

\* Autor pendiente de normalizar en manifest.

### Operaciones y verticals

| Módulo | Versión | Autor | Función | Cliente / BD | Estado disco | Estado BD |
|---|---|---|---|---|---|---|
| **repair_workshop** | 1.0 | — | Taller reparación joyería (órdenes, mail) | — | En disco | No instalado |
| **whatsapp_center** | 1.0 | Easy Tech Services | Centro mensajes WhatsApp integrado Odoo | — | En disco | No instalado |
| **corredor_fields** | 1.0 | — | Campos personalizados corredor en contactos | — | En disco | No instalado |
| **charlie_shopbot** | 1.0 | Easy Tech Services | Tienda web + asistente Charlie Pity | — | En disco | No instalado |
| **contact_report_list** | 1.0 | EasyTech Services | Listado de contactos en PDF | — | En disco | No instalado |

### Módulos buscados — no encontrados

| Módulo | Resultado |
|---|---|
| `easytech_check_expense_reason` | **Ausente** en TAMAL |
| Educación (custom) | **Ausente** |
| Eventos (custom) | **Ausente** — solo `event` estándar Odoo |
| Membresías (custom) | **Ausente** — solo `membership` estándar Odoo |

---

## Módulos instalados en BD sin código en disco

**Deuda técnica crítica** — presentes en `ir_module_module` pero ausentes en filesystem:

| Módulo | BD | Autor en BD | Función inferida |
|---|---|---|---|
| `ets_weasy_sale_quote` | Easydb, TTTourism | Easy Tech | Cotizaciones venta (Weasy) |
| `contacto_consecutivo` | lahuaca | — | Consecutivos en contactos |
| `relatic_integration` | relatic | Relatic | Integración específica Relatic |

**Riesgo:** actualización de módulos, clonación de servidor o `-u all` puede fallar.

---

## Repositorios Git confirmados

| Módulo | Remote |
|---|---|
| FE_HKA_OCI (dev copy) | `git@github-fe-hka:shidalgo0925/FE_HKA_OCI.git` |
| FE_HKA_OCI (producción) | Mismo repo esperado en `/opt/odoo/custom-addons/FE_HKA_OCI` |

Otros módulos EasyTech: **sin repositorio git remoto confirmado** en TAMAL.

---

## Copias y backups de código

| Artefacto | Fecha | Ubicación |
|---|---|---|
| Tar custom modules | 2025-10-20 | `/home/admin/odoo18_custom_modules_20251020_021812.tar.gz` |
| FE_HKA_OCI backup | 2026-03-06 | `/home/admin/FE_HKA_OCI_backup_20260306/` |
| FE_HKA_OCI dev (más nuevo) | 2026-03+ | `/home/admin/FE_HKA_OCI/` v18.0.1.2.0 — **no sincronizado a producción** |
| FE_HKA_OCI.bak en addons | 2026-03-11 | `/opt/odoo/custom-addons/FE_HKA_OCI.bak.20260311/` |

---

## Matriz módulo EasyTech × base de datos

| Módulo | Easydb | lahuaca | SMRC | Sanadb | TTTourism | relatic |
|---|---|---|---|---|---|---|
| FE_HKA_OCI | — | — | ✅ | ✅ | ✅ | — |
| invoice_import_massive | — | ✅ | — | — | — | — |
| ets_weasy_sale_quote | ✅* | — | — | — | ✅* | — |
| contacto_consecutivo | — | ✅* | — | — | — | — |
| relatic_integration | — | — | — | — | — | ✅* |
| muk_web_* (tema) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

\* Código ausente en disco.

---

## Módulos terceros relevantes (no EasyTech)

| Proveedor | Módulos | Uso |
|---|---|---|
| MuK IT | `muk_web_*` (5) | Tema backend — todos los clientes |
| Odoo Mates | `om_*` (7+) | Contabilidad community |
| Cybrosys | `base_accounting_kit`, `base_account_budget` | Contabilidad |
| OCA | `web/*` (30+) | Widgets y UX web |
| Odoo SA / estándar | `account`, `sale`, `stock`, `repair`, etc. | Core funcional |

---

## Líneas de producto FE

| Línea | Módulo | Proveedor autorizado | Estado |
|---|---|---|---|
| FE_odoo18 (HKA) | `FE_HKA_OCI` | The Factory HKA | **Producción** — 3 clientes |
| FE_odoo18 (ASP/EBI) | `Fact_Asp_Ebi` | ASP/EBI Gateway | Desarrollado, no desplegado |
| FE_odoo19 | — | — | **No existe aún** |

---

## Conocimiento a preservar

1. Diferencia versiones FE en disco (1.1.0) vs dev (1.2.0)
2. Dependencias Python: `requests`, `PyJWT` (FE_HKA); `pandas`, `openpyxl` (importación)
3. Módulos huérfanos y plan de recuperación de código
4. Qué módulo va a qué cliente (matriz arriba)
5. Módulos en disco no instalados — inventario de "listos para desplegar"
6. `easytech_check_expense_reason` — buscar en otros servidores (OCI, repos Git)

---

*Actualizar este catálogo tras cada despliegue de módulo o migración de cliente.*
