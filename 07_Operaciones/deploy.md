# Deploy (procedimiento EN1)

Procedimiento **obligatorio** para actualizar Easy NodeOne en servidores de cliente o silos Easy Technology. Resume la política del producto en lenguaje operativo.

## Regla de oro

> **Solo se edita código en desarrollo** (`dev/app`). Staging, producción y relatic **solo** reciben código con `git pull` (o checkout de tag/commit acordado), más dependencias, migraciones y reinicio.

Nunca copiar archivos a mano entre silos ni parchear prod con el editor.

## Flujo recomendado

```text
1. Desarrollo y commit en dev (rama develop)
2. Merge / release a main cuando el equipo aprueba
3. Staging: checkout del tag o commit acordado → migrar → reiniciar → QA
4. Prod: MISMA revisión que pasó staging → migrar → reiniciar → verificación
5. Comunicado al cliente si hay novedades visibles
```

## Comandos típicos (servidor Linux)

### Staging o prod — actualizar código

```bash
cd /opt/easynodeone/<staging|prod>/app
git fetch origin --tags
# Dejar el árbol en la revisión acordada, por ejemplo:
# git checkout vX.Y.Z
# o git pull origin main   # solo si el equipo acordó ese commit exacto
```

### Migración de base de datos

```bash
# Producción requiere confirmación explícita en variable de entorno:
export EASYNODEONE_MIGRATE_PROD_CONFIRM=YES   # solo prod
sudo -E bash /opt/easynodeone/scripts/migrate-easynodeone-instance.sh <dev|staging|prod>
```

### Reinicio del servicio

```bash
sudo systemctl restart easynodeone-<dev|staging|prod>
```

Si el servicio **no arranca**: revisar `journalctl -u easynodeone-<silo> -n 80`. Causa frecuente tras releases grandes: **columnas nuevas** en tablas (`invoices`, `payment`, etc.) — la migración debe completarse sin error.

## Qué validar después del deploy

| Check | Cómo |
|-------|------|
| Login admin y usuario normal | Credenciales de prueba del cliente |
| Dashboard | Sin error 500 |
| Módulo crítico del cliente | Ej. campus IIUS, matriz Modecosa, taller, checkout |
| Pago de prueba | Solo en staging o con monto simbólico acordado |

## Ventana con el cliente (producción)

- Acordar **hora y duración** (mantenimiento breve).
- Tener contacto del cliente para avisar «listo» o rollback.
- No desplegar prod un viernes tarde sin plan de guardia.

## Archivos locales que no deben perderse

En algunos silos existen `.env` o `.env.production` **no versionados**. Antes de `git pull`, si hay riesgo de conflicto, el operador hace **stash** o backup del archivo local y lo restaura tras el pull.

## Relación con Easy Wiki

- Novedades para el cliente: redactar desde el doc de novedades del producto y publicar comunicado.
- Este archivo: procedimiento interno Easy Technology.
- Detalle checklist extendido: documento de checklist en el repo del producto (no duplicado línea a línea aquí).

## Quién hace qué

| Rol | Acción |
|-----|--------|
| Desarrollo | Commit en dev, PR, release |
| Operación / DevOps | Pull, migración, reinicio, logs |
| QA | Validación en staging |
| Cuenta / soporte | Aviso al cliente y seguimiento post-deploy |

---

**Ver también:** [[07_Operaciones/qa]] · [[07_Operaciones/soporte]] · [[03_Productos/en1_platform]]
