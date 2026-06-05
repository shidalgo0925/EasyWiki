# CODITO — Servidor lógico (Relatic Panamá)

Documento maestro del host que opera la **instancia EN1 de Relatic Panamá**.  
Actualizado tras inspección en servidor · junio 2026.

---

## Resumen ejecutivo

**CODITO** es el nombre lógico del VPS **Contabo** que aloja, entre otros silos Easy Technology, la **producción aislada de Relatic** (Easy NodeOne / EN1). Relatic consume la aplicación en `apps.relatic.org` y `miembros.relatic.org`, con base PostgreSQL dedicada y backups SQL diarios. El mismo equipo físico también ejecuta **dev, staging y prod** de Easy NodeOne para otros clientes — riesgo operativo documentado; el **propósito contractual de CODITO** es Relatic Panamá.

| Campo | Valor |
|-------|-------|
| **Cliente** | Relatic Panamá |
| **Producto principal** | EN1 (Easy NodeOne) — silo `relatic` |
| **Estado operativo** | **Producción** (Relatic) + co-hosting EasyTech (dev/staging/prod) |
| **Responsable** | EasyTech |
| **Proveedor IaaS** | Contabo |
| **Hostname técnico** | `vmi3225509.contaboserver.net` |

---

## Tarea 10 – Propósito del servidor

| Campo | Valor |
|-------|-------|
| **Nombre lógico** | CODITO |
| **Objetivo** | Operar la plataforma **Relatic Panamá** (membresías, pagos, planes, portal miembros) |
| **Cliente** | Relatic Panamá |
| **Estado** | **Producción** (instancia cliente Relatic). El VPS además aloja silos **Desarrollo / Staging / Prod** EasyTech (no confundir con el contrato Relatic). |
| **Responsable** | EasyTech |
| **Fecha de creación** | *Por confirmar con EasyTech* (host Contabo activo; silo `relatic` documentado desde abr 2026 en inventario interno) |

---

## Tarea 14 – Clasificación

| Campo | Valor |
|-------|-------|
| **Categoría** | **Producción** |
| **Subtipo** | Instancia dedicada por cliente (`/opt/easynodeone/relatic/`) |
| **Nota** | Mismo metal que laboratorio operativo EasyTech → ver **Riesgos** |

---

## Dominios (Relatic y relacionados en este host)

| Dominio | Uso | Backend |
|---------|-----|---------|
| `apps.relatic.org` | App EN1 Relatic (principal) | Gunicorn `127.0.0.1:9103` |
| `miembros.relatic.org` | Mismo upstream EN1 Relatic (alias host) | `9103` |
| `abril26.relatic.org` | Landing marketing estático (Vite `relatic-public`) | `/var/www/abril26.relatic.org` |

Otros `server_name` en el **mismo VPS** (no son Relatic, pero comparten máquina): `appprd.easynodeone.com`, `appdev…`, `apptst…`, sitios EClassOne / EThesis / `ai.easynodeone.com`, etc. — inventariar en fichas **Spaguetti**, **Arroz con Pollo**, **OCI** cuando corresponda.

---

## Aplicaciones

| Aplicación | Ruta en disco | Repositorio Git | Rama observada |
|------------|---------------|-----------------|----------------|
| **EN1 — silo Relatic** | `/opt/easynodeone/relatic/app` | `git@github.com:shidalgo0925/Easy-NodeOne.git` | `develop` *(verificar política: doc operativa indica `main` o `relatic`)* |
| **Landing Relatic** | `/opt/easynodeone/landings/relatic-public` | `git@github.com:shidalgo0925/relatic-public.git` | *según deploy* |
| **Front RelaticV2** *(opcional)* | `/opt/easynodeone/dev/relaticV2-github` | `github.com/Gill3010/relaticV2` | No sustituye EN1 salvo decisión producto |

**Cliente wiki:** [[04_Clientes/iius]] no aplica · **Relatic:** documentar ficha comercial en `04_Clientes/` cuando exista `relatic.md` *(pendiente en wiki)*.

---

## Servicios (systemd / puertos)

| Servicio | Unidad systemd | Puerto | WorkingDirectory |
|----------|----------------|--------|------------------|
| EN1 Relatic | `easynodeone-relatic.service` | **9103** | `/opt/easynodeone/relatic/app/backend` |
| EN1 Dev | `easynodeone-dev.service` | 9101 | `/opt/easynodeone/dev/app/backend` |
| EN1 Staging | `easynodeone-staging.service` | 9104 | `/opt/easynodeone/staging/app/backend` |
| EN1 Prod (otros clientes) | `easynodeone-prod.service` | 9102 | `/opt/easynodeone/prod/app/backend` |

| Capa | Componente |
|------|------------|
| Proxy | **Nginx** → upstream `easynodeone_relatic_app` |
| App | **Gunicorn** (venv `/opt/easynodeone/relatic/venv`) |
| Bootstrap | `bootstrap_nodeone.py` (PreStart, DDL idempotente) |
| Config | `EnvironmentFile=/opt/easynodeone/relatic/.env` |

---

## Tarea 11 – Dependencias

| Dependencia | Relatic / CODITO | Detalle |
|-------------|------------------|---------|
| **DNS** | Sí | Zonas `*.relatic.org` (y registros hacia IP del VPS). Gestión: *confirmar si registrador + Cloudflare*. |
| **Cloudflare** | **Sí** *(operativo típico)* | TLS/proxy en dominios públicos; no documentar credenciales. Confirmar acceso en cuenta EasyTech/Relatic. |
| **SMTP / correo** | Sí *(vía app)* | Variables tipo `MAIL_*` en plantilla EN1; remitente y relay configurados en administración / `.env` del silo — **sin copiar valores aquí**. |
| **APIs externas** | Sí | **Google OAuth** (`GOOGLE_CLIENT_*`); **PayPal** (`PAYPAL_*`, URLs return/cancel en `miembros.relatic.org`) |
| **Bases de datos externas** | **No** | PostgreSQL **local** `127.0.0.1:5432`, BD `easynodeone_relatic` (usuario dedicado en `.env`) |
| **Pasarelas de pago** | Sí | PayPal (modo según `PAYPAL_MODE`); otros métodos si el tenant los activa en EN1 |
| **Facturación electrónica** | No *(por defecto Relatic)* | Módulo `efactura` EN1 solo si se contrata y activa para la org — no asumido en esta ficha |

Referencias cruzadas (mismo host, otros clientes): integraciones Odoo viven en **TAMAL** / EN1 dev, no en silo Relatic.

---

## Tarea 12 – Accesos operativos

*(Sin contraseñas ni claves.)*

| Acceso | ¿Disponible? | Notas |
|--------|--------------|-------|
| **SSH** | **Sí** | Acceso equipo EasyTech al VPS Contabo |
| **Root / sudo** | **Sí** | Migraciones, `systemctl`, Nginx, PostgreSQL |
| **Git** | **Sí** | Pull en `/opt/easynodeone/relatic/app`; **no** editar árbol a mano en prod |
| **Cloudflare** | **Sí** *(esperado)* | DNS / proxy / firewall; cuenta a nombrar en runbook interno |
| **Proveedor** | **Contabo** | Plan VPS; hostname `vmi3225509` |

Panel Contabo: gestión de VM, snapshots proveedor *(si contratados — verificar)*.

---

## Tarea 13 – Backups

| Campo | Valor |
|-------|-------|
| **Existe backup** | **Sí** |
| **Frecuencia** | **Diaria** — `0 2 * * *` (cron sistema) |
| **Script** | `/opt/easynodeone/scripts/backup-easynodeone.sh` |
| **Qué respalda** | SQL plano: `easynodeone_relatic` → `relatic_YYYY-MM-DD_HH-MM.sql` |
| **Ubicación** | **Local** — `/opt/easynodeone/backups/` |
| **Remota** | *Por confirmar* (no documentada copia off-site automática en script actual) |
| **Responsable** | **EasyTech** (operación); verificar restauración trimestral |
| **Log cron** | `/var/log/easynodeone-backup-sql.log` |

El mismo cron también genera `prod_*.sql` (otros clientes en el mismo VPS). Restauración Relatic: procedimiento solo con ventana acordada y BD de prueba primero.

*(Opcional histórico: volcados `-Fc` en `/var/backups/easynodeone/daily/` si el script extendido sigue activo — ver `EASYNODEONE-OPERACION-DIARIA.md` en servidor.)*

---

## Riesgos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| **VPS compartido** (Relatic + dev/staging/prod + otros sitios) | Error en deploy/migración puede afectar vecinos | Checklist staging; ramas y `.env` por silo; no tocar `relatic/` sin ventana |
| **Rama Git vs política** (`develop` observada en silo) | Desalineación con doc `main`/`relatic` | Acordar rama única Relatic y fijar en checklist |
| **Backup solo local** | Pérdida del VPS = pérdida de backups | Añadir réplica remota (S3, otro DC) — pendiente |
| **Secretos en `.env`** | Fuga si se copian a wiki/chat | Solo gestor de secretos; rotación PayPal/OAuth |
| **Cloudflare / DNS** | Caída DNS = app inaccesible | Documentar cuenta y contacto; monitor externo |

---

## Próximos pasos

1. **Confirmar** fecha de alta CODITO y contacto Relatic en `05_Proyectos/` *(crear `relatic/` si aplica)*.
2. **Fijar rama Git** del silo Relatic (`main` vs `develop` vs `relatic`) y reflejarlo en [[07_Operaciones/deploy]].
3. **Verificar** backup off-site y prueba de restore de `easynodeone_relatic`.
4. **Crear ficha** `04_Clientes/relatic.md` en Easy Wiki (comercial, no técnica).
5. **Documentar OCI** (siguiente en cola) antes de profundizar **TAMAL** (Odoo 18/19, FE, módulos EasyTech).
6. **No copiar** `backend/docs` de EN1 aquí; enlazar desde [[99_Recursos/README]] si hace falta.

---

## Referencias en servidor (no wiki)

| Documento | Ruta |
|-----------|------|
| Inventario apps | `/opt/easynodeone/UBICACION-APPS.md` |
| Operación diaria | `/opt/easynodeone/EASYNODEONE-OPERACION-DIARIA.md` |
| Config pagos Relatic | `relatic/app/md/CONFIGURACION_PAGOS.md` *(en repo EN1)* |

---

## Checklist de secciones (inspección)

| Sección | Estado |
|---------|--------|
| Resumen ejecutivo | ✅ |
| Propósito (Tarea 10) | ✅ |
| Cliente | ✅ |
| Dominios | ✅ |
| Aplicaciones | ✅ |
| Servicios | ✅ |
| Dependencias (Tarea 11) | ✅ |
| Backups (Tarea 13) | ✅ |
| Accesos (Tarea 12) | ✅ |
| Clasificación (Tarea 14) | ✅ |
| Riesgos | ✅ |
| Próximos pasos | ✅ |

---

**Índice servidores:** [[06_Arquitectura/servidores/README]] · **Deploy EN1:** [[07_Operaciones/deploy]]
