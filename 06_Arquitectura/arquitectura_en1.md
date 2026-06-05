# Arquitectura — EN1 (Easy NodeOne)

Resumen para **operación, ventas y soporte**. El detalle de código vive en el repositorio del producto; aquí está la «foto» que el equipo Easy debe conocer.

## Qué es EN1 técnicamente

- **Monolito web** (una aplicación principal) con **módulos** que se encienden por organización.
- **Multi-tenant**: cada `organización` tiene datos, módulos y pagos propios.
- **PostgreSQL** (o SQLite en desarrollo local) como base de datos.
- **Sesión por cookie** (login web); APIs JSON reutilizan la misma sesión para admin y apps.

## Capas (vista simple)

```text
[ Navegador / App Flutter / Landing externa ]
                    │
                    ▼
         [ Aplicación web EN1 + seguridad ]
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
  Módulos      Guards SaaS     Roles RBAC
  (citas,      (¿módulo ON     (permisos
   taller,      para esta       finos)
   ventas…)      empresa?)
                    │
                    ▼
              [ Base de datos ]
```

## Punto de entrada y módulos

- Toda funcionalidad nueva entra como **módulo** registrado de forma central (no rutas sueltas sin control).
- Antes de servir una pantalla o API, se comprueba si el **módulo SaaS** está activo para la organización actual.
- Admin de **plataforma** (`is_admin`) omite restricciones de módulo y puede ver cualquier org.

## Multi-empresa (resolución de contexto)

La organización activa se resuelve por:

- Subdominio / host (si aplica).
- Selector tras login si el usuario tiene varias empresas.
- Última organización elegida en sesión.

Modo **single-tenant** (una sola org forzada) existe en instalaciones dedicadas; en IIUS suele ser org principal = instituto.

## Autenticación y permisos

| Mecanismo | Uso |
|-----------|-----|
| Login web | Sesión cookie estándar |
| Admin plataforma | Acceso global a configuración |
| Admin tenant | Administración de su empresa (RBAC) |
| Permisos granulares | Códigos tipo `analytics.view`, dominio `workshop`, etc. |
| Módulo SaaS | Si está apagado, pantalla redirige o API responde 403 |

## Integraciones externas (catálogo)

| Sistema | Para qué |
|---------|----------|
| Stripe / PayPal | Pagos en línea |
| Yappy manual / transferencia | Cobro local con validación |
| Google / Facebook / LinkedIn | Login social (si está configurado) |
| Odoo | Catálogo seguridad (Modecosa); webhooks de pago hacia Odoo |
| PAC efacturapty | Factura electrónica Panamá |
| Office 365 | Flujo correo institucional |
| Moodle | LMS (módulo académico) |

## Entornos y despliegue

| Silo | Rama típica | Regla |
|------|-------------|-------|
| `dev/app` | `develop` | **Único** lugar donde se edita código |
| `staging/app` | `main` (tag/commit acordado) | Solo `git pull` + migración + reinicio |
| `prod/app` | `main` (misma revisión validada en staging) | Igual; nunca parches a mano |

Tras cada actualización en servidor: script de migración del silo + reinicio del servicio systemd (`easynodeone-<silo>`). Si el servicio no arranca, revisar logs: a menudo faltan columnas nuevas en PostgreSQL.

Ver procedimiento: [[07_Operaciones/deploy]]

## Módulos por dominio (mapa mental)

- **Legacy / núcleo:** auth, members, payments, communications, marketing, policies.
- **Operaciones:** citas, eventos, taller, contador inventario.
- **Comercial:** CRM, contactos, ventas, analítica.
- **Educación:** academic (programas, matrículas).
- **Finanzas:** efactura, facturas.
- **Seguridad / integración:** matriz Odoo, permisología EN1.

Lista completa con nombres en pantalla: [[03_Productos/en1_platform#Catálogo de módulos EN1 (referencia)]]

## Documentos relacionados en wiki

- [[03_Productos/en1_platform]]
- [[07_Operaciones/modulo_taller]]
- [[06_Arquitectura/arquitectura_api]]
- [[06_Arquitectura/servidores/README]] — fichas CODITO, OCI, TAMAL, etc.
- [[04_Clientes/iius]] · [[04_Clientes/modecosa]]

---

**Suite:** [[02_Suite/mapa_suite]]
