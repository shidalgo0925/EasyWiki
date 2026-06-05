# Odoo 19 Enterprise — TAMAL

| Campo | Valor |
|---|---|
| **Servidor inspeccionado** | TAMAL |
| **Fecha inspección** | 2026-06-04 |
| **Resultado** | **NO INSTALADO** |

---

## Hallazgos

La inspección de TAMAL no encontró:

- Binario Odoo 19 (`odoo-bin` único en `/opt/odoo` — versión 18.0)
- Directorio de addons Enterprise (`web_enterprise`, etc.)
- Servicio systemd adicional para Odoo 19
- Base de datos asociada a Odoo 19
- Licencia Enterprise activa

### Única instancia presente

| Instancia | Versión | Edición |
|---|---|---|
| `/opt/odoo` | 18.0 | Community |

---

## Base `odoo18` — aclaración

Existe una base PostgreSQL llamada `odoo18` en TAMAL. **No es Odoo 19 ni Enterprise.**

| Campo | Valor |
|---|---|
| Empresa | YourCompany |
| Módulos instalados | 12 |
| Clasificación | Laboratorio / demo |
| Última actividad | 2026-02-27 |

Probablemente creada durante pruebas de migración o setup inicial del servidor.

---

## Implicaciones

- Funcionalidades Enterprise (accounting reports avanzados, studio, IoT, etc.) **no disponibles** en TAMAL
- Contabilidad se cubre con módulos Community de terceros (Odoo Mates)
- Si EasyTech planea Odoo 19 Enterprise, requerirá nuevo despliegue (servidor o instancia adicional)

---

## Acción recomendada (documentación)

Cuando se despliegue Odoo 19 Enterprise:

1. Documentar en este archivo: ruta, servicio, licencia, bases
2. Actualizar `06_Arquitectura/servidores/TAMAL.md` o crear servidor dedicado
3. Definir migración de clientes desde Odoo 18 Community

---

*Estado: placeholder post-inspección — sin Enterprise en TAMAL al 2026-06-04.*
