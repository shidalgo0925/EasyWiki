# Proyecto — EN1 (plataforma)

**Producto:** [[03_Productos/en1_platform]]  
**Repositorio:** Easy-NodeOne (código solo en silo desarrollo según política Git)

## Qué documenta este proyecto

Evolución **transversal** de la plataforma (no un cliente concreto): releases, módulos nuevos, deuda técnica acordada, capacitación interna.

## Silos de despliegue Easy Technology

| Silo | Ruta servidor | Rama habitual |
|------|---------------|---------------|
| Dev | `/opt/easynodeone/dev/app` | `develop` |
| Staging | `/opt/easynodeone/staging/app` | `main` / tag |
| Prod | `/opt/easynodeone/prod/app` | `main` / tag |

## Release reciente (referencia jun 2026)

- Panel ERP, contactos, pagos Yappy por org, taller SLA, eventos/certificados, FE Panamá (inicio), fixes transacciones SQL en chequeos de usuario.
- Documentación técnica en `backend/docs/` del repo producto.

## Clientes que consumen EN1

- [[04_Clientes/iius]]
- [[04_Clientes/modecosa]]
- [[04_Clientes/clientes_generales]]

## Operación

- [[07_Operaciones/deploy]]
- [[06_Arquitectura/arquitectura_en1]]
