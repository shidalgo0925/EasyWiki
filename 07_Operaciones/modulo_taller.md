# Módulo Taller (EN1) — operación

Guía para **administradores del cliente**, **recepción de taller** y **soporte Easy Technology**. Código SaaS: **`workshop`** («Taller + SLA»).

## Qué cubre

| Capacidad | Descripción |
|-----------|-------------|
| Órdenes de trabajo (OT) | Vehículo, cliente, líneas de servicio/producto, notas, asesor |
| Inspección | Mapa de zonas, puntos de daño, severidad, fotos |
| Checklist | Ítems de recepción/entrega |
| Fotos | Entrada, proceso y salida |
| SLA por etapa | Semáforo verde / amarillo / rojo, monitor y alertas |
| Cotización | Crear cotización en **Ventas** desde la OT (requiere módulo `sales`) |

## Activar el módulo para un cliente

1. Admin de **plataforma** → Organizaciones → **Módulos SaaS**.
2. Activar **`workshop`** para la empresa del taller.
3. Usuarios de recepción deben tener sesión en esa **organización**.

Si está apagado: pantallas de taller redirigen al dashboard; las APIs responden error de módulo no habilitado.

## Módulos relacionados

| Módulo | ¿Obligatorio? | Uso |
|--------|---------------|-----|
| `workshop` | Sí | Todo el taller |
| `sales` | Solo para cotización desde OT | Genera cotización `Q-xxxx` |
| Catálogo de servicios | Recomendado | Líneas de OT y tiempos por tipo de servicio |

## Pantallas principales (admin tenant)

| Pantalla | Ruta | Función |
|----------|------|---------|
| Monitor / listado | `/admin/workshop/orders` | Tablero OT, filtros, SLA, KPIs |
| Nueva orden | `/admin/workshop/orders/new` | Alta de OT |
| Detalle | `/admin/workshop/orders/<id>` | Edición, inspección, fotos, estados |
| Ajustes SLA | `/admin/workshop/settings` | Parámetros generales |
| Procesos | `/admin/workshop/process-config` | Minutos por etapa y por servicio |

## Flujo operativo típico

1. **Recepción** crea OT con datos del vehículo y cliente (búsqueda o alta rápida).
2. **Inspección** en mapa de carrocería; fotos por punto si hay daño.
3. **Cotización** (si tienen Ventas): generar desde la OT para aprobar con el cliente.
4. **Trabajo en proceso** — actualizar estado y fotos de proceso.
5. **Entrega** — checklist de salida y cierre.

El **monitor SLA** muestra retrasos por etapa (recepción, cotización, en taller, entrega, etc.). Los tiempos esperados se configuran en Ajustes / Procesos.

## Soporte: incidencias frecuentes

| Problema | Qué revisar |
|----------|-------------|
| No aparece menú Taller | Módulo `workshop` activo para la org; usuario en la org correcta |
| No genera cotización | Módulo `sales` activo |
| Fotos no suben | Permisos de carpeta en servidor (operación); tamaño de archivo |
| Semáforo siempre rojo | Tiempos SLA muy bajos en configuración de procesos |

## Despliegue (equipo Easy)

Tras actualizar código en staging/prod: migración del silo + reinicio ([[07_Operaciones/deploy]]). El producto aplica cambios de esquema de taller de forma idempotente en el arranque/migración.

---

**Producto:** [[03_Productos/en1_platform]] · **Arquitectura:** [[06_Arquitectura/arquitectura_en1]]
