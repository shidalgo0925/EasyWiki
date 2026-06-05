# TAMAL — Servidor ERP Principal EasyTech

| Campo | Valor |
|---|---|
| **Nombre interno** | TAMAL |
| **Hostname sistema** | `vmi3048421` / `vmi3048421.contaboserver.net` |
| **Proveedor** | Contabo (AS40021) |
| **Rol** | Servidor ERP principal multi-tenant Odoo 18 Community |
| **Estado inspección** | 2026-06-04 — DOCUMENTADO |
| **Backup Hub OCI** | Fases 1–3 ✅ · Fase 5 restore ✅ (Easydb + **La Huaca**) — 2026-06-05 |
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
| **Bases de datos PostgreSQL** | Script Fase 3 + **restore Fase 5** (Easydb + lahuaca) | Bajo demanda | TAMAL + OCI | **Sin cron** — backup **recuperable**; **Fase 4 autorizada** |
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

### Nota transferencia

Para backups con `rsync`, instalar `rsync` en OCI accesible para `backupsrv`, o usar **`scp`** en scripts de backup (compatible con claves `restrict`). Fase 2 usa **scp**.

---

## Backup Hub OCI — Fase 2 (PostgreSQL manual)

**Objetivo:** exportar base Odoo, transferir a OCI, verificar integridad. **Sin cron / sin automatización.**

### Estructura local TAMAL

| Ruta | Uso |
|---|---|
| `/backups/tamal/db/` | Dumps PostgreSQL |
| `/backups/tamal/logs/` | Logs futuros (vacío en Fase 2) |

### Backup validado — Easydb (2026-06-05)

| Campo | Valor |
|---|---|
| **Base** | `Easydb` (Easy Technology Services — interno) |
| **Archivo local** | `/backups/tamal/db/Easydb_2026-06-05.dump` |
| **Archivo OCI** | `/backups/tamal/Easydb_2026-06-05.dump` |
| **Formato** | PostgreSQL custom (`pg_dump -Fc`) |
| **Tamaño** | **9.7 MB** (TAMAL y OCI coinciden) |
| **Fecha dump** | 2026-06-05 06:14:07 CEST |
| **PostgreSQL origen** | 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1) |
| **TOC entries** | 11 513 |
| **Integridad** | `pg_restore --list` — **OK** (11 524 líneas, sin errores) |
| **Transferencia** | `scp` vía `/root/.ssh/id_ed25519_backup_oci` → `backupsrv@40.233.1.138:/backups/tamal/` |

### Procedimiento manual (referencia)

```bash
# 1. Dump (usuario postgres; salida en path root)
sudo sh -c 'sudo -u postgres pg_dump -Fc Easydb > /backups/tamal/db/Easydb_$(date +%F).dump'

# 2. Integridad local
pg_restore --list /backups/tamal/db/Easydb_$(date +%F).dump | head

# 3. Transferir a OCI
scp -i /root/.ssh/id_ed25519_backup_oci -o IdentitiesOnly=yes \
  /backups/tamal/db/Easydb_$(date +%F).dump \
  backupsrv@40.233.1.138:/backups/tamal/

# 4. Verificar en OCI
ssh -i /root/.ssh/id_ed25519_backup_oci -o IdentitiesOnly=yes \
  backupsrv@40.233.1.138 'ls -lh /backups/tamal/*.dump'
```

**Nota:** `postgres` no escribe directo en `/backups/tamal/db/` (permisos root); usar redirección con `sudo sh -c` como arriba.

### Checklist Fase 2

| Paso | Estado |
|---|---|
| Estructura `/backups/tamal/{db,logs}` | ✅ |
| Dump `Easydb` generado | ✅ |
| `pg_restore --list` sin errores | ✅ |
| Transferencia scp → OCI | ✅ |
| Dump visible en OCI (tamaño coincide) | ✅ |
| Cron / automatización | ❌ No creado (deliberado) |

---

## Backup Hub OCI — Fase 2.5 (inventario de recuperación)

**Objetivo:** medir tamaño real de dump por cliente, validar integridad (`pg_restore --list`) y transferir a OCI. **Sin cron, sin script, sin restauración completa** (eso es Fase 5).

**Fecha inventario:** 2026-06-05  
**Formato:** `pg_dump -Fc` · PostgreSQL 16.14  
**Destino OCI:** `/backups/tamal/` (74 MB total en hub)

### Tabla inventario — bases producción

| Base | Cliente | Tamaño dump | Bytes | TOC entries | `pg_restore --list` | En OCI |
|---|---|---:|---:|---:|---|---|
| **Easydb** | Easy Technology Services | 9.7 MB | 10 155 332 | 11 524 | ✅ Sí | ✅ |
| **lahuaca** | La Huaca | 16 MB | 16 674 962 | 13 342 | ✅ Sí | ✅ |
| **SMRC** | Servicios Múltiples RC | 13 MB | 12 773 841 | 10 886 | ✅ Sí | ✅ |
| **Sanadb** | SANAGUA LODGE | 9.5 MB | 9 899 244 | 11 122 | ✅ Sí | ✅ |
| **TTTourism** | T & T Tourism Plus | 9.7 MB | 10 079 648 | 11 353 | ✅ Sí | ✅ |
| **relatic** | Relatic / Multiservicios TK | 17 MB | 17 702 037 | 13 336 | ✅ Sí | ✅ |
| **TOTAL (6 bases prod.)** | — | **~74 MB** | **77 285 064** | — | — | ✅ |

**Excluida deliberadamente:** `odoo18` (laboratorio/demo).

### Hallazgos clave

| Métrica | Valor | Implicación |
|---|---|---|
| **Total dumps producción** | ~74 MB / día | OCI: espacio mínimo; retención 30 días ≈ 2.2 GB |
| **Mayor dump** | relatic (17 MB) | No es La Huaca — a pesar de 5 637 facturas, `lahuaca` comprime a 16 MB |
| **Menor dump** | Sanadb (9.5 MB) | Clientes similares en rango 9–10 MB |
| **Tiempo dump 6 BD** | ~21 s | Carga baja en TAMAL |
| **Tiempo transferencia scp** | ~11 s | Ancho de banda suficiente para Fase 4 nocturna |
| **BD vs dump** | lahuaca 121 MB → 16 MB dump | Ratio compresión ~7.5× (custom format `-Fc`) |

**Conclusión:** el volumen ERP de EasyTech en TAMAL es **moderado**. Una política de retención diaria + 30/90 días en OCI es viable sin costo de almacenamiento significativo. La Huaca **no** requiere estrategia especial por tamaño (sí por criticidad de negocio).

### Archivos en TAMAL y OCI (2026-06-05)

```text
/backups/tamal/db/Easydb_2026-06-05.dump      9.7 MB
/backups/tamal/db/lahuaca_2026-06-05.dump     16 MB
/backups/tamal/db/SMRC_2026-06-05.dump        13 MB
/backups/tamal/db/Sanadb_2026-06-05.dump     9.5 MB
/backups/tamal/db/TTTourism_2026-06-05.dump  9.7 MB
/backups/tamal/db/relatic_2026-06-05.dump     17 MB
```

Mismos archivos en `backupsrv@40.233.1.138:/backups/tamal/`.

### Checklist Fase 2.5

| Paso | Estado |
|---|---|
| Dump las 6 bases producción | ✅ |
| `pg_restore --list` sin errores (todas) | ✅ |
| Transferencia scp → OCI (todas) | ✅ |
| Tamaños coinciden TAMAL = OCI | ✅ |
| Tabla inventario documentada | ✅ |
| Restauración completa probada | ✅ **Fase 5** (Easydb + lahuaca) |
| Script `backup_postgresql_tamal.sh` | ✅ **Fase 3** |
| Cron 02:00 / 03:00 / 04:00 | **Autorizado Fase 4** — pendiente implementar |

### Roadmap backup TAMAL

| Fase | Alcance | Estado |
|---|---|---|
| **2** | Demo manual Easydb | ✅ |
| **2.5** | Inventario tamaños todas las bases prod. | ✅ |
| **3** | Script `backup_postgresql_tamal.sh` (6 bases → carpeta `YYYY-MM-DD/`) | ✅ |
| **4** | Automatización: 02:00 dump · 03:00 scp OCI · 04:00 verificación | **Autorizada** — pendiente implementar |
| **5** | **Prueba restauración real** — backup no existe hasta validar recover | ✅ Easydb + **lahuaca** |

---

## Backup Hub OCI — Fase 3 (script manual)

**Objetivo:** unificar dump + validación + transferencia OCI en un script ejecutable manualmente. **Sin cron.**

### Script

| Campo | Valor |
|---|---|
| **Ruta** | `/usr/local/bin/backup_postgresql_tamal.sh` |
| **Ejecución** | `sudo /usr/local/bin/backup_postgresql_tamal.sh` |
| **Usuario** | **root** (requerido: clave SSH, paths backup) |
| **Bases incluidas** | Easydb, lahuaca, SMRC, Sanadb, TTTourism, relatic |
| **Excluida** | `odoo18` (laboratorio) |
| **Formato dump** | `pg_dump -Fc` |
| **Validación** | `pg_restore --list` antes de cada `scp` |
| **Transferencia** | `scp` (no rsync) |
| **Fallo por base** | Registra error, continúa con las demás |
| **Retención** | No elimina dumps anteriores |

### Rutas

| Destino | Ruta |
|---|---|
| Dumps locales | `/backups/tamal/db/YYYY-MM-DD/{Base}.dump` |
| Log | `/backups/tamal/logs/backup_postgresql_tamal_YYYY-MM-DD.log` |
| OCI | `backupsrv@40.233.1.138:/backups/tamal/YYYY-MM-DD/` |
| Clave SSH | `/root/.ssh/id_ed25519_backup_oci` |

### Flujo del script

1. Crear carpeta diaria local y remota (OCI).
2. Por cada base: `pg_dump -Fc` → validar `pg_restore --list` → `scp` a OCI.
3. Registrar tamaño, TOC entries y resultado por base.
4. Resumen final en log y stdout.
5. Exit code `0` si todas OK; `1` si alguna falló.

### Primera ejecución validada (2026-06-05)

| Campo | Valor |
|---|---|
| **Inicio** | 06:21:10 CEST |
| **Duración** | ~33 s |
| **Resultado** | **6/6 OK** — 0 fallos |
| **Tamaño total** | 74 MiB (77 285 064 bytes) |
| **Local** | `/backups/tamal/db/2026-06-05/` (6 archivos `.dump`) |
| **OCI** | `/backups/tamal/2026-06-05/` (6 archivos `.dump`) |
| **Log** | `/backups/tamal/logs/backup_postgresql_tamal_2026-06-05.log` |
| **Dumps Fase 2/2.5** | **Preservados** en `/backups/tamal/db/*.dump` y `/backups/tamal/*.dump` (OCI raíz) |

### Checklist Fase 3

| Paso | Estado |
|---|---|
| Script en `/usr/local/bin/backup_postgresql_tamal.sh` | ✅ |
| Ejecución manual 6 bases | ✅ |
| `pg_restore --list` antes de scp | ✅ |
| Transferencia OCI en subcarpeta diaria | ✅ |
| Log generado | ✅ |
| Dumps anteriores no borrados | ✅ |
| Cron / systemd timer | ❌ No creado (deliberado) |
| Odoo / PostgreSQL sin cambios | ✅ |

---

## Backup Hub OCI — Fase 5 (restauración real)

**Objetivo:** confirmar que un dump generado por el proceso de backup es **recuperable** en PostgreSQL. **Sin conectar Odoo, sin nginx, sin cron.**

### Prueba 1 — Easydb (2026-06-05)

| Campo | Valor |
|---|---|
| **Archivo dump** | `/backups/tamal/db/2026-06-05/Easydb.dump` (9.7 MB) |
| **Base temporal** | `Easydb_restore_test_20260605` |
| **Duración restore** | ~34 s · exit **0** |
| **Base temporal final** | **Eliminada** |

| Check | Original | Restaurada | OK |
|---|---:|---:|---|
| Tamaño BD | 62 MB | 59 MB | ✅ ~95% |
| Tablas `public` | 580 | 580 | ✅ |
| `res_company` / `res_users` | 1 / 7 | 1 / 7 | ✅ |
| `ir_module_module` | 703 | 703 | ✅ |
| `account_move` | 12 | 12 | ✅ |
| Empresa | Easy Technology Services - TML | Idem | ✅ |

Log: `/backups/tamal/logs/restore_easydb_test_2026-06-05.log`

### Prueba 2 — lahuaca / La Huaca (2026-06-05)

**Motivo:** cliente más crítico por volumen operativo (~5 900 facturas). Validación final antes de cron.

| Campo | Valor |
|---|---|
| **Archivo dump** | `/backups/tamal/db/2026-06-05/lahuaca.dump` (16 MB) |
| **Base temporal** | `lahuaca_restore_test_20260605` |
| **Comando restore** | `pg_restore -d lahuaca_restore_test_20260605 --no-owner --no-acl` |
| **Duración restore** | ~45 s · exit **0** |
| **Base original `lahuaca`** | **No modificada** |
| **Base temporal final** | **Eliminada** |

| Check | Original | Restaurada | OK |
|---|---:|---:|---|
| Tamaño BD | 121 MB | 120 MB | ✅ ~99% |
| Tablas `public` | 658 | 658 | ✅ |
| `res_company` / `res_users` | 1 / 6 | 1 / 6 | ✅ |
| `ir_module_module` | 703 | 703 | ✅ |
| `account_move` | 5 968 | 5 968 | ✅ |
| `account_move` posted | 5 954 | 5 954 | ✅ |
| Empresa | La Huaca | La Huaca | ✅ |

Log: `/backups/tamal/logs/restore_lahuaca_test_2026-06-05.log`

### Restricciones respetadas (ambas pruebas)

- ❌ No se tocó ninguna base productiva (escritura)
- ❌ No se modificó Odoo, nginx ni módulos
- ❌ No se publicó subdominio ni acceso navegador
- ✅ Bases temporales eliminadas al cerrar cada prueba

### Checklist Fase 5

| Paso | Easydb | lahuaca |
|---|---|---|
| Base temporal + `pg_restore` exit 0 | ✅ | ✅ |
| Tablas y conteos = original | ✅ | ✅ |
| Facturas validadas | 12 | ✅ 5 968 |
| Odoo no conectado | ✅ | ✅ |
| Base temporal eliminada | ✅ | ✅ |

### Conclusión

Pipeline **export → OCI → restore** validado en **Easydb** (control) y **lahuaca** (cliente crítico). **Fase 4 (cron diario) autorizada** para implementación. Resto de bases prod. con `--list` OK; restore puntual opcional.

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
