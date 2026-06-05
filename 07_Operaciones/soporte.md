# Soporte a clientes

Procedimiento para **incidencias** en EN1 y productos Easy Suite.

## Qué pedir siempre al cliente

1. **Hora exacta** (zona Panamá u otra acordada).
2. **Usuario** (email o login, sin contraseña).
3. **Organización** si tiene varias empresas en la misma plataforma.
4. **Pantalla o URL** donde ocurrió (ej. campus, checkout, taller).
5. **Qué esperaba** vs **qué vio** (mensaje de error, captura si puede).
6. Si es **pago**: método (Yappy, transferencia), si subió comprobante.

## Niveles

| Nivel | Quién | Ejemplos |
|-------|-------|----------|
| L1 | Cliente / capacitación | «No encuentro el menú», contraseña olvidada |
| L2 | Easy Technology operación | Módulo apagado, pago pendiente de validación, campus sin matrícula |
| L3 | Desarrollo | Error 500, bug reproducible, integración Odoo |

## Antes de escalar a desarrollo

- Confirmar módulo SaaS activo para la org.
- Reproducir en **staging** si existe.
- Revisar si hubo **deploy reciente** ([[07_Operaciones/deploy]]).

## Errores conocidos post-actualización

| Síntoma | Causa habitual |
|---------|----------------|
| 500 en dashboard tras deploy | Migración incompleta o transacción SQL sin rollback en chequeo de usuario |
| No entra al campus (IIUS) | Matrícula no en `paid`/`confirmed`; Yappy sin validar |
| Matriz Odoo vacía (Modecosa) | API key, URL catálogo, firewall |

## Comunicación al cliente

- Tono claro, sin jerga de servidor.
- Plazo estimado si se requiere deploy.
- Referencia a novedades si la incidencia es «¿dónde está la función nueva?» (doc novedades jun 2026).

---

**IIUS:** [[04_Clientes/iius]] · **Modecosa:** [[04_Clientes/modecosa]] · **Taller:** [[07_Operaciones/modulo_taller]]
