# OCI — Servidor lógico (Producción IA / Landing Pages)

Documento maestro del host **Oracle Cloud Infrastructure (OCI)** de Easy Technology Services.  
Actualizado tras inspección en servidor · junio 2026.

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

## Notas de arquitectura (relación con CODITO)

| Elemento | ¿En OCI? | ¿En CODITO (Contabo)? |
|----------|----------|------------------------|
| `ai.easynodeone.com` | **No** | **Sí** (mismo VPS `vmi3225509`) |
| `api-ai.easynodeone.com` | **No** | *Por confirmar en inspección CODITO* |
| Open WebUI / LiteLLM | **No** | **Sí** *(stack `/opt/ai-stack` en Contabo — no duplicar ficha CODITO)* |
| EN1 / Relatic | **No** | **Sí** |
| Ollama `mistral:latest` | **Sí** (`0.0.0.0:11434`) | *No observado en esta ficha* |

**CODITO permanece cerrado** (ficha completa). Esta ficha solo enlaza lo que CODITO delegó a OCI y aclara que el metal es **distinto**.

---

## Infraestructura

| Recurso | Valor observado |
|---------|-----------------|
| **CPU** | 4 vCPU (`aarch64`) |
| **RAM** | 23 GiB (~22 GiB disponibles en inspección) |
| **Disco** | 45 GB (`/dev/sda1`), ~34 % uso |
| **Swap** | 0 B (sin swap configurado) |
| **Sistema operativo** | Ubuntu 22.04.5 LTS (Jammy), kernel `6.8.0-1047-oracle` |
| **Arquitectura** | **ARM64** (A1.Flex) |
| **Shape OCI** | A1.Flex *(inferido por docs internos de migración E5 → A1.Flex)* |
| **Agente cloud** | `oracle-cloud-agent` (snap), `unified-monitoring-agent` en `/opt` |

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
| **Detailing Service VE** | Landing + reservas (estático) | HTML/CSS/JS | **Producción** | EasyTech / cliente | `/home/ubuntu/DetailingServicesVE` |
| **AA Transporte** | Landing transporte | HTML estático | **Producción** | EasyTech / cliente | `/home/ubuntu/aa-transporte-landing` |
| **Refrigeración SJ** | Landing + API leads | HTML + Flask API | **Producción** | EasyTech / cliente | `/home/ubuntu/RefrigeracionSJ` (+ `api/`) |
| **Ollama** | Inferencia LLM local | Ollama + `mistral:latest` (~4.4 GB) | **Activo** (sin UI web documentada) | EasyTech | systemd `ollama.service` |
| **relatic_integration_dev** | Módulo Odoo (integración) en desarrollo | Python/Odoo | **No producción** | EasyTech | `/home/ubuntu/proyectos/relatic_integration_dev` |
| **invoice_import_massive_git** | Utilidad importación facturas | Python | **No producción** *(sin systemd)* | EasyTech | `/home/ubuntu/proyectos/invoice_import_massive_git` |
| **ets_report_studio / ets_weasy_sale_quote** | Módulos Odoo EasyTech | Python | **No producción** | EasyTech | `/home/ubuntu/ets_*` |
| **hka_test** | Pruebas facturación HKA | Python | **Laboratorio** | EasyTech | `/home/ubuntu/proyectos/hka_test` |

**Redirect raíz:** `/home/ubuntu/index.html` redirige a `DetailingServicesVE/`.

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
| Preview HTTP | `python3 -m http.server` | Puertos **8765**, **8780** (`0.0.0.0`) y **8070** (`127.0.0.1`) — servidores manuales sin Nginx; **riesgo de exposición** |

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
| **CODITO / Contabo** | **Referencia** | Stack IA productivo y EN1 — **dependencia organizacional**, no de red desde landings |
| **Let's Encrypt / Certbot** | **Sí** | TLS en todos los vhosts públicos |
| **OCI Security Lists** | **Sí** | Puertos 22, 80, 443 documentados en `docs/documentacion/INSTRUCCIONES_SECURITY_LISTS.md` |

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

| Campo | Valor |
|-------|-------|
| **Existe backup aplicación** | **No documentado** |
| **Cron backup SQL / archivos** | **No** — `crontab` usuario y root vacíos; sin scripts tipo `backup-*.sh` en rutas de apps |
| **Backup sistema** | Solo **dpkg/alternatives** en `/var/backups/` (estándar Ubuntu, no restauración de sitios) |
| **Remota** | **No observada** |
| **OCI snapshots** | *Por confirmar* en consola OCI (no inspeccionado desde shell) |
| **Responsable** | **EasyTech** — política de backup **pendiente de definir** |
| **Certbot** | Renovación automática TLS; no sustituye backup de contenido |

**Riesgo:** pérdida del VPS implica pérdida de sitios, BDs locales y modelo Ollama sin restore probado.

---

## Riesgos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| **Sin backup off-site** de sitios y PostgreSQL | Pérdida total ante fallo de disco o terminación de instancia | Implementar backup diario a Object Storage OCI o S3; probar restore |
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

1. **Alinear nomenclatura** en README wiki: OCI = Producción landings + Ollama auxiliar; IA productiva = CODITO.
2. **Implementar backups** (contenido `/home/ubuntu/*` landings + dump PostgreSQL) hacia almacenamiento remoto OCI.
3. **Cerrar puertos** innecesarios (8069, 8765, 8780, 11434 público) o restringir a VCN / túnel.
4. **Migrar secretos** de systemd override a archivos `EnvironmentFile` fuera de wiki/git.
5. **Revisar** unidad `detailing-landing.service` (ruta inexistente).
6. **Documentar TAMAL** (siguiente en cola según CODITO) antes de Marketing Hub / Easy Operator.
7. **No copiar** `backend/docs` de EN1 ni duplicar contenido de CODITO.

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

---

**Índice servidores:** [[06_Arquitectura/servidores/README]] · **CODITO (IA productiva / EN1):** [[06_Arquitectura/servidores/CODITO]]
