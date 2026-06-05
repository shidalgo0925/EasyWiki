# EClassOne

**EClassOne** es el producto de [[02_Suite/easy_suite|Easy Suite]] para **aula digital y experiencia de campus**: aprendizaje en línea, acceso a contenidos y convivencia con inscripciones y pagos del instituto.

## Relación con EN1

En implementaciones como [[04_Clientes/iius]], la **lógica operativa** (programas, matrículas, pagos, campus cerrado) vive en **EN1** con el módulo `academic`. EClassOne es la **marca y el paquete comercial** de «experiencia educativa»; puede incluir:

- Campus web EN1 (`/mi-campus`, política `academic_closed`).
- Integración **Moodle** cuando el contrato lo pide.
- Landings de inscripción y certificados/eventos.

## Para qué sirve (mensaje al cliente)

- Publicar programas y cobrar inscripciones en un solo ecosistema.
- Controlar **quién entra al campus** según matrícula o pago.
- Emitir certificados y gestionar eventos académicos si están contratados.

## Módulos EN1 típicos

| Módulo | Uso |
|--------|-----|
| `academic` | Programas, matrículas |
| `payments` | Cobros |
| `memberships` | Planes institucionales |
| `events` / `certificates` | Congresos y diplomas |
| `marketing_email` | Comunicación a alumnos |

## Implementación

Easy Technology configura tenant, política de campus y branding antes de go-live.

## Presencia en CODITO (jun 2026)

Aplicación **EClassOne** desplegada en `/opt/easyclassone/{dev,staging,prod}/app` — Flask + Gunicorn + PostgreSQL. **Sin repositorio Git local** en el servidor (confirmar origen remoto).

| Silo | Dominio | BD | Comercial |
|------|---------|-----|-----------|
| Dev | `appdev.eclassone.com` | `easyclassone_dev` | Laboratorio |
| Staging | `appstaging.eclassone.com` | `easyclassone_staging` | Staging |
| Prod | `app.eclassone.com` | `easyclassone_prod` | Producción |

Landing estática: `eclassone.com` → `/var/www/eclassone`.

Detalle: [[02_Suite/inventario_easy_suite]].

**Cliente referencia:** [[04_Clientes/iius]] · **Proyecto:** `05_Proyectos/iius/`

---

**Mapa:** [[02_Suite/mapa_suite]] · **Plataforma:** [[03_Productos/en1_platform]]
