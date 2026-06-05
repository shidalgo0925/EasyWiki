# TAMAL — Servidor ERP Principal EasyTech

| Campo | Valor |
|---|---|
| **Nombre interno** | TAMAL |
| **Hostname sistema** | `vmi3048421` / `vmi3048421.contaboserver.net` |
| **Proveedor** | Contabo (AS40021) |
| **Rol** | Servidor ERP principal multi-tenant Odoo 18 Community |
| **Estado inspección** | 2026-06-04 — DOCUMENTADO |
| **Backup Hub OCI** | Fase 1 — **VALIDADA** (2026-06-05) |
| **Restricción aplicada** | Solo lectura; sin reinicios ni cambios |

---

## FASE 1 — Inventario del servidor

| Recurso | Detalle |
|---|---|
| **Sistema operativo** | Ubuntu 24.04.4 LTS (Noble Numbat) — kernel 6.8.0-106-generic |
| **CPU** | 4 vCPU — AMD EPYC (KVM/QEMU) |
| **RAM** | 7.8 GiB total — ~6.0 GiB disponible |
| **Swap** | **0 B** (sin swap configurado) |
| **Disco** | `/dev/sda1` 145 GB — 9.3 GB usados (7%) |
| **IP pública** | `217.216.80.159` |
| **IPv6 pública** | `2605:a143:2304:8421::1` |
| **IP privada** | No aplica — VPS Contabo con interfaz pública única (`eth0`) |
| **Uptime al inspeccionar** | 68 días |
| **Usuarios shell** | `admin`, `shidalgo`, `odoo` |

---

## FASE 2 — Inventario Odoo

### Instancias encontradas

| Instancia | Versión | Edición | Ruta | Servicio systemd | Python | PostgreSQL | Estado |
|---|---|---|---|---|---|---|---|
| **Odoo principal** | 18.0 | **Community** | `/opt/odoo` | `odoo.service` | 3.12.3 (`/opt/odoo/venv`) | PostgreSQL 16 (`postgresql@16-main`) | **active** |

### No presente en TAMAL

- Odoo 19
- Odoo Enterprise
- Segunda instancia Odoo

### Configuración clave

| Parámetro | Valor |
|---|---|
| Config | `/etc/odoo/odoo.conf` |
| Binario | `/opt/odoo/odoo-bin` |
| Addons path | `/opt/odoo/custom-addons`, `/opt/odoo/addons` |
| Data dir / filestore | `/var/lib/odoo` (283 MB filestore) |
| Puerto HTTP | `8069` (proxy nginx `proxy_mode=True`) |
| Log | `/var/log/odoo/odoo.log` |
| Healthcheck | `odoo-healthcheck.service` (oneshot, **inactive**); polling activo vía `/web/health` |

---

## FASE 3 — Inventario de bases de datos

Arquitectura: **multi-tenant por subdominio** (`*.etsrv.site`) con map nginx → `db=`.

| Base | Empresa(s) | Tamaño | Subdominio | Clasificación | Última actividad usuario | Observaciones |
|---|---|---|---|---|---|---|
| **Easydb** | Easy Technology Services - TML | 62 MB | `easydb.etsrv.site` | **Producción** (interno EasyTech) | 2026-03-28 | 12 facturas; módulo `ets_weasy_sale_quote` instalado **sin código en disco** |
| **lahuaca** | La Huaca | 121 MB | `lahuaca.etsrv.site` | **Producción** | 2025-12-29 (accesos recientes en log) | **5 637 facturas** — cliente de mayor volumen; `invoice_import_massive` activo |
| **SMRC** | Servicios Múltiples RC | 65 MB | `smrc.etsrv.site` | **Producción** | 2026-02-26 | FE HKA activa — 47 docs autorizados |
| **Sanadb** | SANAGUA LODGE, S.A. - TML | 60 MB | *(sin subdominio)* | **Producción** | 2026-03-11 | FE HKA activa — 37 docs autorizados; acceso solo vía selector Odoo |
| **TTTourism** | T & T Tourism Plus, S.A. - TML | 60 MB | `tttourism.etsrv.site` | **Producción** | 2026-01-22 | FE HKA activa — 3 docs autorizados |
| **relatic** | Relatic Panamá - TML; Multiservicios TK - TML | 80 MB | `relatic.etsrv.site` | **Producción** | 2025-11-20 | `relatic_integration` instalado **sin código en disco** |
| **odoo18** | YourCompany | 23 MB | *(sin subdominio)* | **Laboratorio / Demo** | 2026-02-27 | Solo 12 módulos instalados; base de prueba |

**No encontradas en TAMAL:** bases Modecosa, Rycom ni referencias en PostgreSQL.

---

## FASE 4 — Clientes

| Cliente | Base | Estado | Proyecto / función | Dependencias |
|---|---|---|---|---|
| **Easy Technology Services** | Easydb | Activo | ERP interno corporativo | Odoo 18, tema MuK, `ets_weasy_sale_quote` |
| **La Huaca** | lahuaca | Activo — alto volumen | ERP contable / importación masiva facturas | `invoice_import_massive`, `contacto_consecutivo`*, contabilidad Odoo Mates |
| **Servicios Múltiples RC (SMRC)** | SMRC | Activo | ERP + Facturación Electrónica Panamá | `FE_HKA_OCI`, contabilidad community kit |
| **SANAGUA LODGE** | Sanadb | Activo | ERP + FE Panamá | `FE_HKA_OCI`; sin URL pública dedicada |
| **T & T Tourism Plus** | TTTourism | Activo | ERP turismo + FE | `FE_HKA_OCI`, `ets_weasy_sale_quote`* |
| **Relatic Panamá / Multiservicios TK** | relatic | Activo — baja actividad reciente | ERP + integración propia | `relatic_integration`* |
| **Modecosa** | — | **No presente** | — | Probablemente en otro servidor (OCI u otro) |
| **Rycom** | — | **No presente** | — | Probablemente en otro servidor |

\* Módulo instalado en BD pero **código ausente** en `/opt/odoo/custom-addons` — riesgo operativo.

---

## FASE 5 — Módulos EasyTech

Ruta producción: `/opt/odoo/custom-addons/`  
Copia desarrollo FE: `/home/admin/FE_HKA_OCI/` (versión más nueva que producción)

### Módulos propios EasyTech (en disco)

| Módulo | Versión (disco) | Cliente / uso | Estado | Repositorio | Función |
|---|---|---|---|---|---|
| **FE_HKA_OCI** | 18.0.1.1.0 | SMRC, Sanadb, TTTourism | Instalado en 3 BD | `git@github-fe-hka:shidalgo0925/FE_HKA_OCI.git` | Facturación Electrónica Panamá vía The Factory HKA |
| **Fact_Asp_Ebi** | 18.0.1.0.0 | — | En disco, **no instalado** | Local / sin remote confirmado | FE alternativa vía gateway ASP/EBI |
| **invoice_import_center** | 2.0 | — | En disco, **no instalado** | Local | Centro importación facturas Excel/CSV |
| **invoice_import_massive** | 1.0.0 | La Huaca | Instalado | Local | Importación masiva facturas |
| **carga_factura_automatizada** | 1.0 | — | En disco, **no instalado** | Local | Carga automatizada XLS/CSV |
| **repair_workshop** | 1.0 | — | En disco, **no instalado** | Local | Taller de reparación (joyería) |
| **whatsapp_center** | 1.0 | — | En disco, **no instalado** | Local | Centro mensajes WhatsApp en Odoo |
| **contact_report_list** | 1.0 | — | En disco, **no instalado** | Local | Listado contactos PDF |
| **cuentas_por_cobrar** | 1.0 | — | En disco, **no instalado** | Local | Reporte estado de cuenta / cobros |
| **corredor_fields** | 1.0 | — | En disco, **no instalado** | Local | Campos personalizados corredor |
| **charlie_shopbot** | 1.0 | — | En disco, **no instalado** | Local | Tienda + chatbot Charlie Pity |
| **simple_invoice_import** | — | — | Directorio **vacío** | — | Reservado / incompleto |

### Módulos solicitados — resultado búsqueda

| Módulo buscado | Resultado |
|---|---|
| `easytech_check_expense_reason` | **No encontrado** en disco ni en ninguna BD |
| Facturación Electrónica Panamá | `FE_HKA_OCI` (HKA) + `Fact_Asp_Ebi` (ASP/EBI, no desplegado) |
| Reporte Diario de Cobros | `cuentas_por_cobrar` y `om_account_daily_reports` (Odoo Mates) — no confirmado como "diario de cobros" |
| Taller | `repair_workshop` en disco; módulo estándar `repair` disponible |
| Educación | **Sin módulo custom**; solo apps estándar Odoo si se instalan |
| Eventos | **Sin módulo custom**; `event` estándar no instalado en clientes activos |
| Membresías | **Sin módulo custom**; `membership` estándar no instalado en clientes activos |

### Módulos instalados sin código en disco (huérfanos)

| Módulo | BD afectadas | Autor en BD | Riesgo |
|---|---|---|---|
| `ets_weasy_sale_quote` | Easydb, TTTourism | Easy Tech | Actualización/reinicio puede fallar |
| `contacto_consecutivo` | lahuaca | — | Idem |
| `relatic_integration` | relatic | Relatic | Idem |

### Terceros relevantes (no EasyTech, desplegados)

- **MuK Theme** (`muk_web_*`) — todas las BD activas
- **Odoo Mates Accounting** (`om_*`) — contabilidad community en clientes contables
- **OCA Web** — colección en `/opt/odoo/custom-addons/web/`

---

## FASE 6 — Facturación Electrónica

| Aspecto | Detalle |
|---|---|
| **Proveedor activo** | **The Factory HKA Corp.** — módulo `FE_HKA_OCI` |
| **Proveedor alternativo (no desplegado)** | ASP/EBI Gateway — módulo `Fact_Asp_Ebi` |
| **Clientes con FE activa** | SMRC (47 autorizados), Sanadb (37), TTTourism (3) |
| **Arquitectura** | Módulo Odoo → API HKA → DGI Panamá; documentos en modelo `hka_document` |
| **Dependencias Python** | `requests`, `PyJWT` |
| **Dependencias Odoo** | `base`, `product`, `account`, `contacts` |
| **Riesgos** | Producción en disco v18.0.1.1.0; dev copy en `/home/admin` v18.0.1.2.0 sin sincronizar; credenciales HKA en `res.company` / settings por BD |

---

## FASE 7 — Backups

| Tipo | Estado | Frecuencia | Destino | Observaciones |
|---|---|---|---|---|
| **Bases de datos PostgreSQL** | **NO automatizado** | — | — | **Riesgo crítico** — sin cron `pg_dump` detectado |
| **Código custom addons** | Manual | Único hallado: 2025-10-20 | `/home/admin/odoo18_custom_modules_20251020_021812.tar.gz` (79 MB) | Desactualizado (>7 meses) |
| **FE_HKA_OCI** | Git | Bajo demanda | GitHub `shidalgo0925/FE_HKA_OCI` | Backup local adicional `FE_HKA_OCI_backup_20260306` |
| **Filestore Odoo** | Sin backup dedicado | — | `/var/lib/odoo/filestore` (283 MB) | Incluye adjuntos de todas las BD |
| **EConverso** | Manual | 2026-02-23 | `/home/admin/apps/econverso_backup_20260223_2135.tar.gz` | App separada, no ERP |
| **Certificados SSL** | Certbot | Auto-renovación | Let's Encrypt | Válidos hasta 2026-07/08 |

---

## FASE 8 — Arquitectura ERP en el ecosistema EasyTech

```
TAMAL (217.216.80.159 — Contabo)
├── Nginx (443/80) — reverse proxy multi-tenant
│   ├── *.etsrv.site → Odoo :8069 (map host → db)
│   └── econverso.com → Gunicorn :5174 (no ERP)
├── Odoo 18 Community (única instancia)
│   ├── 6 BD producción + 1 laboratorio
│   ├── FE_HKA_OCI (3 clientes activos)
│   └── 48+ módulos en custom-addons
├── PostgreSQL 16
├── EConverso (WhatsApp / marketing — WAConnect lineage)
└── Clientes ERP dependientes
    ├── Easy Technology Services (Easydb)
    ├── La Huaca (lahuaca) ← mayor volumen
    ├── SMRC
    ├── SANAGUA LODGE (Sanadb)
    ├── T & T Tourism Plus
    └── Relatic / Multiservicios TK
```

### Papel de TAMAL

TAMAL es hoy el **único servidor Odoo productivo** identificado para clientes EasyTech en Contabo. Concentra:

- Multi-tenancy por subdominio (patrón heredado de OCI)
- Facturación electrónica Panamá (HKA)
- Módulos propios EasyTech
- ERP de al menos **6 clientes externos** + operación interna

**No aloja:** Modecosa, Rycom, Odoo 19 Enterprise.

---

## Riesgos operativos

| # | Riesgo | Severidad | Impacto si TAMAL cae |
|---|---|---|---|
| 1 | Sin backups automáticos de BD | **Crítico** | Pérdida de datos irreversible |
| 2 | Sin swap (7.8 GB RAM, picos Odoo+PG) | Alto | OOM kill de procesos |
| 3 | Single point of failure — 1 Odoo, 1 PG | **Crítico** | Todos los clientes ERP offline |
| 4 | Módulos huérfanos (código ausente) | Alto | Fallos en update/restart de módulos |
| 5 | Sanadb sin subdominio público | Medio | Dependencia de selector / acceso directo |
| 6 | Exposición a escaneo (logs con intentos exploit) | Medio | Superficie de ataque |
| 7 | Tar backup código desactualizado | Alto | Restauración incompleta |
| 8 | Credenciales en `/etc/odoo/odoo.conf` | Medio | Compromiso total si filtra |
| 9 | La Huaca: 5637 facturas en única BD | Alto | Mayor impacto de negocio |

---

## Criterio de éxito — respuestas

### 1. ¿Qué vive en TAMAL?

- Ubuntu 24.04 VPS Contabo
- Odoo 18 Community (única instancia)
- PostgreSQL 16 con 7 bases Odoo
- Nginx multi-tenant `*.etsrv.site`
- EConverso (app WhatsApp, puerto 5174)
- Módulos custom EasyTech + contabilidad community + tema MuK

### 2. ¿Qué clientes dependen de TAMAL?

Easy Technology Services, La Huaca, SMRC, SANAGUA LODGE, T & T Tourism Plus, Relatic/Multiservicios TK.  
Modecosa y Rycom **no** están en TAMAL.

### 3. ¿Qué módulos pertenecen a EasyTech?

Ver FASE 5 y `07_ERP/catalogo_modulos_easytech.md`. Núcleo: `FE_HKA_OCI`, importación facturas, taller, WhatsApp center, reportes contactos/cobros, corredor, shopbot.

### 4. ¿Qué ocurriría si TAMAL deja de existir mañana?

- **6 clientes ERP** sin acceso a facturación, inventario, contabilidad
- **3 clientes** sin emisión FE Panamá (SMRC, Sanadb, TTTourism)
- **La Huaca** pierde operación de 5 600+ facturas históricas
- Sin backups automáticos de BD, recuperación depende de tar manual oct-2025 y git de FE
- EConverso (econverso.com) también cae
- Certificados y DNS `*.etsrv.site` quedan huérfanos hasta migración

### 5. ¿Qué conocimiento ERP debe preservarse en Easy Wiki?

- Mapa host → BD (nginx `easydb-etsrv.conf`)
- Procedimiento alta subdominio (`procedimiento-odoo-subdominio-etsrv.txt`)
- Catálogo módulos EasyTech y estado por cliente
- Arquitectura FE HKA (flujo, dependencias, clientes activos)
- Inventario módulos huérfanos y deuda técnica
- Política de backups (actualmente inexistente — acción requerida)
- Diferencia TAMAL vs OCI (OCI cerrado; TAMAL = ERP Contabo)
- Repositorio FE: `shidalgo0925/FE_HKA_OCI`

---

## Backup Hub OCI — Fase 1 (conexión y prueba)

Destino: **OCI Backup Hub** (`40.233.1.138`, usuario `backupsrv`, ruta `/backups/tamal/`).  
Referencia hub: [[06_Arquitectura/servidores/OCI#Backup Hub]].

| Campo | Valor |
|---|---|
| **Estado Fase 1** | **VALIDADA** — 2026-06-05 |
| **Clave en TAMAL** | `/root/.ssh/id_ed25519_backup_oci` (modo `600`) |
| **Fingerprint clave** | `SHA256:dvIetad3hzt3V9PfSxLblfvF53xz7Hd11klUogjIVy4` |
| **Usuario destino** | `backupsrv@40.233.1.138` |
| **Ruta destino** | `/backups/tamal/` |
| **Cron / backup auto** | **No creado** (fuera de alcance Fase 1) |

### Instalación de llave (2026-06-05)

Copiada desde PC operador (Git Bash) en dos pasos:

1. `ubuntu@40.233.1.138:/home/ubuntu/.ssh/backup-hub/id_ed25519_tamal` → PC `/tmp/`
2. PC → `root@217.216.80.159:/root/.ssh/id_ed25519_backup_oci`

Permisos aplicados: `/root/.ssh` → `700`, clave → `600`.

### Pruebas ejecutadas desde TAMAL

**SSH:**

```text
hostname → instance-20251115-1442
whoami   → backupsrv
```

**Transferencia de prueba:**

| Método | Resultado | Notas |
|---|---|---|
| **rsync** | **No** | `remote command not found` — `backupsrv` sin `rsync` en PATH (clave `restrict`) |
| **scp** | **OK** | Archivo `tamal_to_oci_test.txt` recibido en `/backups/tamal/` |

**Evidencia en OCI** (vía `backupsrv`):

```text
-rw-r--r-- 1 backupsrv backupsrv 42 Jun  5 04:11 tamal_to_oci_test.txt
test TAMAL to OCI 2026-06-05 04:10:47 UTC
```

### Checklist Fase 1

| Paso | Estado |
|---|---|
| Copiar `id_ed25519_tamal` → `/root/.ssh/id_ed25519_backup_oci` | ✅ |
| Permisos `700` / `600` | ✅ |
| SSH `backupsrv@40.233.1.138` | ✅ |
| Transferencia archivo prueba | ✅ (`scp`; rsync pendiente instalar/enabled en OCI) |
| Evidencia en `/backups/tamal/` | ✅ |

### Nota Fase 2

Para backups con `rsync`, instalar `rsync` en OCI accesible para `backupsrv`, o usar **`scp`** en scripts de backup (compatible con claves `restrict`).

---

## Servicios adicionales (no ERP)

| Servicio | Puerto | Descripción |
|---|---|---|
| `econverso.service` | 5174 | EConverso — Gunicorn, `/home/admin/apps/econverso` |
| `nginx.service` | 80/443 | Reverse proxy |
| `fail2ban` | — | Solo jail `sshd` |

---

## Referencias locales

| Recurso | Ruta |
|---|---|
| Config nginx Odoo | `/etc/nginx/sites-available/easydb-etsrv.conf` |
| Config Odoo | `/etc/odoo/odoo.conf` |
| Procedimiento subdominio | `/home/admin/procedimiento-odoo-subdominio-etsrv.txt` |
| Rutas Contabo | `/home/admin/contabo-rutas.md` |
| Instrucciones Cursor equipo | `/home/shidalgo/apps/cursor-instrucciones/` |

---

*Inspección realizada en modo estricto (read-only). Sin reinicios, despliegues ni cambios en BD.*
