# Odoo 18 Community — TAMAL

| Campo | Valor |
|---|---|
| **Servidor** | TAMAL (`217.216.80.159`) |
| **Versión** | Odoo Server 18.0 |
| **Edición** | Community |
| **Estado** | Producción — `odoo.service` active |

---

## Instalación

| Componente | Detalle |
|---|---|
| Ruta | `/opt/odoo` |
| Binario | `/opt/odoo/odoo-bin` |
| Python | 3.12.3 — venv `/opt/odoo/venv` |
| Config | `/etc/odoo/odoo.conf` |
| Servicio | `odoo.service` (systemd, usuario `odoo`) |
| Puerto | 8069 (detrás de nginx) |
| PostgreSQL | 16 — cluster `16-main`, usuario `odoo` |
| Addons | `/opt/odoo/addons` (core) + `/opt/odoo/custom-addons` (custom) |
| Data | `/var/lib/odoo` |

---

## Bases de datos en esta instancia

| Base | Cliente | URL | Clasificación |
|---|---|---|---|
| Easydb | Easy Technology Services | `https://easydb.etsrv.site` | Producción |
| lahuaca | La Huaca | `https://lahuaca.etsrv.site` | Producción |
| SMRC | Servicios Múltiples RC | `https://smrc.etsrv.site` | Producción |
| Sanadb | SANAGUA LODGE | *(selector interno)* | Producción |
| TTTourism | T & T Tourism Plus | `https://tttourism.etsrv.site` | Producción |
| relatic | Relatic / Multiservicios TK | `https://relatic.etsrv.site` | Producción |
| odoo18 | YourCompany (demo) | *(sin URL)* | Laboratorio |

---

## Arquitectura de acceso

Nginx mapea subdominio → base mediante `map $host $odoo_db` en `/etc/nginx/sites-available/easydb-etsrv.conf`.

Flujo:

```
Usuario → https://<cliente>.etsrv.site
       → nginx (SSL Let's Encrypt)
       → redirect / → /web/login?db=<DB_NAME>
       → Odoo :8069
```

Patrón heredado de la arquitectura OCI (documentada y cerrada).

---

## Módulos de contabilidad Community

Desplegados vía Odoo Mates / Cybrosys en clientes contables:

- `om_account_accountant`
- `om_account_asset`
- `om_account_budget`
- `om_account_daily_reports`
- `om_account_followup`
- `om_fiscal_year`
- `om_recurring_payments`
- `base_accounting_kit` (Cybrosys)

---

## Tema UI

MuK Backend Theme desplegado en todas las bases activas:

- `muk_web_appsbar`
- `muk_web_chatter`
- `muk_web_colors`
- `muk_web_dialog`
- `muk_web_theme`

---

## Monitoreo

- Health endpoint: `GET /web/health` (200 OK — polling cada ~70s en logs)
- Script: `/usr/local/bin/odoo-healthcheck.sh` (reinicia odoo si falla; servicio oneshot no programado en cron visible)

---

## Backup PostgreSQL — TAMAL

| Campo | Valor |
|---|---|
| **Estado** | **Cron diario activo (Fase 4)** — 2026-06-05 |
| **Script backup** | `/usr/local/bin/backup_postgresql_tamal.sh` |
| **Script verify** | `/usr/local/bin/verify_backup_postgresql_tamal.sh` |
| **Cron** | `/etc/cron.d/backup-postgresql-tamal` — **02:00** backup · **04:00** verify |
| **Ejecución manual** | `sudo /usr/local/bin/backup_postgresql_tamal.sh` |
| **Formato** | `pg_dump -Fc` (PostgreSQL 16.14) |
| **Local TAMAL** | `/backups/tamal/db/YYYY-MM-DD/` |
| **Remoto OCI** | `backupsrv@40.233.1.138:/backups/tamal/YYYY-MM-DD/` |
| **Total 6 bases prod.** | **~74 MB** por ejecución |
| **Restauración completa** | ✅ Easydb + **lahuaca** (Fase 5) |

### Bases incluidas

Easydb · lahuaca · SMRC · Sanadb · TTTourism · relatic — excluida `odoo18`.

Procedimiento DR completo: [[07_ERP/disaster_recovery]].

---

### Tamaño dump por base (referencia Fase 2.5)

| Base | Cliente | Tamaño dump | Restauración validada |
|---|---|---:|---|
| Easydb | Easy Technology Services | 9.7 MB | ✅ **restore real** (Fase 5) |
| lahuaca | La Huaca | 16 MB | ✅ **restore real** (Fase 5) |
| SMRC | Servicios Múltiples RC | 13 MB | ✅ `--list` |
| Sanadb | SANAGUA LODGE | 9.5 MB | ✅ `--list` |
| TTTourism | T & T Tourism Plus | 9.7 MB | ✅ `--list` |
| relatic | Relatic / Multiservicios TK | 17 MB | ✅ `--list` |
| **TOTAL** | — | **~74 MB** | Easydb + lahuaca restore real ✅ |

Procedimiento restore: [[06_Arquitectura/servidores/TAMAL#Backup Hub OCI — Fase 5 (restauración real)]].

---

## Riesgos específicos Odoo 18 en TAMAL

1. Única instancia para todos los tenants
2. Módulos instalados sin código fuente en disco
3. Sin `dbfilter` restrictivo — aislamiento depende solo de nginx/subdominio
4. Admin master password en config de servidor

---

*Ver también: `06_Arquitectura/servidores/TAMAL.md`, `catalogo_modulos_easytech.md`*
