# Integraciones (Easy Suite)

EN1 y el resto de la suite se conectan a sistemas del cliente o de terceros. Esta página resume **qué integramos** y **cómo se explica al cliente**.

## ERP — Odoo (referencia: Modecosa)

| Flujo | Descripción |
|-------|-------------|
| **Catálogo de seguridad** | Odoo expone JSON de usuarios, grupos y membresías; EN1 importa y muestra matriz |
| **Pagos** | EN1 notifica pagos a Odoo por webhook (configuración separada) |

Fase 1 catálogo: **solo lectura** desde Odoo. Fase 2: aplicar cambios en grupos con aprobación.

Ver [[04_Clientes/modecosa]] y [[06_Arquitectura/arquitectura_api]].

## Pagos

- Stripe, PayPal (automático).
- Yappy con comprobante y transferencia bancaria (validación manual).
- Configuración **por organización**.

## Educación

- **Moodle** (módulo `academic`) cuando el proyecto lo incluye.
- Campus cerrado y matrículas nativas EN1 (IIUS).

## Correo y marketing

- SMTP / plantillas EN1.
- Campañas `marketing_email`.
- Office 365 institucional (`office365`).

## Facturación electrónica

- Panamá vía PAC en módulo `efactura`.

## Landings externas

- Sitios de inscripción o marketing en OCI u otro hosting que llaman a EN1 (checkout, programas).

## Punto de venta

- [[03_Productos/eposone]] puede compartir catálogo y clientes con EN1 según contrato.

## Lo que no hacemos por defecto

- Sincronizar inventario completo bidireccional con cualquier ERP sin proyecto dedicado.
- Guardar credenciales de admin Odoo en EN1 para Fase 1 de matriz.

---

**Suite:** [[02_Suite/mapa_suite]]
