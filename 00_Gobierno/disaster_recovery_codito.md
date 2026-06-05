# Disaster Recovery — CODITO

Análisis de continuidad operativa del VPS **CODITO** (`vmi3225509`, `194.60.201.29`).  
Basado en auditoría en vivo · `2026-06-05` · **solo lectura, sin cambios en servicios**.

**Ficha técnica completa:** [[06_Arquitectura/servidores/CODITO]]

---

## 1. Escenario

> **Pregunta:** ¿Qué ocurre si mañana desaparece CODITO?

Desaparecer CODITO significa **pérdida total del VPS Contabo**: disco, backups locales, contenedores Docker, certificados TLS en origen, `.env` con secretos y todos los procesos systemd. DNS seguiría apuntando a una IP muerta hasta reconfigurar.

**Tiempo hasta detección:** minutos a horas (según monitorización; no hay evidencia de monitor externo documentado en esta auditoría).

---

## 2. Matriz de impacto (Fase 9)

Clasificación si el VPS no vuelve en < 24 h.

| Servicio / activo | Deja de funcionar | Impacto | Recuperable desde |
|-------------------|-------------------|---------|-------------------|
| `apps.relatic.org` / `miembros.relatic.org` (EN1 Relatic) | **Sí — inmediato** | **CRÍTICO** | Git + backup SQL `relatic_*.sql` + `.env` |
| Pagos PayPal / OAuth Relatic | **Sí** | **CRÍTICO** | `.env` (no en Git) + panel PayPal/Google |
| BD `easynodeone_relatic` | **Sí** | **CRÍTICO** | Backup diario local *(si se pierde VPS, se pierde backup)* |
| Landing `abril26.relatic.org` | **Sí** | GIT | Git `relatic-public` + rebuild |
| `appprd.easynodeone.com` (EN1 prod) | **Sí** | **CRÍTICO** | Git + backup `prod_*.sql` + uploads |
| `appdev` / `apptst` (EN1 dev/staging) | **Sí** | MEDIO | Git; BD dev/staging **sin backup** |
| `ai.easynodeone.com` / `api-ai.easynodeone.com` | **Sí** | ALTO | Docker images + config YAML; **datos WebUI no** |
| Open WebUI (chats, vectores, uploads) | **Sí** | ALTO | **No respaldado** (~1,1 GiB en volúmen) |
| LiteLLM + Ollama | **Sí** | BAJO | Rebuild contenedor + config `/opt/ai-stack/` |
| EasyThesis (`ethesis.site`) | **Sí** | MEDIO | Git + BD **sin backup automático** |
| Easy Class One | **Sí** | MEDIO | **Sin Git en servidor**; BD sin backup |
| Landings `easynodeone.com`, `eclassone.com` | **Sí** | GIT | Rebuild desde repos |
| Easy Wiki (Markdown) | **No en producción web** | BAJO | GitHub `EasyWiki` |
| RelaticV2 (experimental) | **Sí** (si se usara) | BAJO | GitHub |
| Correo / jobs EN1 | **Sí** | según uso | Config en `.env` |

### Resumen por criticidad *(alcance backup OCI)*

| Nivel | Qué cae | Backup OCI |
|-------|---------|------------|
| **CRÍTICO** | Relatic + EN1 prod (app, pagos, BD, uploads prod) | CODITO-1…3 |
| **ALTO** | Open WebUI (datos IA no en Git) | CODITO-4 |
| **BAJO** | Dev, staging, ECO, EasyThesis, LiteLLM | Rebuild Git |
| **GIT** | Landings | Excluidos DR |

---

## 3. Qué se perdería irrecuperablemente (hoy)

Sin copia **off-site** previa al desastre:

1. **Todos los backups SQL** en `/opt/easynodeone/backups/` (176 MiB, retención ~55 días prod/relatic).
2. **Open WebUI:** `webui.db`, `vector_db`, uploads y cache (~1,1 GiB).
3. **Archivos subidos EN1** no versionados en Git (~128 MiB prod, ~6 MiB relatic en `static/uploads` + `uploads/`).
4. **Secretos** de todos los silos (`.env`), claves LiteLLM (`MASTER_KEY.txt`), credenciales PayPal/OAuth/SMTP.
5. **Bases PostgreSQL sin backup:** dev, staging, easythesis, easyclassone, clone relatic.
6. **Certificados Let's Encrypt** en origen (reemitibles, pero requieren DNS operativo).
7. **Modelos Ollama** descargados (re-descargables con tiempo/ancho de banda).
8. **Easy Class One:** código en disco sin historial Git local.

**Ventana de pérdida de datos Relatic:** desde el último backup exitoso (cron 02:00) hasta el momento del desastre — **hasta ~24 h de transacciones** (pagos, altas, cambios de plan).

---

## 4. Continuidad operativa — plan recomendado (Fase 10)

### 4.1 Qué debe respaldarse (alcance aprobado)

| Prioridad | Activo | Fase |
|-----------|--------|------|
| P0 | BD `easynodeone_relatic` + `easynodeone_prod` | CODITO-1 |
| P0 | `.env` Relatic + `.env` prod (cifrado) | CODITO-2 |
| P1 | Uploads Relatic + EN1 prod | CODITO-3 |
| P1 | Open WebUI *(sin cache)* | CODITO-4 |

**Fuera de alcance:** dev, staging, Easy Class One, EasyThesis, LiteLLM, nginx, landings *(Git)*.

### 4.2 Qué debe enviarse a OCI

**Diseño detallado:** sección **9**.

| Componente | Destino OCI | Fase |
|------------|-------------|------|
| PostgreSQL Relatic + prod | `postgres/relatic/` · `postgres/prod/` | CODITO-1 |
| `.env` cifrados | `config/env/` | CODITO-2 |
| Uploads prod | `uploads/relatic/` · `uploads/en1-prod/` | CODITO-3 |
| Open WebUI | `docker/open-webui/` | CODITO-4 |

### 4.3 Qué puede reconstruirse desde Git *(no backup OCI)*

| Componente | Recuperación |
|------------|--------------|
| Código EN1 (dev/staging) | `git clone` Easy-NodeOne |
| Easy Class One · EasyThesis | Git + venv + systemd |
| LiteLLM | `/opt/ai-stack/litellm/` + `docker pull` |
| Landings | `relatic-public`, EN1 `landing/`, etc. |
| Easy Wiki | GitHub `EasyWiki` |

### 4.4 Qué no puede recuperarse actualmente *(hasta CODITO-1…4)*

| Activo | Motivo |
|--------|--------|
| Backups en disco del VPS | Mismo punto de fallo |
| BD prod Relatic + prod EN1 off-site | CODITO-1 pendiente |
| Uploads prod / Relatic | CODITO-3 pendiente |
| Chats Open WebUI | CODITO-4 pendiente |
| `.env` prod / Relatic | CODITO-2 pendiente |
| Transacciones post-backup 02:00 | Gap hasta ~24 h |

---

## 5. Estimación de tiempos de recuperación (RTO)

Escenario: **nuevo VPS provisionado** (Contabo u OCI), DNS actualizado, equipo con acceso a secretos off-site.

| Escenario | RTO estimado | RPO estimado (Relatic) |
|-----------|--------------|------------------------|
| **Solo Relatic** (mínimo contractual) | **8–16 h** | ~24 h (último backup local perdido → necesita off-site) |
| **Relatic + EN1 prod** | **16–24 h** | ~24 h |
| **CODITO completo** (todos los servicios actuales) | **24–48 h** | Variable; muchas BD sin backup |
| **Con backups off-site ya operativos** | **4–8 h** (Relatic) | < 24 h (último dump remoto) |

Factores que alargan: reemisión TLS, recrear 12+ sitios Nginx, descargar modelos Ollama, reconfigurar Cloudflare, prueba de pagos PayPal en sandbox antes de prod.

---

## 6. Servicios que quedarían fuera (lista operativa)

Hasta completar restore:

- Portal miembros y administración Relatic.
- Cobro PayPal y flujos de inscripción Relatic.
- App EN1 producción (`appprd.easynodeone.com`).
- Entorno dev/staging EN1 (`appdev`, `apptst`).
- Portal IA (`ai.easynodeone.com`) y API Continue (`api-ai.easynodeone.com`).
- EasyThesis (ambos dominios).
- Easy Class One (todos los entornos).
- Landings corporativas (`easynodeone.com`, `eclassone.com`, `abril26.relatic.org`).

**Easy Wiki:** no hay servicio web en CODITO; el equipo puede seguir trabajando desde GitHub.

---

## 7. Acciones inmediatas recomendadas

**Estado:** plan off-site **diseñado** (jun 2026) — ver sección 9. **Implementación aún no iniciada.**

Prioridad de ejecución cuando se apruebe implementación:

1. Prerrequisitos OCI (bucket 5 GiB, IAM, clave API CODITO).
2. **CODITO-1:** push dumps `relatic` + `prod`.
3. **CODITO-2 → CODITO-4** según sección 9.
4. Prueba restore trimestral (solo prod crítica).
5. Monitor HTTP `apps.relatic.org`.

*(Detalle técnico completo en sección 9.)*

---

## 9. Plan backup off-site OCI *(alcance aprobado · sin implementar)*

**Principio:** solo **valor de negocio** — dos BDs productivas, secretos prod, uploads prod, Open WebUI.  
**Medición:** `2026-06-05` en CODITO · **sin cron · sin copias**.

### 9.0 Clasificación oficial

| Nivel | Activos | Backup OCI |
|-------|---------|------------|
| **CRÍTICO** | `easynodeone_relatic`, `easynodeone_prod` | CODITO-1 |
| **CRÍTICO** | `.env` Relatic, `.env` prod | CODITO-2 |
| **ALTO** | Uploads Relatic + EN1 prod | CODITO-3 |
| **ALTO** | Open WebUI *(datos, no cache)* | CODITO-4 |
| **BAJO** | Dev, staging, ECO, EasyThesis, LiteLLM | **No** — Git rebuild |
| **GIT** | Landings | **Excluidos DR** |

### 9.1 Inventario medido

#### PostgreSQL (CODITO-1)

| BD | Tamaño cluster | Dump diario medido |
|----|----------------|-------------------|
| `easynodeone_relatic` | 21 MB | **4,05 MiB** |
| `easynodeone_prod` | 18 MB | **0,89 MiB** |

#### `.env` (CODITO-2)

| Archivo | Ruta | Tamaño |
|---------|------|--------|
| Relatic | `/opt/easynodeone/relatic/.env` | 1 259 B |
| EN1 Prod | `/opt/easynodeone/prod/.env` | 534 B |

#### Uploads (CODITO-3)

| Ámbito | Rutas | Tamaño |
|--------|-------|--------|
| Relatic | `relatic/app/static/uploads` + `relatic/app/uploads` | **5,76 MiB** |
| EN1 Prod | `prod/app/static/uploads` | **126,97 MiB** |
| **Total baseline** | | **132,73 MiB** |

#### Open WebUI (CODITO-4)

| Item | Valor |
|------|-------|
| Ruta | `/var/lib/docker/volumes/open-webui/_data` |
| Total volúmen | 1,04 GiB |
| **A respaldar** | `webui.db` + `vector_db` = **732 KiB** |
| **Excluir** | `cache/` = 1,04 GiB |

---

### 9.2 Estructura OCI

```text
backups/codito/
├── postgres/relatic|prod/YYYY/MM/DD/
├── config/env/relatic.env.age · prod.env.age
├── uploads/relatic/ · uploads/en1-prod/
├── docker/open-webui/YYYY-MM-DD/
└── logs/push-YYYY-MM-DD.log
```

---

### 9.3 Dimensionamiento total

| Concepto | Valor |
|----------|-------|
| **Día 1 (baseline completo)** | **~138 MiB** |
| **Día típico recurrente** | **~5,5–8,5 MiB** |
| **Ingesta mes 1** | **~320 MiB** |
| **Ingesta mensual recurrente** | **~165–255 MiB** |
| **Espacio OCI steady-state** | **~550–650 MiB** |
| **Bucket recomendado** | **5 GiB** |
| **Tiempo copia día 1** | 2–4 min |
| **Tiempo copia día típico** | < 1 min |
| **Coste orientativo** | **~USD 0,13/mes** |
| **RPO Relatic (post CODITO-1)** | < 24 h |
| **RTO Relatic (con OCI)** | 4–8 h |

---

### 9.4 Roadmap (4 fases)

| Fase | Contenido |
|------|-----------|
| **CODITO-1** | PG `easynodeone_relatic` + `easynodeone_prod` |
| **CODITO-2** | `.env` Relatic + prod cifrados |
| **CODITO-3** | Uploads Relatic + EN1 prod |
| **CODITO-4** | Open WebUI sin `cache/` |

**Excluido explícitamente:** dev, staging, Easy Class One, EasyThesis, LiteLLM, nginx, landings.

---

### 9.5 Impacto tras implementación completa

| Hoy | Tras CODITO-1…4 |
|-----|-----------------|
| Backups mueren con VPS | PG prod sobrevive en OCI |
| Uploads / WebUI perdidos | Restaurables desde bucket |
| Secretos solo en disco | `.env` cifrado off-site |
| RTO Relatic 8–16 h | **4–8 h** |

---

## 8. Conclusión obligatoria

### ¿Qué pasa si mañana se pierde CODITO?

**Todo lo que corre en `194.60.201.29` deja de existir.** Relatic Panamá queda **completamente offline** (app, pagos, miembros). EasyTech pierde además dev/staging/prod EN1, IA interna, EasyThesis y Easy Class One en el mismo golpe. Los backups actuales **mueren con el disco**.

**Plan de mitigación diseñado (no activo):** 4 fases **CODITO-1…4** hacia OCI — solo producción crítica. Hasta **CODITO-1**, el riesgo contractual Relatic es el mismo.

### ¿Cuántas horas tomaría recuperarlo?

| Situación | RTO Relatic |
|-----------|-------------|
| **Hoy** (solo backup local) | 8–16 h; datos en riesgo |
| **Tras CODITO-1** (PG off-site) | **4–8 h** |
| **Tras CODITO-1…4** | **4–8 h** Relatic/prod · laboratorios: rebuild Git |

### ¿Qué información se perdería?

**Hoy:** gap ~24 h Relatic; uploads prod; WebUI; `.env` prod.

**Tras CODITO-1…4:** solo gap 02:00→desastre; dev/staging/ECO/EThesis reconstruibles sin datos históricos.

### ¿Qué servicios quedarían fuera?

Relatic y EN1 prod hasta restore. Dev/staging/ECO/EThesis/LiteLLM: rebuild manual. Landings: redeploy Git.

### Plan respaldo CODITO → OCI (alcance aprobado)

| Fase | Contenido | Tamaño clave |
|------|-----------|--------------|
| CODITO-1 | PG Relatic + prod | **4,9 MiB/día** |
| CODITO-2 | `.env` cifrados | **~2 KiB/día** |
| CODITO-3 | Uploads | **132,7 MiB baseline** |
| CODITO-4 | Open WebUI sin cache | **732 KiB/día** |

**Total día 1:** ~**138 MiB** · **Día típico:** ~**6–8 MiB** · **Bucket:** **5 GiB** · **~USD 0,13/mes**  
**Estado:** dimensionado — **implementación pendiente**.

---

**Relacionado:** [[06_Arquitectura/servidores/CODITO]] · [[06_Arquitectura/servidores/README]] · [[07_Operaciones/deploy]]
