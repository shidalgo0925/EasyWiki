# OCI — Servidor lógico (Producción IA / Landing Pages)

Documento maestro del host **Oracle Cloud Infrastructure (OCI)** de Easy Technology Services.  
Actualizado tras inspección en servidor · junio 2026 · **revisión de cierre y backup Git**.

---

## Resumen ejecutivo

**OCI** es el nombre lógico de la instancia **Oracle Cloud A1.Flex** (`instance-20251115-1442`) que aloja **landing pages y sitios web de clientes EasyTech**, herramientas internas ligeras (módulos Odoo en desarrollo, scripts) y **Ollama** con el modelo `mistral:latest` para inferencia local. **No** aloja el stack principal de Producción IA (`ai.easynodeone.com`, Open WebUI, LiteLLM) — ese stack vive en el VPS **Contabo** documentado en [[06_Arquitectura/servidores/CODITO]].

Si este servidor dejara de existir mañana: caerían los sitios públicos `biconsultingpma.com`, `mustangbasketacademy.online`, `detailingserviceve.site` y los subdominios `*.etsrv.site` servidos aquí; se perdería Ollama local y las BDs PostgreSQL locales (`infomobile`, `onepercent_db`) sin backup documentado; **no** afectaría directamente EN1/Relatic ni el portal IA en Contabo.

| Campo | Valor |
|-------|-------|
| **Cliente** | EasyTech / interno + sitios de clientes (BI Consulting, Mustang, Detailing VE, AA Transporte, Refrigeración SJ) |
| **Producto principal** | Hosting de **landing pages** y APIs de captación de leads |
| **Estado operativo** | **Producción** (sitios cliente) + componentes IA **locales** (Ollama) |
| **Responsable** | EasyTech |
| **Proveedor IaaS** | **Oracle Cloud Infrastructure (OCI)** |
| **Hostname técnico** | `instance-20251115-1442` |
| **IP pública** | `40.233.1.138` |
| **IP privada (VCN)** | `10.0.0.53/24` (`enp0s6`) |

---

## Tarea 10 – Propósito del servidor

| Campo | Valor |
|-------|-------|
| **Nombre lógico** | OCI |
| **Objetivo** | Alojar **landing pages**, sitios estáticos y APIs de contacto/leads para clientes EasyTech; nodo auxiliar de **IA local** (Ollama); laboratorio ligero de módulos Odoo/scripts |
| **Cliente** | EasyTech (interno) + clientes con landings desplegadas |
| **Estado** | **Producción** (sitios públicos activos). La etiqueta histórica «Producción IA» aplica de forma **parcial**: solo Ollama en este metal; el stack IA productivo está en **CODITO/Contabo**. |
| **Responsable** | EasyTech |
| **Fecha de creación** | **~15 nov 2025** (hostname `instance-20251115-1442`; migración documentada desde instancia OCI **E5** → **A1.Flex** en `/home/ubuntu/docs/documentacion/`) |

### ¿Por qué existe?

- Separar **landings y sitios ligeros** de clientes en infraestructura OCI (Free Tier / A1.Flex), sin competir por recursos con EN1 y el stack IA en Contabo.
- Servir sitios con **Nginx + Certbot** y APIs Flask mínimas para formularios anti-spam.
- Ofrecer **inferencia LLM local** vía Ollama (modelo `mistral`) para pruebas o cargas internas sin depender de APIs externas en este host.

### ¿Qué problema resuelve?

- Publicación rápida de **marketing sites** bajo dominios propios o subdominios `etsrv.site`.
- Captación de leads (BI Consulting, Refrigeración SJ) con validación anti-spam y envío SMTP.
- Punto de despliegue independiente de la instancia Contabo (CODITO), reduciendo blast radius frente a EN1.

---

## Tarea 14 – Clasificación

| Campo | Valor |
|-------|-------|
| **Categoría** | **Producción** |
| **Subtipo** | Landing Pages + APIs de leads + **IA local auxiliar** (Ollama) |
| **Nota** | No confundir con «Producción IA» completa (Open WebUI / LiteLLM / `ai.easynodeone.com`) → ver **Notas de arquitectura** |

### Evaluación estratégica

| Rol | ¿Aplica en OCI? | Justificación |
|-----|-----------------|---------------|
| **Producción** | **Sí** | Sitios cliente con tráfico real y TLS activo |
| **Landing Pages** | **Sí** | Función principal observada (5 vhosts Nginx) |
| **IA** | **Parcial** | Ollama + `mistral:latest` local; sin Open WebUI/LiteLLM/Docker |
| **Marketing** | **Sí** | Landings de captación y presencia web |
| **Laboratorio** | **Parcial** | `proyectos/relatic_integration_dev`, `hka_test`, módulos Odoo sin systemd prod |
| **Centro de operaciones futuro** | **No hoy** | Sin Easy Operator, sin Easy Wiki desplegada aquí, sin orquestación central |

**Conclusión:** OCI es hoy un **nodo de producción para landings y micro-APIs**, con **IA local experimental** (Ollama). El rol de «Producción IA» corporativa sigue en **CODITO (Contabo)** hasta migración explícita.

---

## Notas de arquitectura (relación con otros servidores)

| Elemento | ¿En OCI? | ¿En otro host? |
|----------|----------|----------------|
| `ai.easynodeone.com` | **No** | **CODITO** — `vmi3225509` (Contabo) |
| `api-ai.easynodeone.com` | **No** | **CODITO** *(por confirmar en ficha)* |
| `appprd.easynodeone.com` | **No** (solo enlace HTML) | **CODITO / Spaguetti** — EN1 prod |
| Open WebUI / LiteLLM | **No** | **CODITO** — `/opt/ai-stack` |
| EN1 / Relatic | **No** | **CODITO** |
| Ollama `mistral:latest` | **Sí** (`0.0.0.0:11434`) | Consumidor autorizado: **`vmi3119011`** (`95.111.244.137`, Contabo) vía UFW |
| Módulos Odoo (`relatic_integration_dev`, `ets_*`) | **Desarrollo en disco** | Destino deploy: **TAMAL** *(ficha pendiente)* |
| Easy Wiki (prod) | **No** — clon de trabajo en `/home/ubuntu/EasyWiki` | **CODITO** — `/opt/easynodeone/dev/EasyWiki` |
| Refrigeración SJ → EN1 webhook | Código listo (`en1WebhookUrl`) | **Inactivo** (`''`) — futuro **CODITO/EN1** |

**CODITO permanece cerrado** (ficha completa). Esta ficha enlaza dependencias sin duplicar contenido de CODITO.

---

## Infraestructura

| Recurso | Valor observado |
|---------|-----------------|
| **CPU** | 4 vCPU (`aarch64`) |
| **RAM** | 23 GiB (~22 GiB disponibles en inspección) |
| **Disco** | 45 GB (`/dev/sda1`), ~34 % uso · **~30 GB libres** (jun 2026) |
| **Espacio reservado backups** | **~25–30 GB** disponibles bajo `/backups` *(sin cuota dura; prod ~16 GB en uso)* |
| **Swap** | 0 B (sin swap configurado) |
| **Sistema operativo** | Ubuntu 22.04.5 LTS (Jammy), kernel `6.8.0-1047-oracle` |
| **Arquitectura** | **ARM64** (A1.Flex) |
| **Shape OCI** | A1.Flex *(inferido por docs internos de migración E5 → A1.Flex)* |
| **Agente cloud** | `oracle-cloud-agent` (snap), `unified-monitoring-agent` en `/opt` |
| **Firewall host** | **UFW activo** — ver sección **UFW** |

### UFW (firewall en host)

| Puerto | Acción | Origen | Notas |
|--------|--------|--------|-------|
| 22/tcp | ALLOW | Anywhere | SSH |
| 80/tcp | ALLOW | Anywhere | HTTP → redirect TLS |
| 443/tcp | ALLOW | Anywhere | HTTPS (Nginx) |
| 8069/tcp | ALLOW | Anywhere | Legacy `detailing-landing` — **riesgo**; Nginx ya sirve el sitio |
| 11434/tcp | ALLOW | **`95.111.244.137`** únicamente | Ollama API — host remoto `vmi3119011.contaboserver.net` |

Complementa (no sustituye) las **OCI Security Lists** en consola Oracle.

---

## Dominios

| Dominio | Uso | SSL | Proxy / DNS |
|---------|-----|-----|-------------|
| `biconsultingpma.com` / `www` | BI Consulting (Flask vía Nginx) | Let's Encrypt (Certbot) | A record → `40.233.1.138` *(sin proxy Cloudflare observado en resolución)* |
| `mustangbasketacademy.online` / `www` | Landing estática (Vite `dist`) | Let's Encrypt | *Confirmar registrador / Cloudflare en runbook* |
| `detailingserviceve.site` / `www` | Landing estática | Let's Encrypt | *Confirmar registrador* |
| `aatransporte.etsrv.site` | Landing AA Transporte | Let's Encrypt | **Cloudflare** proxy ON → IP anycast CF |
| `refrigeracionsj.etsrv.site` | Landing + API `/api/` | Let's Encrypt | **Cloudflare** proxy ON → zona `etsrv.site` |

**Certificados Let's Encrypt activos** (`/etc/letsencrypt/live/`): `aatransporte.etsrv.site`, `biconsultingpma.com`, `detailingserviceve.site`, `mustangbasketacademy.online`, `refrigeracionsj.etsrv.site`.

Renovación: `certbot.timer` / cron estándar Certbot.

---

## Aplicaciones

| Aplicación | Función | Tecnología | Estado | Responsable | Ruta / repo |
|------------|---------|------------|--------|-------------|-------------|
| **BI Consulting** | Sitio corporativo + formulario contacto anti-spam | Flask + Gunicorn, reCAPTCHA | **Producción** | EasyTech / cliente BI | `/home/ubuntu/proyectos/BICONsulitng` · `git@github-biconsulting:shidalgo0925/biconsultingpma.git` |
| **Mustang Basketball Academy** | Landing deportiva | HTML estático (`dist`) | **Producción** | EasyTech / cliente | `/home/ubuntu/MustangBaskAca` · `git@github-mustang:shidalgo0925/Mustang-Bastketball-.git` |
| **Detailing Service VE** | Landing + reservas (estático) | HTML/CSS/JS | **Producción** | EasyTech / cliente | `/home/ubuntu/DetailingServicesVE` · `git@github.com:shidalgo0925/DetailingserviceVE.site.git` |
| **AA Transporte** | Landing transporte | HTML estático | **Producción** | EasyTech / cliente | `/home/ubuntu/aa-transporte-landing` *(repo Git pendiente aprobación)* |
| **Refrigeración SJ** | Landing + API leads | HTML + Flask API | **Producción** | EasyTech / cliente | `/home/ubuntu/RefrigeracionSJ` (+ `api/`) *(repo Git pendiente aprobación)* |
| **Ollama** | Inferencia LLM local | Ollama + `mistral:latest` (~4.4 GB) | **Activo** (sin UI web documentada) | EasyTech | systemd `ollama.service` |
| **relatic_integration_dev** | Módulo Odoo (integración) en desarrollo | Python/Odoo | **No producción** | EasyTech | `/home/ubuntu/proyectos/relatic_integration_dev` |
| **invoice_import_massive_git** | Utilidad importación facturas | Python | **No producción** *(sin systemd)* | EasyTech | `/home/ubuntu/proyectos/invoice_import_massive_git` |
| **ets_report_studio / ets_weasy_sale_quote** | Módulos Odoo EasyTech | Python | **No producción** | EasyTech | `/home/ubuntu/ets_*` |
| **hka_test** | Pruebas facturación HKA | Python | **Laboratorio** | EasyTech | `/home/ubuntu/proyectos/hka_test` |
| **infomobile** *(legado)* | App móvil (BD huérfana) | PostgreSQL | **Retirado** — sin servicio | EasyTech | BD `infomobile` (`users`, `devices`) |
| **onepercent** *(legado)* | App TEA / gamificación (BD huérfana) | PostgreSQL | **Retirado** — sin servicio | EasyTech | BD `onepercent_db` |

**Redirect raíz:** `/home/ubuntu/index.html` redirige a `DetailingServicesVE/`.

**Enlace cross-server (Detailing → EN1):** `index.html` referencia `https://appprd.easynodeone.com/profile` (EN1 prod en **CODITO**).

**Histórico retirado en este host:** Odoo y apex `etsrv.site` fueron eliminados del servidor; subdominios `*.etsrv.site` activos apuntan solo a landings actuales. Docs legacy en `/home/ubuntu/docs/documentacion/`.

---

## Servicios (systemd / puertos)

| Servicio | Unidad systemd | Puerto | Backend |
|----------|----------------|--------|---------|
| **Nginx** | `nginx.service` | 80, 443 | Reverse proxy / estáticos |
| **BI Consulting** | `biconsulting.service` | `127.0.0.1:5000` | Gunicorn → `/home/ubuntu/proyectos/BICONsulitng` |
| **Refrigeración SJ API** | `refrigeracionsj-api.service` | `127.0.0.1:5001` | Gunicorn → `/home/ubuntu/RefrigeracionSJ/api` |
| **Detailing landing** *(legacy)* | `detailing-landing.service` | `0.0.0.0:8069` | `python3 -m http.server` — **WorkingDirectory incorrecto** (`DetailingServiceVE` no existe); Nginx sirve estático sin este puerto |
| **Ollama** | `ollama.service` | `0.0.0.0:11434` | `/usr/local/bin/ollama serve` |
| **PostgreSQL 14** | `postgresql@14-main.service` | `127.0.0.1:5432` | BDs: `infomobile`, `onepercent_db` |
| **SSH** | `ssh.service` | 22 | Acceso operativo |
| **OCI monitoring** | `unified-monitoring-agent.service` | — | Métricas/logs hacia OCI |

### Capas de software

| Capa | Componente | Versión / notas |
|------|------------|-----------------|
| Proxy | **Nginx** | 1.18.0 (Ubuntu) |
| App | **Python 3.10** + Gunicorn | Flask en BI Consulting y Refrigeración SJ |
| App | **Node.js** | v20.18.2 *(build Mustang; sin PM2)* |
| IA | **Ollama** | Modelo `mistral:latest` |
| BD | **PostgreSQL 14** | Local; uso productivo de BDs no confirmado en apps activas |
| Contenedores | **Docker** | **No instalado / no en uso** |
| Proceso Node | **PM2** | **No** |
| Preview HTTP | `python3 -m http.server` | **8765** → `aa-transporte-landing` · **8780** → `RefrigeracionSJ` · **8070** → `DetailingServicesVE` (127.0.0.1) — sin Nginx; **riesgo de exposición** |
| Firewall | **UFW** | Ver tabla **UFW** en Infraestructura |

---

## Tarea 11 – Dependencias

| Dependencia | ¿OCI? | Detalle |
|-------------|-------|---------|
| **DNS** | **Sí** | Dominios propios + subdominios `*.etsrv.site` (zona gestionada en **Cloudflare** según comentarios Nginx y docs en `/home/ubuntu/docs/documentacion/SOLUCION_DNS_CLOUDFLARE.md`) |
| **Cloudflare** | **Sí** (parcial) | Proxy activo en `aatransporte.etsrv.site`, `refrigeracionsj.etsrv.site` (IPs anycast `104.21.x`, `172.67.x`). `biconsultingpma.com` resuelve directo a `40.233.1.138`. |
| **SMTP / correo** | **Sí** | BI Consulting: SMTP vía variables en systemd override; Refrigeración SJ: `EnvironmentFile` en `smtp.env` — **sin copiar valores aquí** |
| **APIs externas** | **Sí** | **Google reCAPTCHA** (BI Consulting); posible relay SMTP del proveedor de correo del cliente |
| **APIs IA externas** | **No observado** | Sin OpenAI/Anthropic en este host; Ollama es local |
| **Bases de datos** | **Local** | PostgreSQL `127.0.0.1:5432` — `infomobile`, `onepercent_db` *(sin vínculo claro con apps Nginx activas)* |
| **CODITO / Contabo** | **Sí** | Stack IA + EN1; enlace funcional Detailing → `appprd.easynodeone.com` |
| **TAMAL** | **Sí** (dev) | Módulos Odoo desarrollados en OCI, desplegados en TAMAL |
| **vmi3119011 (Contabo)** | **Sí** | Único origen UFW permitido para Ollama `:11434` |
| **Let's Encrypt / Certbot** | **Sí** | TLS en todos los vhosts públicos |
| **OCI Security Lists** | **Sí** | Puertos 22, 80, 443 documentados en `docs/documentacion/INSTRUCCIONES_SECURITY_LISTS.md` |
| **UFW (host)** | **Sí** | Reglas locales — ver sección **UFW** |

---

## Tarea 12 – Accesos operativos

*(Sin contraseñas ni claves.)*

| Acceso | ¿Disponible? | Notas |
|--------|--------------|-------|
| **SSH** | **Sí** | Usuario `ubuntu`; clave en `~/.ssh/authorized_keys` |
| **Root / sudo** | **Sí** | `ubuntu` con sudo (grupo admin) |
| **Git** | **Sí** | Deploy por pull en repos bajo `/home/ubuntu/`; claves dedicadas (`id_ed25519_github`, `id_ed25519_biconsulting`, `id_ed25519_mustang`, etc.) |
| **Cloudflare** | **Sí** *(esperado)* | Cuenta EasyTech para zona `etsrv.site`; confirmar acceso para dominios externos |
| **Proveedor OCI** | **Sí** | Consola Oracle Cloud; Security Lists, snapshots, monitoring agent |
| **Cursor / IDE remoto** | **Sí** | `.cursor-server` presente en home |

---

## Tarea 13 – Backups

### Backup en Git (sitios en producción)

| Sitio | Repositorio | Estado Git (jun 2026) |
|-------|-------------|------------------------|
| **Detailing Service VE** | `git@github.com:shidalgo0925/DetailingserviceVE.site.git` | **Sincronizado** — commit `622515d` en `main` |
| **Mustang Basketball Academy** | `git@github-mustang:shidalgo0925/Mustang-Bastketball-.git` | **Sincronizado** con `origin/main` |
| **BI Consulting** | `git@github-biconsulting:shidalgo0925/biconsultingpma.git` | **Desalineado** — cambios locales sin commit en prod (`app.py`, `index.html`, CSS/JS, etc.) |
| **AA Transporte** | *Pendiente aprobación* | **Sin Git** — solo disco en servidor |
| **Refrigeración SJ** | *Pendiente aprobación* | **Sin Git** — solo disco en servidor |

### Otros respaldos

| Campo | Valor |
|-------|-------|
| **Cron backup SQL / archivos** | **No** — `crontab` usuario y root vacíos |
| **Backup sistema** | **dpkg/alternatives** en `/var/backups/` + `dpkg-db-backup.timer` |
| **Remota (Object Storage / S3)** | **No observada** |
| **OCI snapshots** | *Por confirmar* en consola OCI |
| **PostgreSQL** (`infomobile`, `onepercent_db`) | **Sin dump automático** |
| **Ollama** (`mistral:latest`) | **Sin backup** — re-descarga desde registry |
| **Responsable** | **EasyTech** |
| **Certbot** | Renovación TLS automática; no sustituye backup de contenido |

**Riesgo:** AA Transporte y Refrigeración SJ dependen solo del disco del VPS; BI Consulting puede perder cambios no commiteados; BDs legadas y modelo Ollama sin restore probado.

---

## Backup Hub

Preparación del host OCI como **receptor de backups** desde otros servidores EasyTech (TAMAL, CODITO, Spaguetti). Infraestructura base + **llaves SSH dedicadas** (jun 2026). **Sin rsync ni cron en origen aún.**

| Campo | Valor |
|-------|-------|
| **Estado** | **Listo para recibir backups** — infraestructura y llaves públicas en OCI; privadas pendientes en origen |
| **Usuario** | `backupsrv` **creado** *(sin sudo)* |
| **Estado SSH** | **Activo** — puerto **22/tcp** (`ssh.service` enabled) |
| **Espacio disponible** | **~30 GB** libres en `/` *(disco total 45 GB; uso prod ~16 GB)* |

### Directorios

| Ruta | Origen previsto |
|------|-----------------|
| `/backups/tamal` | TAMAL |
| `/backups/codito` | CODITO (Contabo) |
| `/backups/spaguetti` | Spaguetti |
| `/backups/manual` | Copias manuales / ad-hoc |
| `/backups/logs` | Registro de transferencias *(futuro)* |

### Permisos y acceso SSH

| Elemento | Valor |
|----------|-------|
| **Propietario** | `backupsrv:backupsrv` en `/backups` |
| **Modo** | `750` en árbol `/backups` |
| **`~backupsrv/.ssh/authorized_keys`** | **3 claves** ed25519 (una por origen), con `restrict` |
| **Validación escritura** | `sudo -u backupsrv touch /backups/test.txt` — OK |
| **Validación SSH** | `ssh -i …/id_ed25519_tamal backupsrv@127.0.0.1` — OK |

### Llaves SSH (jun 2026)

Par dedicado **por servidor origen**. La **pública** está en `backupsrv`; la **privada** queda en OCI para copiar al origen *(no en wiki)*.

| Origen | Comentario clave | Fingerprint (SHA256) | Destino rsync |
|--------|------------------|----------------------|---------------|
| **TAMAL** | `backup-tamal@instance-20251115-1442` | `dvIetad3hzt3V9PfSxLblfvF53xz7Hd11klUogjIVy4` | `/backups/tamal/` |
| **CODITO** | `backup-codito@instance-20251115-1442` | `J5oVpgUtMElbFpyOLkp2GvKBcGA7VQFBxOH3X0u5mA4` | `/backups/codito/` |
| **Spaguetti** | `backup-spaguetti@instance-20251115-1442` | `9iHnuhMwJXOiGqFbUvE+k60XhjbLTDkDeQETU+2escU` | `/backups/spaguetti/` |

| Ruta en OCI (solo servidor) | Contenido |
|-----------------------------|-----------|
| `/home/ubuntu/.ssh/backup-hub/id_ed25519_<origen>` | Clave **privada** — copiar al servidor origen |
| `/home/ubuntu/.ssh/backup-hub/id_ed25519_<origen>.pub` | Clave pública *(ya instalada en `authorized_keys`)* |

**Restricciones por clave:** `restrict`, sin port-forwarding, X11, agent-forwarding ni PTY.

**Despliegue en origen (pendiente):** en cada servidor (TAMAL / CODITO / Spaguetti), instalar la privada correspondiente (p. ej. `/root/.ssh/id_ed25519_backup_oci`, modo `600`) y probar:

```bash
ssh -i /root/.ssh/id_ed25519_backup_oci backupsrv@40.233.1.138
```

### UFW (sin cambios)

Reglas vigentes al preparar el hub — **no se modificaron**:

| # | Puerto | Acción | Origen |
|---|--------|--------|--------|
| 1 | 22/tcp | ALLOW | Anywhere |
| 2 | 80/tcp | ALLOW | Anywhere |
| 3 | 443/tcp | ALLOW | Anywhere |
| 4 | 8069/tcp | ALLOW | Anywhere |
| 5 | 11434/tcp | ALLOW | `95.111.244.137` |

**Pendiente:** copiar privadas a TAMAL/CODITO/Spaguetti, rsync sobre SSH, cron en origen, y política de retención.

---

## Riesgos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| **Sin backup off-site** de sitios y PostgreSQL | Pérdida total ante fallo de disco o terminación de instancia | Git para landings (3/5 con repo; 2 pendientes); backup BD + Object Storage OCI |
| **BI Consulting: prod ≠ Git** | Cambios locales sin commit no recuperables | Commit + push del estado actual de producción |
| **AA Transporte / Refrigeración SJ sin Git** | Pérdida total si cae el VPS | Crear repos tras aprobación; push inicial |
| **Secretos en systemd drop-in** (`biconsulting.service.d/override.conf`) | Fuga si se expone unidad o wiki | Mover a `EnvironmentFile` con permisos 600; rotar claves SMTP/reCAPTCHA |
| **Puertos HTTP expuestos** (8069, 8765, 8780, 11434) sin Nginx | Superficie de ataque; bypass de TLS | Cerrar en Security Lists / firewall; bind `127.0.0.1`; deshabilitar servicios legacy |
| **`detailing-landing.service` con ruta inválida** | Servicio zombie / confusión operativa | Corregir `WorkingDirectory` o deshabilitar unidad (Nginx ya sirve el sitio) |
| **Etiqueta «Producción IA» vs realidad** | Decisiones de arquitectura erróneas | Mantener stack IA en ficha CODITO; OCI = landings + Ollama auxiliar |
| **Sin swap** | OOM bajo picos (Ollama + Gunicorn) | Monitorear RAM; limitar Ollama; considerar swap o shape mayor |
| **ARM64 (A1.Flex)** | Binarios x86 incompatibles (p. ej. `wkhtmltox` amd64 en home sin uso) | Validar arquitectura antes de instalar paquetes |
| **Single point of failure** | Todas las landings OCI en una VM | Documentar RTO; plan de réplica o segundo nodo |
| **Cloudflare / DNS** | Caída DNS = sitios inaccesibles | Documentar cuenta; monitor externo |

---

## Próximos pasos

1. **Commit + push** estado prod de BI Consulting a `biconsultingpma.git`.
2. **Crear repos Git** para AA Transporte y Refrigeración SJ tras aprobación.
3. **Implementar backups** BD (`infomobile`, `onepercent_db`) y dumps hacia Object Storage OCI.
4. **Cerrar puertos** innecesarios (8069 mundo, 8765/8780) y revisar UFW Ollama (`11434`).
5. **Migrar secretos** de systemd override a `EnvironmentFile` con permisos 600.
6. **Deshabilitar** `detailing-landing.service` (zombie; Nginx ya sirve el sitio).
7. **Documentar TAMAL** (siguiente en cola) antes de Marketing Hub / Easy Operator.

---

## Cierre documental

| Campo | Valor |
|-------|-------|
| **Estado ficha** | **Documentado y Cerrado** |
| **Alcance** | Auditoría infraestructura Fase 2 — hechos observados, sin secretos |
| **Fecha cierre** | Junio 2026 |
| **Vacíos aceptados** | OCI snapshots en consola (*por confirmar*); repos Git AA Transporte / Refrigeración SJ (*pendiente aprobación*) |
| **Siguiente servidor** | **TAMAL** |

---

## Referencias en servidor (no wiki)

| Documento | Ruta |
|-----------|------|
| Estructura workspace | `/home/ubuntu/ESTRUCTURA_WORKSPACE.md` |
| DNS Cloudflare `etsrv.site` | `/home/ubuntu/docs/documentacion/SOLUCION_DNS_CLOUDFLARE.md` |
| Migración E5 → A1.Flex | `/home/ubuntu/docs/documentacion/INFO_APAGAR_E5.md` |
| Security Lists OCI | `/home/ubuntu/docs/documentacion/INSTRUCCIONES_SECURITY_LISTS.md` |

---

## Checklist de secciones (inspección)

| Sección | Estado |
|---------|--------|
| Resumen ejecutivo | ✅ |
| Propósito (Tarea 10) | ✅ |
| Evaluación estratégica | ✅ |
| Notas de arquitectura (CODITO) | ✅ |
| Infraestructura | ✅ |
| Dominios | ✅ |
| Aplicaciones | ✅ |
| Servicios | ✅ |
| Dependencias (Tarea 11) | ✅ |
| Backups (Tarea 13) | ✅ |
| Accesos (Tarea 12) | ✅ |
| Clasificación (Tarea 14) | ✅ |
| Riesgos | ✅ |
| Próximos pasos | ✅ |
| UFW / firewall host | ✅ |
| Backup Git por sitio | ✅ |
| Backup Hub (preparación) | ✅ |
| Dependencias cross-server | ✅ |
| Cierre documental | ✅ |

---

**Índice servidores:** [[06_Arquitectura/servidores/README]] · **CODITO (IA productiva / EN1):** [[06_Arquitectura/servidores/CODITO]] · **Siguiente:** TAMAL
