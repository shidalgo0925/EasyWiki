# EN1 Navigation & Commerce Hub

**Iniciativa:** Estratégica — Backlog aprobado  
**Estado:** BACKLOG APROBADO  
**Prioridad:** MEDIA  
**Dependencias:** Finalización Modecosa, finalización IIUS, estabilización EN1  
**Documento maestro:** [[10_Roadmap/roadmap_2026]]  
**Producto:** [[03_Productos/en1_platform|EN1 Platform]]  
**Cliente de referencia:** [[04_Clientes/iius|IIUS]]

---

## Contexto Ejecutivo

> **Restricción crítica:** No se autoriza iniciar desarrollo de esta mejora hasta finalizar:
> 1. Cierre Modecosa
> 2. Cierre IIUS
> 3. Estabilización EN1

IIUS se encuentra aproximadamente al **92% de avance**. Las prioridades inmediatas son operativas, no estratégicas. Este documento prepara el terreno para que, una vez liberados los recursos, el desarrollo del Commerce Hub sea inmediato y con alcance claro.

---

## Objetivo

Convertir la navegación superior de EN1 en un **hub comercial unificado** que permita operar la plataforma como marketplace de:

- Programas académicos
- Servicios profesionales
- Eventos
- Membresías
- Certificaciones
- Productos digitales

**Frase de diseño:** *Una sola navegación, múltiples productos, misma experiencia.*

---

## Navegación Futura

```
Inicio
│
├─ Tienda
│  ├─ Programas
│  ├─ Servicios
│  ├─ Eventos
│  ├─ Membresías
│  ├─ Certificaciones
│  └─ Productos Digitales
│
├─ Dashboard
│
├─ Mi Campus          (academic_closed — si aplica)
│
├─ Mi Perfil
│
└─ Soporte
```

---

## Fases de Implementación

### Fase 1 — Núcleo Comercial

**Alcance:**

Implementar `Tienda` con:

```
Tienda
├─ Programas
└─ Servicios
```

**Tareas técnicas:**

| # | Tarea | Complejidad | Owner |
|---|-------|-------------|-------|
| 1 | Crear módulo `commerce_hub` en EN1 | Media | Backend |
| 2 | Rediseñar navbar superior con dropdown `Tienda` | Baja | Frontend |
| 3 | Implementar catálogo de programas (reusa academic) | Baja | Backend |
| 4 | Implementar catálogo de servicios (nuevo tipo de producto) | Media | Backend |
| 5 | Checkout unificado para programas + servicios | Media | Backend |
| 6 | Páginas de detalle reutilizables (programa / servicio) | Baja | Frontend |
| 7 | Tests de integración en DEV | Baja | QA |

**Compatibilidad requerida:**

- [ ] Mantener compatibilidad con **Academic Gate** (política `academic_closed` de IIUS).
- [ ] Mantener compatibilidad con **permisos RBAC actuales**.
- [ ] Mantener compatibilidad **multi-tenant**.
- [ ] No modificar **rutas existentes** (`/mi-campus`, `/programa/:slug`, `/checkout`).

**Ambientes:**

- [ ] DEV (`appdev.easynodeone.com`)
- [ ] CODITO staging (`apptst.easynodeone.com`)
- [ ] Producción (`appprd.easynodeone.com` + tenant cliente)

---

### Fase 2 — Expansión de Catálogo

**Alcance:**

Incorporar al hub:

```
Tienda
├─ Programas
├─ Servicios
├─ Eventos
├─ Membresías
├─ Certificaciones
└─ Productos Digitales
```

**Tareas técnicas:**

| # | Tarea | Complejidad | Owner |
|---|-------|-------------|-------|
| 1 | Extender `commerce_hub` para eventos (reusa events) | Baja | Backend |
| 2 | Extender para membresías (reusa memberships) | Baja | Backend |
| 3 | Extender para certificaciones (reusa certificates) | Baja | Backend |
| 4 | Crear tipo `producto_digital` (descargas, ebooks, plantillas) | Media | Backend |
| 5 | Filtros unificados en Tienda (categoría, precio, modalidad) | Media | Frontend |
| 6 | Búsqueda global de productos/servicios/programas | Media | Backend |
| 7 | Carrito de compras compartido (si aplica) | Alta | Backend |
| 8 | Tests E2E de flujo completo | Media | QA |

---

## Alcance Técnico Detallado

### Qué se modifica

| Componente | Cambio |
|------------|--------|
| **Navbar superior** | Nuevo dropdown `Tienda` con subcategorías. |
| **Router frontend** | Nuevas rutas: `/tienda`, `/tienda/programas`, `/tienda/servicios`, etc. |
| **API backend** | Nuevo endpoint `/api/v1/commerce/catalog` con filtros. |
| **Base de datos** | Tabla `commerce_products` (polimórfica) o extensión de tablas existentes. |
| **Checkout** | Reutilizar checkout actual; agregar `product_type` en transacción. |
| **Admin panel** | Nueva sección "Catálogo comercial" para gestionar productos/servicios. |

### Qué NO se modifica

| Componente | Razón |
|------------|-------|
| Rutas existentes (`/mi-campus`, `/checkout`, `/programa/:slug`) | Evitar rotura en clientes activos (IIUS, Modecosa). |
| Lógica de matrícula académica | Academic Gate permanece independiente. |
| Permisología RBAC base | Se extiende, no se reemplaza. |
| Estructura multi-tenant | El hub respeta `organization_id`. |

---

## Ambientes y Despliegue

| Ambiente | URL | Uso |
|----------|-----|-----|
| DEV | `appdev.easynodeone.com` | Desarrollo activo |
| Staging (CODITO) | `apptst.easynodeone.com` | Pruebas antes de producción |
| Producción | `appprd.easynodeone.com` | Clientes en vivo |

**Regla de deploy:**  
Feature branch → DEV → PR → Staging → Validación QA → Producción con migraciones.  
Detalle: [[07_Operaciones/deploy]]

---

## Justificación de Negocio

| Problema actual | Solución con Commerce Hub |
|-----------------|---------------------------|
| EN1 se percibe solo como plataforma académica (IIUS). | Marketplace multi-producto: programas, servicios, eventos, membresías. |
| Cada producto tiene su propia landing aislada. | Catálogo unificado con navegación consistente. |
| Checkout repetido por producto. | Checkout unificado con carrito compartido (Fase 2). |
| Difícil cross-sell (vender servicio a alumno de programa). | Recomendaciones en Tienda basadas en historial. |
| Marketing disperso por producto. | Campañas centralizadas desde Marketing Hub. |

**Métricas de éxito (post-implementación):**

- Reducción de 30% en tiempo de configuración de nuevo producto.
- Aumento de 20% en cross-sell (medido por transacciones multi-producto).
- Unificación de 100% de checkouts en un solo flujo.

---

## Instrucción para el Programador

### Cuándo empezar

> **NO iniciar hasta que:**
> - Modecosa esté en estado **CERRADO**.
> - IIUS esté en estado **ENTREGADO**.
> - EN1 tenga tag de versión estable sin incidencias críticas por 2 semanas.

### Checklist previo al desarrollo

- [ ] Revisar este documento con Producto.
- [ ] Confirmar diseño de navbar con UI/UX (si aplica).
- [ ] Validar modelo de datos con Arquitectura.
- [ ] Crear feature branch: `feature/en1-commerce-hub-fase1`.
- [ ] Actualizar test suite con casos de Commerce Hub.

### Checklist durante el desarrollo

- [ ] Cada PR incluye tests unitarios.
- [ ] Cada PR pasa CI/CD en DEV.
- [ ] Documentar nuevos endpoints en swagger/Postman.
- [ ] Actualizar este wiki con decisiones técnicas tomadas.

### Checklist de cierre

- [ ] QA aprueba en staging.
- [ ] Documentación de usuario actualizada.
- [ ] Rollback plan definido.
- [ ] Deploy a prod con monitoreo activo.

---

## Fases Futuras Relacionadas

| Iniciativa | Estado | Documento |
|------------|--------|-----------|
| **EPayRoll** | Pendiente | *(por crear: `10_Roadmap/epayroll_roadmap.md`)* |
| **Marketing Hub** | Pendiente | *(por crear: `10_Roadmap/marketing_hub.md`)* |
| **EasyAgents** | Pendiente | *(por crear: `10_Roadmap/easyagents.md`)* |
| **Gobierno Tecnológico** | Pendiente | *(por crear: `10_Roadmap/gobierno_tecnologico.md`)* |

---

## Enlaces Wiki

- **Roadmap maestro:** [[10_Roadmap/roadmap_2026]]
- **Producto EN1:** [[03_Productos/en1_platform]]
- **Cliente IIUS:** [[04_Clientes/iius]]
- **Deploy y operaciones:** [[07_Operaciones/deploy]]
- **Arquitectura API:** [[06_Arquitectura/arquitectura_api]]
- **Marketing:** [[09_Marketing/marketing_hub]]

---

*Documento preparado: junio 2026*  
*Próxima revisión: post-cierre IIUS y Modecosa*  
*Elaborado por: Easy Technology Services — Dirección Tecnológica*