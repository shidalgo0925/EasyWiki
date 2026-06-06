# EasyTech Context — Documento Maestro de Onboarding

> **Propósito:** Permitir a cualquier IA, programador, consultor o nuevo integrante comprender Easy Technology Services en menos de 10 minutos.
>
> **Audiencia:** ChatGPT, Cursor, Kimi, Accio, Easy Operator, nuevos desarrolladores, consultores.
>
> **Tipo:** Resumen ejecutivo con enlaces a documentación detallada.
>
> **Actualizado:** junio 2026.

---

## 1. Resumen Ejecutivo

### ¿Qué es Easy Technology Services?

**Easy Technology Services** es una empresa panameña de desarrollo de software que diseña, implementa y da soporte a plataformas digitales para clientes que necesitan **operar, vender, cobrar, enseñar o facturar** en un solo ecosistema coherente.

### ¿Cuál es su misión?

Diseñar, construir y operar soluciones digitales que:
1. **Funcionen** en el día a día del cliente.
2. **Escalen** por módulos y por organización.
3. **Se documenten** para que el conocimiento no dependa de una sola persona.

### ¿Qué tipo de empresa es?

- **No** es una agencia de sitios web.
- **No** vende licencias ajenas sin acompañamiento.
- **Sí** es un socio tecnológico de implementación: entiende el negocio del cliente, activa módulos relevantes, valida en pruebas, documenta y soporta.

### ¿Qué problemas resuelve?

| Sector | Problema | Solución Easy Suite |
|--------|----------|---------------------|
| Educación | Inscripciones dispersas, campus sin control | EN1 + módulo `academic` + EClassOne |
| Comercio | Inventario desconectado, caja lenta | EN1 + ePosOne |
| Servicios | Citas desorganizadas, pagos manuales | EN1 + módulos `appointments`, `payments` |
| Operaciones | Taller sin trazabilidad, SLA invisible | EN1 + módulo `workshop` |
| Multi-sucursal | Sistemas aislados por marca | EN1 multi-tenant (una plataforma, varias organizaciones) |

La entrega se apoya en **EN1 Platform** como núcleo y en productos especializados de **Easy Suite**.

**Documentación completa:** [[01_Empresa/easytechnology]] · [[00_Gobierno/mision]] · [[00_Gobierno/vision]] · [[00_Gobierno/valores]]

---

## 2. Infraestructura Corporativa

EasyTech opera sobre una infraestructura híbrida de VPS (Contabo + Oracle Cloud). No hay IPs ni credenciales en este documento.

### OCI

| Campo | Valor |
|-------|-------|
| **Función** | Hosting de landing pages de clientes + Backup Hub + Ollama auxiliar |
| **Estado** | Producción (sitios estáticos y APIs de leads) |
| **Nota** | No aloja el stack principal de IA (Open WebUI/LiteLLM) — ese está en CODITO |

### TAMAL

| Campo | Valor |
|-------|-------|
| **Función** | Servidor ERP principal multi-tenant Odoo 18 Community |
| **Estado** | Producción activa (6 clientes ERP + operación interna) |
| **Nota** | Facturación electrónica Panamá (HKA), módulos propios EasyTech |

### CODITO

| Campo | Valor |
|-------|-------|
| **Función** | Producción EN1 (Relatic + EN1 prod) + Laboratorios (dev, staging, EClassOne, EThesisOne) + IA (Open WebUI, LiteLLM, Ollama) |
| **Estado** | Producción crítica + co-hosting de labs |
| **Nota** | Cliente contractual principal: Relatic Panamá |

### SPAGUETTI

| Campo | Valor |
|-------|-------|
| **Función** | *(No documentado en wiki — servidor pendiente de inventario o desmantelado)* |
| **Estado** | **Desconocido** |
| **Nota** | No existe ficha `SPAGUETTI.md` en el repositorio |

### MODECOSA

| Campo | Valor |
|-------|-------|
| **Función** | *(No es servidor propio de EasyTech — es el ERP del cliente)* |
| **Estado** | Cliente con Odoo 19 propio (`erp.modecosa.com`) |
| **Nota** | Integra con EN1 vía conector `en1_connector` (catálogo de seguridad) |

**Detalle técnico:** [[06_Arquitectura/servidores/OCI]] · [[06_Arquitectura/servidores/TAMAL]] · [[06_Arquitectura/servidores/CODITO]]

---

## 3. Easy Suite

Easy Suite es la familia comercial de productos EasyTech. Un cliente puede empezar con un módulo y crecer hacia un ERP completo sin cambiar de proveedor.

### EN1 Platform (Easy NodeOne)

- **Qué es:** Motor SaaS principal. Backend Flask + panel admin + portal miembros + checkout + módulos activables por organización.
- **Para quién:** Negocios e instituciones que necesitan operación web integral.
- **Unidad de datos:** Organización (tenant) — logo, usuarios, módulos, pagos propios.
- **Unidad de despliegue:** Silo — copia del repo + `.env` + BD PostgreSQL + dominio.
- **Estado:** Producción activa (evolución continua).

**Relatic, IIUS y Modecosa-type son Apps EN1** — implementaciones del mismo motor con configuración propia.

### Relatic

- **Qué es:** App EN1 para Relatic Panamá (membresías, pagos PayPal, portal miembros).
- **Dominios:** `apps.relatic.org`, `miembros.relatic.org`
- **Estado:** Producción activa (cliente contractual de CODITO).

### EClassOne

- **Qué es:** Producto de aula digital y experiencia de campus. Puede convivir con EN1 (IIUS) o desplegarse solo.
- **Estado:** Prod + Staging + Dev en CODITO.
- **Nota:** Sin repositorio Git local confirmado en servidor.

### EThesisOne

- **Qué es:** Flujos académicos de investigación y tesis (protocolos, revisiones, trazabilidad).
- **Estado:** Laboratorio / demo operativa en CODITO.
- **Repo:** `Ethesis`

### ePosOne

- **Qué es:** Punto de venta (POS) para retail y mostrador.
- **Estado:** **Sin despliegue** — roadmap Q3 2026 (ficha comercial + pilotos).
- **Relación EN1:** Opcional (inventario, contactos).

### EPayRoll

- **Qué es:** Nómina y gestión de personal (cálculo de salarios, deducciones, reportes legales).
- **Estado:** **Sin despliegue** — visión Q4 2026 según demanda.
- **Relación EN1:** Opcional (empleados como contactos).

### Marketing Hub

- **Qué es:** Centro de mensajes comerciales — elevator pitches, audiencias, campañas.
- **Estado:** Documentación viva en Easy Wiki (no es aplicación desplegada).

### Easy Wiki

- **Qué es:** Base de conocimiento corporativa operativa (Obsidian-style + Git).
- **Estado:** MVP en curso (Fase 2 auditoría completada). No servida por web en jun 2026.
- **Roadmap:** Publicación estática Q4 2026.

**Documentación completa:** [[02_Suite/easy_suite]] · [[02_Suite/mapa_suite]] · [[01_Arquitectura_Producto/easy_suite_architecture]]

---

## 4. Clientes Estratégicos

### Modecosa

- **Producto:** Odoo 19 propio + integración EN1 (catálogo de seguridad).
- **Estado:** Fase 1 entregada (lectura de catálogo Odoo en EN1). Fase 2 planificada (aplicar cambios con aprobación humana).
- **Módulo EN1:** `security_matrix`

### IIUS

- **Producto:** EN1 Platform + campus cerrado (`academic_closed`).
- **Estado:** Producción activa. Programas, inscripciones, pagos, campus cerrado, certificados.
- **Política clave:** Alumno accede a `/mi-campus` solo con matrícula `paid` o `confirmed`.

### Relatic

- **Producto:** App EN1 (silo `relatic`).
- **Estado:** Producción activa. Membresías, pagos PayPal, portal miembros.
- **Nota:** No existe ficha independiente `04_Clientes/relatic.md`; documentado dentro de CODITO.

### Otros clientes relevantes

| Cliente | Producto | Infraestructura | Nota |
|---------|----------|-----------------|------|
| La Huaca | Odoo 18 (TAMAL) | TAMAL | Mayor volumen ERP (~5.600 facturas) |
| SMRC | Odoo 18 + FE HKA | TAMAL | Facturación electrónica Panamá activa |
| SANAGUA LODGE | Odoo 18 + FE HKA | TAMAL | Sin subdominio público dedicado |
| T & T Tourism Plus | Odoo 18 + FE HKA | TAMAL | |
| BI Consulting | Landing Flask | OCI | `biconsultingpma.com` |
| Mustang Basketball Academy | Landing estática | OCI | |
| Detailing Service VE | Landing estática | OCI | |
| AA Transporte | Landing estática | OCI | Sin repo Git aprobado |
| Refrigeración SJ | Landing + API leads | OCI | Sin repo Git aprobado |

**Documentación completa:** [[04_Clientes/modecosa]] · [[04_Clientes/iius]] · [[04_Clientes/clientes_generales]]

---

## 5. Roadmap Oficial (2026)

**Fuente única:** [[10_Roadmap/roadmap_2026]]

### Q1–Q2 2026 (consolidado)

| Prioridad | Tema | Estado |
|-----------|------|--------|
| Alta | EN1 ERP operativo (contactos, pagos Yappy, taller SLA, eventos, certificados) | ✅ Desplegado |
| Alta | Easy Wiki MVP (estructura + repo Git) | ✅ Completado |
| Alta | Estabilidad producción (deploy con migraciones) | ✅ Activo |
| Media | IIUS campus cerrado + programas + pagos | ✅ Activo |
| Media | Modecosa Odoo catálogo seguridad v1 | ✅ Fase 1 entregada |
| Media | Facturación electrónica Panamá | ✅ Fase inicial |

### Q3 2026 (planificado)

| Prioridad | Tema |
|-----------|------|
| Media | ePosOne — ficha comercial + pilotos |
| Media | Easy Wiki fase 2 (completar proyectos y operaciones) |
| Media | Marketing — campañas coordinadas |
| Baja | Easy Operator (IA) — prototipo interno |

### Q4 2026 (visión)

| Prioridad | Tema |
|-----------|------|
| Media | Publicación wiki (sitio estático / intranet) |
| Media | EPayRoll / EThesisOne — según demanda comercial |
| Baja | Integraciones adicionales |

---

## 6. Gobierno Tecnológico

### Principios

1. **Una fuente de verdad por producto** — código en Git; documentación en Easy Wiki.
2. **No tocar producción a mano** — solo despliegue acordado.
3. **Cliente = datos sagrados** — migraciones y actualizaciones sin borrar información.
4. **IA asistida, humano responsable** — decisiones finales del equipo.
5. **Naming y marca** — convenciones documentadas.

### Jerarquía de fuentes

```
Easy Wiki  >  GitHub oficial  >  Roadmap  >  Conversaciones informales
```

### Reglas operativas

| Qué | Dónde vive |
|-----|------------|
| Código fuente | GitHub (`shidalgo0925/*`) |
| Documentación operativa | Easy Wiki (este repositorio) |
| Procedimientos técnicos | `07_Operaciones/` |
| Proyectos por cliente | `05_Proyectos/` |
| Roadmap y prioridades | `10_Roadmap/` |

**Documentación completa:** [[00_Gobierno/gobierno_tecnologico]]

---

## 7. Reglas para IA

### Cómo debe trabajar una IA dentro de EasyTech

#### Fuentes oficiales (orden de prioridad)

1. **Easy Wiki** — verdad operativa documentada.
2. **GitHub oficial** — código fuente y versionamiento.
3. **Roadmap** — prioridades comprometidas.
4. **Documentación de proyecto** — alcance, contactos, notas (`05_Proyectos/`).

#### Orden de prioridad absoluto

```
Easy Wiki > GitHub > Roadmap > Conversaciones
```

#### Reglas obligatorias

| # | Regla | Por qué |
|---|-------|---------|
| 1 | **No asumir** | La documentación existe para evitar suposiciones. Si no está en wiki, preguntar o documentar el hallazgo. |
| 2 | **Verificar documentación antes de actuar** | Antes de proponer cambios, confirmar que la información está actualizada en wiki. |
| 3 | **Documentar hallazgos** | Si se descubre información nueva o un error, actualizar la wiki correspondiente. |
| 4 | **Actualizar Wiki cuando corresponda** | Después de cualquier cambio significativo, la wiki debe reflejar el estado actual. |
| 5 | **Diferenciar hechos de inferencias** | Marcar claramente cuando algo es una inferencia vs. un hecho documentado. |
| 6 | **No subir secretos** | Contraseñas, `.env`, tokens nunca a chats públicos. |
| 7 | **Código solo en entornos autorizados** | Git, Cursor con reglas de empresa. |
| 8 | **Producción no se toca solo por sugerencia de IA** | Siempre checklist humano antes de deploy. |

#### Flujo típico de trabajo con IA

```text
Idea / incidencia
    → Analista (IA): clarifica y documenta borrador en Easy Wiki
    → Programador (Cursor): implementa en Git, pruebas en dev
    → Humano: valida en staging, despliega a prod, avisa al cliente
```

**Documentación completa:** [[08_IA/equipo_virtual]] · [[08_IA/easy_operator]]

---

## 8. Estado Actual

| Área | Estado | Nota |
|------|--------|------|
| **Infraestructura** | 🟡 Estable con riesgos | TAMAL backup activo a OCI; CODITO backup off-site diseñado pero pendiente; OCI landings estables |
| **Productos** | 🟢 EN1 producción activa | EClassOne/EThesisOne en labs; ePosOne/EPayRoll sin código |
| **Clientes** | 🟢 Activos | Relatic, IIUS, Modecosa Fase 1, 6 clientes ERP en TAMAL |
| **Marketing** | 🟡 Documentación viva | Marketing Hub como wiki; campañas Q3 planificadas |
| **IA** | 🟡 Laboratorio operativo | Open WebUI + LiteLLM + Ollama en CODITO; Easy Operator planificado Q3 |
| **Roadmap** | 🟢 Al día | Q1–Q2 ejecutado; Q3 planificado; Q4 visión clara |
| **Operaciones** | 🟡 En construcción | Deploy, soporte, QA documentados; Easy Wiki fase 2 en curso |
| **Gobierno** | 🟡 MVP avanzado | Principios definidos; faltan formalizaciones (misión/visión aprobadas por dirección) |

**Leyenda:** 🟢 Saludable · 🟡 En progreso / con riesgos · 🔴 Crítico

---

## 9. Glosario

| Término | Definición |
|---------|------------|
| **EN1** / Easy NodeOne | Plataforma modular central de EasyTech (Flask, PostgreSQL, multi-tenant). |
| **Relatic** | App EN1 en producción para Relatic Panamá (membresías, pagos). |
| **Easy Suite** | Marca paraguas de todos los productos EasyTech. |
| **App EN1** | Instancia desplegada de EN1 con identidad propia (silo + config + BD + dominio). |
| **Tenant / Organización** | Cliente lógico dentro de una App EN1. |
| **Módulo EN1** | Feature activable por organización (`workshop`, `academic`, `payments`, etc.). |
| **Silo** | Despliegue físico de EN1 (dev, staging, prod, relatic). |
| **DR** | Disaster Recovery — plan de recuperación ante desastre. |
| **Easy Wiki** | Documentación viva operativa de EasyTech (Obsidian-style + Git). |
| **TAMAL** | Servidor ERP principal (Odoo 18 Community, Contabo). |
| **CODITO** | Servidor producción EN1 + labs + IA (Contabo). |
| **OCI** | Oracle Cloud Infrastructure — landings clientes + backup hub. |
| **SPAGUETTI** | Servidor no documentado en wiki (pendiente de inventario). |
| **MVP** | Minimum Viable Product — producto mínimo viable. |
| **SaaS** | Software as a Service — software multi-tenant bajo suscripción. |
| **FE** | Facturación Electrónica (Panamá vía HKA). |
| **Easy Operator** | Asistente IA interno planificado (lector de wiki + repos). |

---

## Referencias cruzadas

| Tema | Documento |
|------|-----------|
| Empresa | [[01_Empresa/easytechnology]] |
| Misión | [[00_Gobierno/mision]] |
| Visión | [[00_Gobierno/vision]] |
| Valores | [[00_Gobierno/valores]] |
| Arquitectura de producto | [[01_Arquitectura_Producto/easy_suite_architecture]] |
| Suite y productos | [[02_Suite/easy_suite]] · [[02_Suite/mapa_suite]] |
| Inventario despliegue | [[02_Suite/inventario_easy_suite]] |
| Clientes | [[04_Clientes/iius]] · [[04_Clientes/modecosa]] · [[04_Clientes/clientes_generales]] |
| Infraestructura | [[06_Arquitectura/servidores/CODITO]] · [[06_Arquitectura/servidores/TAMAL]] · [[06_Arquitectura/servidores/OCI]] |
| Gobierno | [[00_Gobierno/gobierno_tecnologico]] |
| DR CODITO | [[00_Gobierno/disaster_recovery_codito]] |
| Roadmap | [[10_Roadmap/roadmap_2026]] |
| Equipo virtual IA | [[08_IA/equipo_virtual]] · [[08_IA/easy_operator]] |

---

*Este documento es la puerta de entrada oficial a EasyTech. Para detalle técnico, seguir los enlaces internos.*