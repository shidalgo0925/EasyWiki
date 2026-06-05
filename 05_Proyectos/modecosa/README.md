# Proyecto — Modecosa

**Cliente:** [[04_Clientes/modecosa]]  
**ERP:** Odoo 19 en `erp.modecosa.com`  
**EN1:** Matriz de permisos vía módulo `security_matrix`

## Alcance

| Fase | Estado | Entregable |
|------|--------|------------|
| Fase 1 | **Entregada** | `en1_connector` + `GET /api/en1/v1/security-catalog` |
| Fase 2 | Planificada | `POST …/security-matrix/apply` con aprobación humana |

## Configuración EN1 (referencia interna)

- URL catálogo Odoo en variables de entorno del silo.
- API key de **solo lectura** (no usuario humano admin).
- Prueba: importación exitosa (~28 users, 111 groups, 153 memberships).

## Contactos

| Rol | Nombre | Canal |
|-----|--------|-------|
| Programador Odoo (cliente) | *(completar)* | |
| Easy — integración | *(completar)* | |

## Hitos

| Fecha | Hito |
|-------|------|
| *(completar)* | Fase 1 en producción Odoo |
| Roadmap 2026 | Fase 2 matriz apply |

## Coordinación

- Cambios en JSON del catálogo: alinear con especificación v1 del producto EN1.
- Pagos EN1 → Odoo: flujo webhook existente; **no mezclar** con tickets de catálogo de seguridad.

## Enlaces

- [[04_Clientes/modecosa]]
- [[03_Productos/integrations]]
