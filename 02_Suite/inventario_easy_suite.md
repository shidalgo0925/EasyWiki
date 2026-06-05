# Inventario Easy Suite en CODITO

Inventario **documental** de productos y plataformas Easy Suite desplegados o presentes en el VPS **CODITO** (`194.60.201.29`).  
**No es** repetición de la ficha de infraestructura — ver [[06_Arquitectura/servidores/CODITO]].

**Fecha:** 2026-06-05 · **Método:** inspección en disco + Git + Easy Wiki existente · **Sin cambios en servicios.**

---

## Resumen ejecutivo

| Producto / activo | ¿En CODITO? | Estado comercial principal |
|-------------------|-------------|----------------------------|
| [[03_Productos/en1_platform\|EN1 Platform]] | ✅ 4 silos | Prod + Staging + Dev + cliente Relatic |
| Relatic (cliente EN1) | ✅ | **Producción** |
| [[03_Productos/eclassone\|EClassOne]] | ✅ 3 silos | Prod + Staging + Dev |
| [[03_Productos/ethesisone\|EThesisOne]] | ✅ 1 instancia | **Laboratorio** |
| [[03_Productos/epayroll\|EPayRoll]] | ❌ | Marca suite; sin código en host |
| [[09_Marketing/marketing_hub\|Marketing Hub]] | ❌ *(solo wiki)* | Documentación comercial |
| Easy Wiki | ✅ repo local | **Laboratorio** (no servido por web) |
| [[03_Productos/eposone\|ePosOne]] | ❌ | Marca suite; sin despliegue observado |
| IA (Open WebUI + LiteLLM) | ✅ | **Laboratorio** |
| Landings (varios) | ✅ estáticos | Git; no apps EN1 |

---

## Mapa físico en CODITO

```text
/opt/easynodeone/          → EN1 (dev, staging, prod, relatic) + Easy Wiki + landings Relatic
/opt/easyclassone/         → EClassOne (dev, staging, prod)
/opt/easythesis/           → EThesisOne (dev)
/opt/ai-stack/             → LiteLLM + scripts IA
/var/www/                  → landings estáticos (easynodeone.com, eclassone.com, abril26.relatic.org)
```

---

## Fichas por producto

### 1. EN1 Platform (Easy NodeOne)

| Campo | Valor |
|-------|-------|
| **Ruta física** | `/opt/easynodeone/{dev,staging,prod,relatic}/app` |
| **Repositorio Git** | `git@github.com:shidalgo0925/Easy-NodeOne.git` |
| **Tecnología** | Python 3 · Flask · Gunicorn · PostgreSQL · systemd |
| **Documento wiki** | [[03_Productos/en1_platform]] · [[06_Arquitectura/arquitectura_en1]] · `05_Proyectos/en1/` |

#### Silos en CODITO

| Silo | Ruta | Rama Git | Último commit | systemd | Puerto | BD PostgreSQL | Dominio(s) | Estado comercial |
|------|------|----------|---------------|---------|--------|---------------|------------|------------------|
| **Dev** | `/opt/easynodeone/dev/app` | `develop` | `2b3d585` · 2026-06-04 | `easynodeone-dev` ✅ | 9101 | `easynodeone_dev` | `appdev.easynodeone.com`, `*dev.easynodeone.com` | **Laboratorio** |
| **Staging** | `/opt/easynodeone/staging/app` | `main` | `deaf1df` · 2026-06-04 | `easynodeone-staging` ✅ | 9104 | `easynodeone_staging` | `apptst.easynodeone.com` | **Staging** |
| **Prod** | `/opt/easynodeone/prod/app` | `main` | `deaf1df` · 2026-06-04 | `easynodeone-prod` ✅ | 9102 | `easynodeone_prod` | `appprd.easynodeone.com` | **Producción** |
| **Relatic** *(cliente)* | `/opt/easynodeone/relatic/app` | `develop` | `5d78e1c` · 2026-06-03 | `easynodeone-relatic` ✅ | 9103 | `easynodeone_relatic` | `apps.relatic.org`, `miembros.relatic.org` | **Producción** |

**Wiki — falta / actualizar:**

- ✅ `en1_platform.md` — completo a nivel producto.
- ⚠️ Añadir tabla «Presencia en CODITO» (propuesta aplicada en este inventario).
- ⚠️ `04_Clientes/relatic.md` — **no existe**; contrato Relatic solo en [[06_Arquitectura/servidores/CODITO]].

**Módulos EN1** activables por tenant: catálogo en [[03_Productos/en1_platform#Catálogo de módulos EN1 (referencia)]].

**Landings EN1:** build en `dev/app/landing/` → publicación en `/var/www/easynodeone` (`easynodeone.com`). Protegidos por Git.

---

### 2. Relatic (implementación cliente sobre EN1)

Relatic **no es un producto distinto de la suite** — es **EN1 Platform** configurado para **Relatic Panamá**.

| Campo | Valor |
|-------|-------|
| **Ruta física app** | `/opt/easynodeone/relatic/app` |
| **Repositorio Git** | `Easy-NodeOne` (mismo que EN1) |
| **Branch** | `develop` *(política operativa doc: verificar `main`/`relatic`)* |
| **Estado runtime** | ✅ Gunicorn activo |
| **Tecnología** | Idem EN1 |
| **Base de datos** | `easynodeone_relatic` |
| **Dominios** | `apps.relatic.org`, `miembros.relatic.org` |
| **Estado comercial** | **Producción** (cliente contractual) |

**Activos relacionados en CODITO:**

| Activo | Ruta | Repo | Dominio | Comercial |
|--------|------|------|---------|-----------|
| Landing marketing | `/opt/easynodeone/landings/relatic-public` → `/var/www/abril26.relatic.org` | `relatic-public` · `main` | `abril26.relatic.org` | Producción (marketing) |
| Front experimental RelaticV2 | `/opt/easynodeone/dev/relaticV2-github` | `Gill3010/relaticV2` · `main` | *(sin Nginx dedicado)* | **Laboratorio** |

**Documento wiki existente:** [[06_Arquitectura/servidores/CODITO]] · [[00_Gobierno/disaster_recovery_codito]]

**Falta:** `04_Clientes/relatic.md` · `05_Proyectos/relatic/` · mención en [[02_Suite/mapa_suite]] como cliente EN1.

---

### 3. EClassOne

| Campo | Valor |
|-------|-------|
| **Ruta física** | `/opt/easyclassone/{dev,staging,prod}/app` |
| **Repositorio Git** | **Sin `.git` local** en servidor |
| **Tecnología** | Python · Flask 2.3 · Gunicorn · PostgreSQL |
| **Documento wiki** | [[03_Productos/eclassone]] · `05_Proyectos/` *(sin ficha ECO dedicada)* |

| Silo | Rama Git | systemd | Puerto | BD | Dominio | Comercial |
|------|----------|---------|--------|-----|---------|-----------|
| Dev | — | `easyclassone-dev` ✅ | 9202 | `easyclassone_dev` | `appdev.eclassone.com` | **Laboratorio** |
| Staging | — | `easyclassone-staging` ✅ | 9203 | `easyclassone_staging` | `appstaging.eclassone.com` | **Staging** *(HTTP)* |
| Prod | — | `easyclassone-prod` ✅ | 9204 | `easyclassone_prod` | `app.eclassone.com`, `apps.eclassone.com` | **Producción** *(HTTP; SSL pendiente en conf Nginx)* |

**Landing:** `/var/www/eclassone` · `eclassone.com` · estático Vite.

**Wiki — falta / actualizar:**

- ⚠️ `eclassone.md` describe paquete comercial + EN1/IIUS; **no documenta despliegue real en CODITO**.
- ⚠️ Crear `05_Proyectos/eclassone/` o ampliar inventario en ficha producto.
- ⚠️ Identificar repo Git remoto (no clonado en host).

---

### 4. EThesisOne

| Campo | Valor |
|-------|-------|
| **Ruta física** | `/opt/easythesis/app` |
| **Repositorio Git** | `git@github.com-easythesis:shidalgo0925/Ethesis.git` |
| **Branch** | `main` |
| **Último commit** | `86ea0c5` · 2026-05-23 |
| **Estado runtime** | ✅ `easythesis-dev.service` |
| **Tecnología** | Python · Flask 2.3 · Gunicorn · PostgreSQL |
| **Base de datos** | `easythesis_dev` |
| **Dominios** | `ethesis.site`, `www.ethesis.site`, `ethesis.etsrv.site` |
| **Estado comercial** | **Laboratorio** / demo operativa |

**Handoff compartido:** `/opt/handoff-plataformas/BITACORA_CAMBIOS_PLATAFORMAS.md` (EN1 + EThesis).

**Wiki — falta / actualizar:**

- ⚠️ `ethesisone.md` indica «sin paquete estándar» — **desactualizado**: hay app desplegada en CODITO.
- ⚠️ Crear `05_Proyectos/ethesisone/` con rutas y dominios.
- ✅ Arquitectura cruzada parcial en [[06_Arquitectura/servidores/CODITO]] (servicios).

---

### 5. EPayRoll

| Campo | Valor |
|-------|-------|
| **Ruta física en CODITO** | **Ninguna** — búsqueda en `/opt` sin código ni servicio |
| **Repositorio Git** | **No desplegado** |
| **Estado comercial** | Marca de suite · **sin implementación en CODITO** |
| **Documento wiki** | [[03_Productos/epayroll]] · `05_Proyectos/epayroll/` *(placeholder)* |

**Roadmap:** Q4 2026 según [[10_Roadmap/roadmap_2026]].

**Falta:** todo contenido de implementación; mantener como producto **conceptual** hasta piloto.

---

### 6. Marketing Hub

| Campo | Valor |
|-------|-------|
| **Ruta física en CODITO** | **Ninguna** — no es aplicación desplegada |
| **Naturealeza** | Documentación y mensajes comerciales en Easy Wiki |
| **Documento wiki** | [[09_Marketing/marketing_hub]] · [[09_Marketing/productos_promocionables]] · [[09_Marketing/campanas]] |
| **Estado comercial** | **Documentación** (no entorno runtime) |

**Relación con CODITO:** los productos promocionados (EN1, EClassOne, etc.) **sí** tienen presencia en CODITO; el Hub en sí no.

**Falta:** tabla «qué está live en CODITO vs solo brochure» — cubierto por este inventario.

---

### 7. Easy Wiki

| Campo | Valor |
|-------|-------|
| **Ruta física** | `/opt/easynodeone/dev/EasyWiki` |
| **Repositorio Git** | `git@github.com:shidalgo0925/EasyWiki.git` |
| **Branch** | `main` |
| **Último commit** | `b9b10b4` · 2026-06-05 |
| **Estado runtime** | **No servido** por Nginx en CODITO |
| **Tecnología** | Markdown · Obsidian-style · Git |
| **Base de datos** | — |
| **Estado comercial** | **Laboratorio** / herramienta interna EasyTech |

**Documento wiki:** [[00_Inicio]] · [[00_Gobierno/gobierno_tecnologico]]

---

### 8. ePosOne

| Campo | Valor |
|-------|-------|
| **En CODITO** | ❌ No observado en `/opt` ni systemd |
| **Documento wiki** | [[03_Productos/eposone]] · `05_Proyectos/eposone/` |
| **Estado comercial** | Marca suite · roadmap Q3 2026 |

---

### 9. Servicios relacionados (no productos Suite)

| Servicio | Ruta | Tecnología | Dominio | Comercial |
|----------|------|------------|---------|-----------|
| **Open WebUI** | Docker vol. `open-webui` | Docker · SQLite interno | vía `ai.easynodeone.com` | Laboratorio IA |
| **LiteLLM** | `/opt/ai-stack/litellm/` | Docker | `ai.easynodeone.com`, `api-ai.easynodeone.com` | Laboratorio IA |
| **Ollama** | systemd | LLM local | — | Laboratorio IA |

Documentación IA: [[06_Arquitectura/arquitectura_ia]] *(breve)* · DR: [[00_Gobierno/disaster_recovery_codito]]

---

## Matriz documentación Easy Wiki

| Producto | Doc producto | Proyecto | Cliente | Infra | ¿Al día? |
|----------|--------------|----------|---------|-------|----------|
| EN1 Platform | [[03_Productos/en1_platform]] | `05_Proyectos/en1/` | varios | [[06_Arquitectura/servidores/CODITO]] | ⚠️ Falta presencia CODITO en ficha producto |
| Relatic | — | **falta** | **falta** `relatic.md` | [[06_Arquitectura/servidores/CODITO]] | ⚠️ |
| EClassOne | [[03_Productos/eclassone]] | **falta** | — | CODITO (servicios) | ⚠️ Despliegue no documentado |
| EThesisOne | [[03_Productos/ethesisone]] | **falta** | — | CODITO (servicios) | ⚠️ Desactualizado vs CODITO |
| EPayRoll | [[03_Productos/epayroll]] | placeholder | — | — | ✅ coherente (sin deploy) |
| ePosOne | [[03_Productos/eposone]] | stub | — | — | ✅ coherente (sin deploy) |
| Marketing Hub | [[09_Marketing/marketing_hub]] | — | — | — | ⚠️ Añadir nota «no es app» |
| Easy Wiki | [[00_Inicio]] | — | — | — | ✅ |
| Suite general | [[02_Suite/easy_suite]] · [[02_Suite/mapa_suite]] | — | — | — | ⚠️ Sin inventario CODITO hasta este doc |

---

## Propuestas de actualización (otros documentos)

| Archivo | Acción propuesta |
|---------|------------------|
| [[02_Suite/easy_suite]] | Enlace a este inventario; nota «presencia host compartido CODITO». |
| [[02_Suite/mapa_suite]] | Añadir fila Relatic; nota EThesis/EClassOne live en CODITO. |
| [[03_Productos/en1_platform]] | Sección «Presencia en CODITO» con tabla de silos. |
| [[03_Productos/eclassone]] | Sección despliegue CODITO + dominios. |
| [[03_Productos/ethesisone]] | Pasar de «visión» a «laboratorio desplegado en CODITO». |
| [[03_Productos/epayroll]] | Explicitar «sin despliegue en CODITO jun 2026». |
| [[09_Marketing/marketing_hub]] | Nota: hub = wiki; productos referenciados pueden estar en CODITO. |
| [[10_Roadmap/roadmap_2026]] | Referencia cruzada a inventario CODITO. |

---

## Referencias cruzadas

- Infraestructura host: [[06_Arquitectura/servidores/CODITO]]
- DR: [[00_Gobierno/disaster_recovery_codito]]
- Rutas técnicas servidor: `/opt/easynodeone/UBICACION-APPS.md`
- Roadmap: [[10_Roadmap/roadmap_2026]]

---

**Suite:** [[02_Suite/easy_suite]] · **Mapa:** [[02_Suite/mapa_suite]]
