# CODITO — Servidor lógico (Relatic Panamá)

Documento maestro del host que opera la **instancia EN1 de Relatic Panamá** y co-aloja el laboratorio operativo EasyTech.  
**Auditoría en vivo** · inspección `2026-06-05` · sin cambios en servicios.

---

## Resumen ejecutivo

**CODITO** es el nombre lógico del VPS **Contabo** (`vmi3225509`) que aloja, entre otros silos Easy Technology, la **producción aislada de Relatic** (Easy NodeOne / EN1). Relatic consume la aplicación en `apps.relatic.org` y `miembros.relatic.org`, con base PostgreSQL dedicada y backups SQL diarios. El mismo equipo físico también ejecuta **dev, staging y prod** de Easy NodeOne, **IA local** (Open WebUI + LiteLLM + Ollama), EasyThesis, Easy Class One y landings estáticos — riesgo operativo documentado; el **propósito contractual de CODITO** es Relatic Panamá.

| Campo | Valor |
|-------|-------|
| **Cliente contractual** | Relatic Panamá |
| **Producto principal** | EN1 (Easy NodeOne) — silo `relatic` |
| **Estado operativo** | **Producción** (Relatic) + co-hosting EasyTech |
| **Responsable** | EasyTech |
| **Proveedor IaaS** | Contabo |
| **Hostname técnico** | `vmi3225509.contaboserver.net` |

**Conclusión rápida:** si CODITO desaparece mañana, **Relatic deja de operar de inmediato** y con él caen todos los demás servicios del VPS. Detalle de impacto, tiempos y pérdida de datos: [[00_Gobierno/disaster_recovery_codito]].

---

## Fase 1 — Inventario de hardware y red

Inspección directa en servidor · `2026-06-05`.

| Campo | Valor |
|-------|-------|
| **Proveedor** | Contabo |
| **VPS / ID** | `vmi3225509` *(plan comercial exacto: confirmar en panel Contabo)* |
| **CPU** | 16 vCPU — AMD EPYC (with IBPB) |
| **RAM** | 64 GiB (62 GiB usable) |
| **Disco** | ~581 GiB (`/dev/sda1`), **42 GiB usados (~8 %)** |
| **Sistema operativo** | Ubuntu 24.04.4 LTS (noble), kernel 6.8.0-111-generic |
| **IP pública** | `194.60.201.29` |
| **IP privada** | **N/A** — VPS sin VPC; red interna solo bridge Docker `172.17.0.0/16` (host `172.17.0.1`) |
| **Gateway** | `194.60.201.1` |

---

## Fase 2 — Inventario de aplicaciones

| Nombre | Función | Estado | Tecnología | Ruta | Dependencias |
|--------|---------|--------|------------|------|--------------|
| **EN1 Relatic** | Producción cliente Relatic (membresías, pagos, portal) | ✅ Activo | Flask + Gunicorn, PostgreSQL | `/opt/easynodeone/relatic/app` | `easynodeone-relatic.service`, BD `easynodeone_relatic`, Nginx, Cloudflare, PayPal, Google OAuth |
| **EN1 Dev** | Desarrollo Easy NodeOne | ✅ Activo | Flask + Gunicorn | `/opt/easynodeone/dev/app` | `easynodeone-dev.service`, BD `easynodeone_dev`, Nginx `appdev.easynodeone.com` |
| **EN1 Staging** | Preproducción EN1 | ✅ Activo | Flask + Gunicorn | `/opt/easynodeone/staging/app` | `easynodeone-staging.service`, BD `easynodeone_staging`, Nginx `apptst.easynodeone.com` |
| **EN1 Prod** | Producción otros clientes EN1 | ✅ Activo | Flask + Gunicorn | `/opt/easynodeone/prod/app` | `easynodeone-prod.service`, BD `easynodeone_prod`, Nginx `appprd.easynodeone.com` |
| **Relatic — landing** | Marketing estático `abril26.relatic.org` | ✅ Activo | Vite/React → Nginx estático | `/opt/easynodeone/landings/relatic-public` → `/var/www/abril26.relatic.org` | Repo `relatic-public`, Let's Encrypt |
| **RelaticV2** | Front experimental (no sustituye EN1) | ⚠️ Desplegado en disco, sin Nginx dedicado observado | Vite | `/opt/easynodeone/dev/relaticV2-github` | Repo GitHub `Gill3010/relaticV2` |
| **Open WebUI** | Chat IA interno | ✅ Activo (healthy) | Docker `ghcr.io/open-webui/open-webui:main` | Contenedor `open-webui` | Nginx `ai.easynodeone.com`, volúmen Docker, SQLite interno |
| **LiteLLM** | Proxy API LLM (Continue, `/v1/`) | ✅ Activo | Docker `litellm-en1:latest` | `/opt/ai-stack/litellm/` | Nginx `ai.easynodeone.com`, `api-ai.easynodeone.com`, config YAML |
| **Ollama** | Modelos LLM locales | ✅ Activo | systemd `ollama.service` | `/usr/local/bin/ollama` | Usado por LiteLLM/Open WebUI según config |
| **ai.easynodeone.com** | Portal IA (UI + API) | ✅ Activo | Nginx → Open WebUI + LiteLLM | `/etc/nginx/sites-enabled/ai.easynodeone.com` | TLS Let's Encrypt, upstream Docker |
| **Easy Wiki** | Documentación interna (Markdown) | ✅ Repo local | Git / Obsidian-style | `/opt/easynodeone/dev/EasyWiki` | **No servido por Nginx** en este host |
| **EasyThesis** | Plataforma tesis | ✅ Activo | Flask + Gunicorn | `/opt/easythesis/app` | `easythesis-dev.service`, BD `easythesis_dev`, Nginx `ethesis.site` |
| **Easy Class One** | LMS (dev/staging/prod) | ✅ Activo | Flask + Gunicorn | `/opt/easyclassone/{dev,staging,prod}/app` | systemd `easyclassone-*.service`, BD PostgreSQL, Nginx `eclassone.com` |
| **Landing EN1** | Sitio estático `easynodeone.com` | ✅ Activo | Nginx estático | `/var/www/easynodeone` | Build desde repo EN1 `landing/` |
| **Landing EClassOne** | Sitio estático | ✅ Activo | Nginx estático | `/var/www/eclassone` | Build Vite local |
| **Flask dev ad-hoc** | Servidor Flask puerto 5056 | ✅ Activo *(proceso huérfano)* | Flask | `/opt/easynodeone/dev/app` | `127.0.0.1:5056` — no Nginx |

---

## Fase 3 — PM2

**PM2 no está instalado** en CODITO (`which pm2` → no encontrado).

Las aplicaciones Python se gestionan con **systemd + Gunicorn**. Inventario equivalente:

| Aplicación (systemd) | Estado | Puerto | RAM (aprox.) | CPU acum. |
|----------------------|--------|--------|--------------|-----------|
| `easynodeone-relatic.service` | active | 9103 | ~436 MiB | alto (prod cliente) |
| `easynodeone-prod.service` | active | 9102 | ~395 MiB | medio |
| `easynodeone-dev.service` | active | 9101 | ~384 MiB | medio |
| `easynodeone-staging.service` | active | 9104 | ~364 MiB | bajo |
| `easythesis-dev.service` | active | 9201 | ~350 MiB | medio |
| `easyclassone-prod.service` | active | 9204 | ~278 MiB | medio |
| `easyclassone-dev.service` | active | 9202 | ~232 MiB | medio |
| `easyclassone-staging.service` | active | 9203 | ~190 MiB | medio |

*RAM vía `systemctl show … MemoryCurrent` · 2026-06-05.*

---

## Fase 4 — Docker

```text
docker ps -a   # 2026-06-05 — 2 contenedores, ambos Up ~3 semanas
```

| Contenedor | Imagen | Estado | Volúmenes / binds | Puertos (host) |
|------------|--------|--------|-------------------|----------------|
| `litellm` | `litellm-en1:latest` | running | `/opt/ai-stack/litellm/config.yaml` → `/app/proxy_server_config.yaml` (ro) | `127.0.0.1:4000→4000` |
| `open-webui` | `ghcr.io/open-webui/open-webui:main` | running (healthy) | volúmen `open-webui` → `/app/backend/data` (**~1,1 GiB**: `webui.db`, `vector_db`, `uploads`, `cache`) | `127.0.0.1:3000→8080` |

**Volúmenes Docker:** `open-webui` (local driver).

**Servicio adicional fuera de Docker:** `ollama.service` (systemd, ~469 MiB RSS).

---

## Fase 5 — Nginx

Fuentes: `/etc/nginx/sites-enabled/`, `/etc/nginx/conf.d/`.

| Dominio | Destino | SSL | Proxy |
|---------|---------|-----|-------|
| `apps.relatic.org`, `miembros.relatic.org` | Gunicorn `127.0.0.1:9103` | Let's Encrypt (`ssl-apps-relatic.conf`) | Sí → `easynodeone_relatic_app` |
| `abril26.relatic.org` | Estático `/var/www/abril26.relatic.org` | LE (`ssl-abril26-relatic.conf`) | No (SPA estática) |
| `appprd.easynodeone.com` | Gunicorn `127.0.0.1:9102` | LE (snippet prd-dev) | Sí |
| `appdev.easynodeone.com`, `*dev.easynodeone.com` | Gunicorn `127.0.0.1:9101` | LE | Sí |
| `apptst.easynodeone.com` | Gunicorn `127.0.0.1:9104` | LE (`ssl-apptst-easynodeone.conf`) | Sí |
| `easynodeone.com` | Estático `/var/www/easynodeone` | LE | No |
| `ai.easynodeone.com` | `/` → `127.0.0.1:3000` (Open WebUI); `/v1/` → `litellm_upstream`; `/health` → LiteLLM | LE | Sí |
| `api-ai.easynodeone.com` | `/v1/`, `/health` → LiteLLM; resto 404 | LE | Sí |
| `eclassone.com` | Estático `/var/www/eclassone` | LE | No |
| `appdev.eclassone.com` | Gunicorn `127.0.0.1:9202` | LE | Sí |
| `app.eclassone.com`, `apps.eclassone.com` | Gunicorn `127.0.0.1:9204` | HTTP only *(SSL pendiente en conf actual)* | Sí |
| `appstaging.eclassone.com` | Gunicorn `127.0.0.1:9203` | HTTP only | Sí |
| `ethesis.site`, `www.ethesis.site` | Gunicorn `127.0.0.1:9201` | LE | Sí |
| `ethesis.etsrv.site` | Gunicorn `127.0.0.1:9201` | LE | Sí |

**conf.d:**

- `00-forwarded-proto-map.conf` — respeta `X-Forwarded-Proto` (Cloudflare).
- `10-litellm-upstream.conf` — upstream `172.17.0.2:4000` *(IP Docker; cambia si se recrea contenedor)*.

---

## Fase 6 — Bases de datos

### PostgreSQL 16 (local, `127.0.0.1:5432`)

| Motor | BD | Tamaño | Aplicación | Criticidad |
|-------|-----|--------|------------|------------|
| PostgreSQL 16 | `easynodeone_relatic` | ~21 MB | EN1 Relatic | **CRÍTICA** |
| PostgreSQL 16 | `easynodeone_prod` | ~18 MB | EN1 Prod | ALTA |
| PostgreSQL 16 | `easynodeone_staging` | ~18 MB | EN1 Staging | MEDIA |
| PostgreSQL 16 | `easynodeone_dev` | ~21 MB | EN1 Dev | MEDIA |
| PostgreSQL 16 | `easynodeone_dev_relatic_clone` | ~15 MB | Clon pruebas | BAJA |
| PostgreSQL 16 | `easythesis_dev` | ~18 MB | EasyThesis | MEDIA |
| PostgreSQL 16 | `easyclassone_dev` | ~16 MB | ECO Dev | MEDIA |
| PostgreSQL 16 | `easyclassone_staging` | ~15 MB | ECO Staging | MEDIA |
| PostgreSQL 16 | `easyclassone_prod` | ~15 MB | ECO Prod | ALTA |

**Cluster total:** ~214 MiB en `/var/lib/postgresql/16/main`.

### SQLite (por silo EN1)

| Archivo | Silo | Uso |
|---------|------|-----|
| `instance/oauth_state.sqlite3` | dev, staging, prod, relatic | Estado OAuth |
| `instance/NodeOne.db` | dev, staging, prod, relatic | Datos auxiliares Flask |
| `instance/membership_legacy.db` | dev | Legacy |
| `webui.db` | Open WebUI (Docker vol.) | Usuarios, chats, config IA |

### MySQL / Redis

| Motor | Estado |
|-------|--------|
| **MySQL / MariaDB** | **No instalado / inactivo** |
| **Redis** | **No instalado** |

---

## Fase 7 — Repositorios Git

| Proyecto | Ruta | Remoto | Rama | Último commit |
|----------|------|--------|------|---------------|
| EN1 Dev | `/opt/easynodeone/dev/app` | `git@github.com:shidalgo0925/Easy-NodeOne.git` | `develop` | `2b3d585` · 2026-06-04 · docs EN1 |
| EN1 Staging | `/opt/easynodeone/staging/app` | `https://github.com/shidalgo0925/Easy-NodeOne.git` | `main` | `deaf1df` · 2026-06-04 · merge develop→staging |
| EN1 Prod | `/opt/easynodeone/prod/app` | `https://github.com/shidalgo0925/Easy-NodeOne.git` | `main` | `deaf1df` · 2026-06-04 |
| EN1 Relatic | `/opt/easynodeone/relatic/app` | `git@github.com:shidalgo0925/Easy-NodeOne.git` | `develop` | `5d78e1c` · 2026-06-03 · fix pagos |
| Landing Relatic | `/opt/easynodeone/landings/relatic-public` | `git@github.com:shidalgo0925/relatic-public.git` | `main` | `655a4aa` · 2026-04-27 |
| RelaticV2 | `/opt/easynodeone/dev/relaticV2-github` | `https://github.com/Gill3010/relaticV2.git` | `main` | `e085bad` · 2026-03-20 |
| Easy Wiki | `/opt/easynodeone/dev/EasyWiki` | `git@github.com:shidalgo0925/EasyWiki.git` | `main` | `b9b10b4` · 2026-06-05 |
| EasyThesis | `/opt/easythesis/app` | `git@github.com-easythesis:shidalgo0925/Ethesis.git` | `main` | `86ea0c5` · 2026-05-23 |
| Easy Class One | `/opt/easyclassone/*/app` | **Sin `.git` local** | — | Despliegue sin repo en disco |

**Nota:** silo Relatic en rama `develop` mientras la política operativa documenta `main`/`relatic` — ver Riesgos.

---

## Fase 8 — Backups existentes

| Qué | ¿Se respalda? | Frecuencia | Ubicación | Riesgo |
|-----|---------------|------------|-----------|--------|
| BD `easynodeone_relatic` | ✅ Sí | Diaria 02:00 | `/opt/easynodeone/backups/relatic_YYYY-MM-DD_HH-MM.sql` | Solo local |
| BD `easynodeone_prod` | ✅ Sí | Diaria 02:00 | `/opt/easynodeone/backups/prod_*.sql` | Solo local |
| Resto BD PostgreSQL | ❌ No | — | — | Pérdida total si cae VPS |
| Volcados `-Fc` históricos | ⚠️ Parcial | Único snapshot abr-2026 | `/var/backups/easynodeone/daily/*.dump` | Obsoleto |
| Uploads EN1 (`static/uploads`) | ❌ No | — | disco silo | prod ~128 MiB, relatic ~6 MiB |
| Open WebUI (`webui.db`, vectors) | ❌ No | — | volúmen Docker ~1,1 GiB | Irrecuperable sin backup |
| `.env` por silo | ❌ No | — | `/opt/easynodeone/{dev,staging,prod,relatic}/.env` | Secretos fuera de Git |
| Landings estáticos | ❌ No *(reconstruibles)* | — | `/var/www/*` | Rebuild desde Git |
| Config Nginx / TLS | ❌ No *(reconstruible)* | — | `/etc/nginx`, `/etc/letsencrypt` | Reemitir certs |
| Modelos Ollama | ❌ No | — | disco Ollama | Re-descarga |
| Easy Class One | ❌ No | — | — | Sin Git local |

**Script:** `/opt/easynodeone/scripts/backup-easynodeone.sh`  
**Cron:** `/etc/cron.d/easynodeone` → `0 2 * * * root …`  
**Log:** `/var/log/easynodeone-backup-sql.log`  
**Retención observada:** ~121 archivos, ~176 MiB total en `/opt/easynodeone/backups/` (sin rotación automática documentada).

**Diseño off-site (OCI):** alcance **producción crítica únicamente** — ver **Fase 9** · [[00_Gobierno/disaster_recovery_codito#9-plan-backup-off-site-oci-diseño]] · **sin implementar**.

---

## Fase 9 — Backup off-site OCI *(alcance aprobado · sin implementar)*

**Backup Hub:** OCI Object Storage · prefijo `backups/codito/`  
**Medición en vivo:** `2026-06-05` · CODITO `194.60.201.29`  
**Estado:** inventario + dimensionamiento · **no cron · no copias**

### 9.0 Clasificación oficial CODITO

```text
CODITO
│
├── PRODUCCIÓN CRÍTICA ──► backup OCI (fases CODITO-1…4)
│   ├── easynodeone_relatic
│   ├── easynodeone_prod
│   ├── .env Relatic + .env EN1 Prod
│   ├── uploads Relatic + uploads EN1 Prod
│   └── Open WebUI (datos, no cache)
│
├── ALTO (operativo, fuera de backup por ahora)
│   └── Open WebUI / IA — cubierto en fase CODITO-4
│
├── BAJO — NO backup (reconstruir desde Git)
│   ├── EN1 Dev · EN1 Staging
│   ├── Easy Class One · EasyThesis
│   └── LiteLLM · Ollama · laboratorios
│
└── LANDINGS — excluidos DR (protegidos por Git)
    └── easynodeone.com · eclassone.com · abril26.relatic.org · …
```

---

### 9.1 Inventario medido (solo valor de negocio)

#### PostgreSQL — producción crítica

| BD | Tamaño en cluster | Dump SQL diario *(observado 2026-06-05)* | Ruta dump local |
|----|-------------------|------------------------------------------|-----------------|
| **`easynodeone_relatic`** | **21 MB** (22 297 623 B) | **4,05 MiB** (4 244 756 B) | `/opt/easynodeone/backups/relatic_YYYY-MM-DD_HH-MM.sql` |
| **`easynodeone_prod`** | **18 MB** (18 889 751 B) | **0,89 MiB** (930 459 B) | `/opt/easynodeone/backups/prod_YYYY-MM-DD_HH-MM.sql` |

**Subtotal CODITO-1:** **~4,9 MiB/día** *(dumps actuales; con `gzip` estimado ~3,8–4,5 MiB/día)*.

#### `.env` — producción crítica (CODITO-2)

| Archivo | Ubicación | Tamaño |
|---------|-----------|--------|
| Relatic | `/opt/easynodeone/relatic/.env` | **1 259 B** (~1,2 KiB) |
| EN1 Prod | `/opt/easynodeone/prod/.env` | **534 B** |

**Subtotal CODITO-2:** **~1,8 KiB/día** *(cifrado o tarball; subir cifrado con `age`/GPG)*.

#### Uploads — producción crítica (CODITO-3)

| Ámbito | Ruta en CODITO | Tamaño medido |
|--------|----------------|---------------|
| **Relatic** | `/opt/easynodeone/relatic/app/static/uploads` | 3,14 MiB |
| **Relatic** | `/opt/easynodeone/relatic/app/uploads` | 2,62 MiB |
| **Relatic** | `/opt/easynodeone/relatic/uploads` | 0 |
| **EN1 Prod** | `/opt/easynodeone/prod/app/static/uploads` | **126,97 MiB** |
| **EN1 Prod** | `/opt/easynodeone/prod/app/uploads` | 0 |
| **EN1 Prod** | `/opt/easynodeone/prod/uploads` | 0 |

**Baseline total uploads (CODITO-3):** **132,73 MiB** (139 174 346 B) · **64 ficheros** en Relatic · mayor volumen en prod.

**Ingesta diaria tras baseline:** incremental (`rclone sync`); estimado **0,5–3 MiB/día** según actividad prod.

#### Docker Open WebUI (CODITO-4)

| Campo | Valor |
|-------|-------|
| Contenedor | `open-webui` |
| Volúmen Docker | `open-webui` |
| Ruta host | `/var/lib/docker/volumes/open-webui/_data` |
| **Tamaño total volúmen** | **1,04 GiB** (1 117 478 531 B) |
| `webui.db` *(respaldar)* | 548 KiB |
| `vector_db/` *(respaldar)* | 184 KiB |
| `uploads/` | 0 |
| `cache/` *(**excluir**)* | **1,04 GiB** — regenerable |

**Subtotal CODITO-4:** **~732 KiB/día** hoy · excluir `cache/`.

#### Fuera de alcance *(no medir para OCI)*

| Grupo | Recuperación |
|-------|--------------|
| EN1 Dev / Staging | `git clone` + venv + `systemctl` |
| Easy Class One · EasyThesis | Git + rebuild |
| LiteLLM | Config en `/opt/ai-stack/litellm/` · rebuild contenedor |
| Landings | Git (`relatic-public`, EN1 `landing/`, etc.) |

---

### 9.2 Estructura OCI (solo fases aprobadas)

```text
backups/codito/
├── postgres/
│   ├── relatic/YYYY/MM/DD/relatic.sql.gz      # CODITO-1
│   └── prod/YYYY/MM/DD/prod.sql.gz            # CODITO-1
├── config/
│   └── env/
│       ├── relatic.env.age                    # CODITO-2
│       └── prod.env.age                       # CODITO-2
├── uploads/
│   ├── relatic/                               # CODITO-3
│   └── en1-prod/                              # CODITO-3
├── docker/
│   └── open-webui/YYYY-MM-DD/                 # CODITO-4 (sin cache/)
│       ├── webui.db
│       └── vector_db/
└── logs/
    └── push-YYYY-MM-DD.log
```

Bucket propuesto: `easytech-backups` · retención sugerida: PG Relatic **90 d** · PG prod **60 d** · uploads **espejo** · WebUI **14 d**.

---

### 9.3 Dimensionamiento — backup diario real hacia OCI

| Fase | Contenido | 1.er día (baseline) | Cada día después |
|------|-----------|---------------------|------------------|
| **CODITO-1** | PG Relatic + prod | **4,9 MiB** | **4,9 MiB** *(objeto nuevo/día)* |
| **CODITO-2** | `.env` cifrados ×2 | **~2 KiB** | **~2 KiB** |
| **CODITO-3** | Uploads Relatic + prod | **132,7 MiB** | **0,5–3 MiB** *(delta)* |
| **CODITO-4** | Open WebUI sin cache | **0,7 MiB** | **~0,1 MiB** *(delta)* |
| **Total** | | **~138,3 MiB** | **~5,5–8,5 MiB** |

| Métrica | Valor |
|---------|-------|
| **Ingesta mes 1** *(baseline + 30 días)* | **~138 MiB + ~180 MiB** ≈ **~320 MiB** |
| **Ingesta mensual recurrente** *(mes 2+)* | **~165–255 MiB** |
| **Espacio OCI steady-state** *(retención PG + espejo uploads + WebUI)* | **~550–650 MiB** |
| **Bucket recomendado** | **5 GiB** *(margen corporativo; comparable a hub TAMAL)* |
| **Tiempo copia — día 1** | **~2–4 min** |
| **Tiempo copia — día típico** | **< 1 min** |
| **Coste OCI orientativo** | **5 GiB ≈ USD 0,13/mes** |

*Supuestos: uplink Contabo 100–500 Mbps; uploads con `rclone sync` (no full copy diaria); PG con retención por lifecycle.*

---

### 9.4 Roadmap (4 fases — diseño únicamente)

| Fase | Alcance | Criterio de éxito |
|------|---------|-------------------|
| **CODITO-1** | `easynodeone_relatic` + `easynodeone_prod` → `postgres/` | Restore en BD vacía desde OCI |
| **CODITO-2** | `.env` Relatic + prod cifrados → `config/env/` | Descifrado y arranque Gunicorn en host test |
| **CODITO-3** | Uploads Relatic + prod → `uploads/` | Checksum / conteo vs origen |
| **CODITO-4** | Open WebUI sin `cache/` → `docker/open-webui/` | Contenedor test lee `webui.db` restaurado |

**No incluido:** dev, staging, Easy Class One, EasyThesis, LiteLLM, nginx, landings.

**Prerrequisitos OCI:** bucket + IAM + clave API CODITO + clave cifrado `.env` fuera del bucket.

---

## Propósito, clasificación y dependencias

*(Tareas 10–14 — sin cambios sustantivos respecto a ficha anterior.)*

| Campo | Valor |
|-------|-------|
| **Nombre lógico** | CODITO |
| **Objetivo** | Operar **Relatic Panamá** (membresías, pagos, planes, portal miembros) |
| **Categoría** | **Producción** (subtipo: silo `/opt/easynodeone/relatic/`) |
| **Co-hosting** | Dev / Staging / Prod EN1, IA, EThesis, EClassOne en el **mismo metal** |

| Dependencia | Detalle |
|-------------|---------|
| DNS / Cloudflare | Dominios públicos; TLS Full strict |
| SMTP | Variables `MAIL_*` en `.env` por silo |
| Google OAuth, PayPal | Credenciales en `.env` Relatic |
| PostgreSQL local | Sin BD externa para Relatic |
| Contabo panel | Snapshots proveedor *por verificar* |

---

## Accesos operativos

*(Sin contraseñas ni claves.)*

| Acceso | Disponible | Notas |
|--------|------------|-------|
| SSH | Sí | Equipo EasyTech |
| sudo / root | Sí | Migraciones, systemd, Nginx, PostgreSQL |
| Git | Sí | Pull por silo; no editar prod a mano |
| Cloudflare | Sí (esperado) | DNS / proxy |
| Contabo | Sí | VM `vmi3225509` |

---

## Riesgos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| VPS compartido | Deploy erróneo afecta vecinos | Ventanas, ramas y `.env` por silo |
| Rama Relatic = `develop` | Desalineación con política `main` | Acordar rama única |
| Backup solo local | Pérdida VPS = pérdida backups | Plan OCI diseñado (Fase 9) — **implementación pendiente** |
| Open WebUI sin backup | Pérdida historial IA | Fase CODITO-4 — **pendiente** |
| Secretos solo en `.env` prod/relatic | No recuperables desde Git | Fase CODITO-2 — **pendiente** |

---

## Referencias

| Documento | Ruta |
|-----------|------|
| DR / impacto | [[00_Gobierno/disaster_recovery_codito]] |
| Backup off-site OCI | Fase 9 (este doc) · [[00_Gobierno/disaster_recovery_codito#9-plan-backup-off-site-oci-diseño]] |
| Inventario apps | `/opt/easynodeone/UBICACION-APPS.md` |
| Operación diaria | `/opt/easynodeone/EASYNODEONE-OPERACION-DIARIA.md` |
| Índice servidores | [[06_Arquitectura/servidores/README]] |

---

**Índice servidores:** [[06_Arquitectura/servidores/README]] · **Deploy EN1:** [[07_Operaciones/deploy]]
