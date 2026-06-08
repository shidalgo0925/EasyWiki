# Landing EN1 — EasyNodeOne (Público)

Sitio de landing estático de **EN1 Platform** construido con **React + Vite + Tailwind CSS**. Sirve como puerta de entrada pública para prospectos, demos y conversión de leads.

## Ubicación en servidor

| Ruta | Descripción |
|------|-------------|
| `/opt/easynodeone/app/landing/` | Código fuente del landing |
| `/opt/easynodeone/app/landing/src/` | Componentes React |
| `/opt/easynodeone/app/landing/public/` | Assets estáticos (imágenes, logos, robots.txt, sitemap) |
| `/opt/easynodeone/app/landing/relatic-public/` | Build alternativo para Relatic (package.json separado) |

## Tecnología

| Capa | Tecnología |
|------|------------|
| Framework | React 19 (Vite) |
| Estilos | Tailwind CSS v4 |
| Fuente | Inter (Google Fonts) |
| Build tool | Vite |
| Linter | ESLint |

## Estructura de páginas

El landing es una **SPA (Single Page Application)** con routing basado en `window.location.pathname`. No usa React Router; el componente `App.jsx` renderiza secciones según la ruta.

| Ruta | Página | Componentes renderizados |
|------|--------|--------------------------|
| `/` (home) | Inicio | Hero + ProductStrip + Ecosystem + UseCases + MultiTenant + Automation + Events + Academic + UserPortal + Admin + ApiDev + Security + Plans + DemoForm |
| `/features` | Funciones | Hero + FeatureBlocks + Ecosystem + ApiDev + DemoForm |
| `/pricing` | Precios | Hero + Plans + DemoForm |
| `/contact` | Contacto | Hero + DemoForm |
| `/use-cases` | Casos de uso | Hero + UseCases + DemoForm |
| `/integrations` | Integraciones | Hero + ApiDev + DemoForm |

## SEO por página

Cada ruta tiene metadatos dinámicos inyectados vía `useEffect`:

- `title`
- `meta name="description"`
- Open Graph (`og:title`, `og:description`, `og:url`, `og:image`)
- Twitter Cards (`twitter:title`, `twitter:description`, `twitter:image`)
- Canonical URL

Valores fijos:
- **Dominio:** `https://easynodeone.com`
- **OG Image:** `/logos/logo-nodeone.png`

## Componentes principales

### Header
Navegación fija superior con logo y enlaces a secciones ancla (`#inicio`, `#ecosistema`, `#casos`, `#contacto`).

### Hero (`Hero.jsx`)
Delegador que renderiza:
- `HeroPlatform` → página home
- `HeroCompact` → resto de páginas (títulos definidos en `heroCompactTitles.js`)

### HeroPlatform
Sección principal de la home con:
- Headline: *"Centraliza miembros, eventos, pagos, certificados y operaciones en una sola plataforma modular"*
- Subtítulo sobre ecosistema multi-tenant para instituciones, asociaciones y empresas
- CTA: *Solicitar demo*, *Ver módulos*, *Explorar plataforma*, *Ir al login* (condicional a `VITE_APP_URL`)
- Badges: Multi-tenant · Seguro · Escalable · API first
- Mock visual del dashboard EN1 (KPIs, actividad reciente, ingresos por mes)

### PlatformProductStrip
Barra visual bajo el hero con figuras de producto.

### EcosystemEN1 (`#ecosistema`)
Grid de 8 módulos con iconos estructurales:

| Módulo | Descripción |
|--------|-------------|
| Membresías | Planes, renovaciones y estados de socio |
| Eventos | Inscripciones, cupos y check-in |
| Pagos | Pasarelas, conciliación y aprobaciones |
| Certificados | Emisión, QR y verificación |
| **Académico** | Programas, cohortes e inscripciones |
| CRM | Pipeline y seguimiento comercial |
| Servicios | Catálogo y reservas |
| Marketing | Campañas y automatizaciones |

Incluye figura de producto: `ecosistema-en1.png`.

### UseCasesEN1 (`#casos`)
Tabla y tarjetas de casos de uso por sector:

| Sector | Uso típico |
|--------|------------|
| **Institutos** | Diplomados, cohortes y certificación |
| Asociaciones | Membresías, renovaciones y beneficios |
| Empresas | Entrenamientos y desarrollo interno |
| Eventos | Registros, pagos y check-in |
| Educación | Programas académicos y trazabilidad |

> **Nota:** "Institutos" es el caso de uso que cubre a clientes como IIUS.

Incluye figura: `soluciones-organizaciones.png`.

### MultiTenantShowcase
Demo visual de múltiples organizaciones (tenants) activas en la plataforma, con datos de ejemplo como:
- Asociación de Ingenieros (1.850 miembros)
- Instituto Tecnológico (1.200 miembros)
- Empresa Constructora (340 miembros)

### AutomationShowcase
Flujos automáticos de comunicación (bienvenida, recordatorio, certificado, reconocimiento).

### EventsShowcase
Gestión de eventos: registro, pagos, check-in, certificados.

### AcademicShowcase (`#academico`)
Sección dedicada a la oferta formativa:
- Headline: *"Académico: programas y cohortes"*
- Mock visual de cohortes con estados (En curso / Inscripciones / Borrador)
- Ejemplo: Programa Data & IA — Cohorte A (32/40), B (18/40), C (0/35)

> **Relevancia IIUS:** Este es el módulo que IIUS utiliza para sus programas, diplomados y campus cerrado.

### UserPortalShowcase (`#portal`)
Vista del portal del usuario final (miembros, eventos, pagos, certificados).

### AdminShowcase
Panel administrativo con gestión de miembros, eventos, pagos y reportes.

### ApiDevShowcase
Sección de API y desarrolladores:
- Endpoints REST documentados
- Webhooks
- SDK y herramientas de integración

### SecurityTrustBand
Banda de confianza: encriptación, cumplimiento, backups, auditoría.

### Plans (`#precios`)
Tabla de planes con precios (material de diseño de producto, no datos reales de checkout).

### DemoForm (`#contacto`)
Formulario de contacto para solicitar demo.

### Footer
Enlaces legales, contacto, redes sociales.

### WhatsAppFloat
Botón flotante de WhatsApp.

## Assets y figuras de producto

| Archivo | Ubicación | Uso |
|---------|-----------|-----|
| `logo-nodeone.png` | `/public/logos/` | Logo principal, favicon, OG image |
| `logo-nodeone-dark.png` | `/public/logos/` | Variante oscura |
| `logo-nodeone-alt.png` | `/public/logos/` | Variante alternativa |
| `ecosistema-en1.png` | `/public/images/product/` | EcosystemEN1 |
| `soluciones-organizaciones.png` | `/public/images/product/` | UseCasesEN1 |
| `plataforma-modular.png` | `/public/images/product/` | Plataforma modular |
| `dashboard-admin.png` | `/public/images/product/` | Admin showcase |
| `gestion-eventos.png` | `/public/images/product/` | Events showcase |
| `automatizacion-workflows.png` | `/public/images/product/` | Automation |
| `robots.txt` | `/public/` | SEO robots |
| `sitemap.xml` | `/public/` | SEO sitemap |

## Configuración y despliegue

### Variables de entorno

| Variable | Ejemplo | Uso |
|----------|---------|-----|
| `VITE_APP_URL` | `https://app.easynodeone.com` | Enlace al login en el hero |

### Archivos de config

- `vite.config.js` — configuración de Vite
- `tailwind.config.js` — configuración de Tailwind
- `postcss.config.js` — PostCSS
- `eslint.config.js` — ESLint
- `index.html` — HTML base con metadatos estáticos

### Despliegue

Ver `DEPLOY_LANDING.txt` en la raíz del proyecto para instrucciones específicas de deploy.

## Relación con clientes

### IIUS
El landing presenta el módulo **Académico** como uno de los 8 pilares del ecosistema EN1. El caso de uso **"Institutos"** en `UseCasesEN1` describe exactamente la operación de IIUS: *"Diplomados, cohortes y certificación"*. El mock de `AcademicShowcase` muestra cohortes con inscripciones, estados y cupos — el mismo modelo que IIUS usa en producción.

### Relatic
Existe una carpeta `relatic-public/` con su propio `package.json`, sugiriendo un build alternativo o white-label para el cliente Relatic.

## Estado (junio 2026)

- Landing funcional y desplegado
- SEO dinámico implementado por ruta
- 6 rutas funcionales
- 15+ componentes visuales
- Mock de dashboard interactivo en el hero
- Sin backend propio; es 100% estático

---

**Producto:** [[03_Productos/en1_platform]] · **Cliente:** [[04_Clientes/iius]] · **Marketing:** [[09_Marketing/marketing_hub]]