# Arquitectura — APIs e integraciones

Cómo EN1 se comunica con **fuera** de la plataforma. Resumen para soporte y integradores.

## APIs propias EN1

- Prefijos **`/api/...`** por dominio (taller, CRM, académico, etc.).
- Requieren **sesión autenticada** salvo rutas públicas documentadas (landings, webhooks entrantes).
- Si el módulo SaaS está apagado: respuesta **403** con mensaje de módulo no habilitado.

## Integración Odoo (Modecosa — catálogo)

| Dirección | Método | Uso |
|-----------|--------|-----|
| Odoo → EN1 | `GET /api/en1/v1/security-catalog` | Descarga JSON usuarios/grupos |
| EN1 → Odoo (fase 2) | `POST …/security-matrix/apply` | Cambios aprobados en grupos |

Autenticación: **Bearer** API key de solo lectura (fase 1). Base de datos: header `X-Odoo-Database`.

## Pagos EN1 → Odoo

- Webhooks de pago desde EN1 hacia Odoo (config `ODOO_API_URL`, firma HMAC).
- **Independiente** del conector de catálogo de seguridad.

## Pasarelas de pago

| Proveedor | Uso |
|-----------|-----|
| Stripe / PayPal | Cobro en línea automático |
| Yappy manual | Comprobante + validación admin |
| Transferencia | Instrucciones en checkout |

## Factura electrónica Panamá

- Módulo `efactura` → PAC (efacturapty u otros según configuración).

## App móvil / Flutter

- Consume las mismas APIs y sesión que la web donde el proyecto lo habilita.
- Sincronización documentada en el repo producto (`FLUTTER_SYNC`).

## Office 365

- Módulo `office365`: solicitudes de correo institucional (flujo aprobación).

## Buenas prácticas

- No exponer API keys en wiki ni chats.
- Rate limit y allowlist IP en Odoo recomendados para catálogo.
- Probar siempre en **staging** antes de prod.

---

**Clientes:** [[04_Clientes/modecosa]] · **EN1:** [[06_Arquitectura/arquitectura_en1]]
