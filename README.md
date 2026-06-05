# Easy Wiki — Easy Technology Services

Wiki operativa (Markdown + **Obsidian**). **FASE 2** — junio 2026: arquitectura de producto, inventario suite e infra CODITO.

## Cómo usar

1. Clonar: `git clone git@github.com:shidalgo0925/EasyWiki.git`
2. Abrir la **carpeta raíz del repo** en Obsidian (el vault es esa carpeta, no una subcarpeta).
3. Empezar por el índice: **[00_Inicio.md](00_Inicio.md)** (en Obsidian también puedes abrir `[[00_Inicio]]`).

### Si ves `[[algo]]` sin enlace

Esa sintaxis es **wikilink de Obsidian**. En la web de GitHub **no** se convierte en link; en Obsidian sí. En GitHub usa la tabla de abajo con rutas `.md`.

## Documentos clave (GitHub)

| Capa | Pregunta | Archivo |
|------|----------|---------|
| **Inicio** | ¿Por dónde empiezo? | [00_Inicio.md](00_Inicio.md) |
| **Arquitectura producto** | ¿Cómo se relacionan EN1, Relatic, EClassOne…? | [01_Arquitectura_Producto/easy_suite_architecture.md](01_Arquitectura_Producto/easy_suite_architecture.md) |
| **Suite** | ¿Qué es Easy Suite? | [02_Suite/easy_suite.md](02_Suite/easy_suite.md) |
| **Suite** | ¿Mapa de productos? | [02_Suite/mapa_suite.md](02_Suite/mapa_suite.md) |
| **Suite** | ¿Qué hay desplegado en CODITO? | [02_Suite/inventario_easy_suite.md](02_Suite/inventario_easy_suite.md) |
| **Productos** | ¿Qué es EN1? | [03_Productos/en1_platform.md](03_Productos/en1_platform.md) |
| **Infra** | ¿Servidor CODITO / Relatic? | [06_Arquitectura/servidores/CODITO.md](06_Arquitectura/servidores/CODITO.md) |
| **DR** | ¿Qué pasa si cae CODITO? | [00_Gobierno/disaster_recovery_codito.md](00_Gobierno/disaster_recovery_codito.md) |
| **Gobierno** | ¿Principios tecnológicos? | [00_Gobierno/gobierno_tecnologico.md](00_Gobierno/gobierno_tecnologico.md) |
| **Roadmap** | ¿Prioridades 2026? | [10_Roadmap/roadmap_2026.md](10_Roadmap/roadmap_2026.md) |

**MVP original + operación EN1:** [07_Operaciones/deploy.md](07_Operaciones/deploy.md), [06_Arquitectura/arquitectura_en1.md](06_Arquitectura/arquitectura_en1.md), [04_Clientes/iius.md](04_Clientes/iius.md), [09_Marketing/marketing_hub.md](09_Marketing/marketing_hub.md).

## Estructura de carpetas

```text
00_Gobierno
01_Arquitectura_Producto   ← relaciones funcionales Easy Suite
01_Empresa
02_Suite
03_Productos
04_Clientes → 05_Proyectos
06_Arquitectura            ← técnica + servidores
07_Operaciones → 08_IA → 09_Marketing → 10_Roadmap → 99_Recursos
```

## Repo

| | |
|--|--|
| **Git** | `git@github.com:shidalgo0925/EasyWiki.git` |
| **PC local (sugerida)** | `\EasyTech\EasyWiki\` |
| **Actualizar** | `git pull` dentro del clone |

---

*Easy Technology Services — documentación interna.*
