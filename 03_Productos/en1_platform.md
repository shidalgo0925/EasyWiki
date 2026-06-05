# EN1 Platform (Easy NodeOne)

**EN1** es la plataforma modular de [[02_Suite/easy_suite|Easy Suite]] para operar un negocio o institución en la web: miembros, servicios, pagos, administración y **módulos activables por organización** (multi-empresa en una misma instalación).

## Para qué sirve

| Área | Qué resuelve |
|------|----------------|
| **Miembros / usuarios** | Registro, login, perfiles, membresías, portal «Mi membresía». |
| **Comercial** | Contactos, CRM, catálogo, tienda, cotizaciones, campañas email. |
| **Finanzas** | Facturas, pagos (Yappy manual, transferencia, Stripe/PayPal según config), factura electrónica Panamá. |
| **Operaciones** | Citas, taller (órdenes + SLA), eventos, certificados, contador de inventario. |
| **Educación** | Programas, inscripciones, campus cerrado hasta matrícula, integración Moodle (según tenant). |
| **Administración** | Varias empresas, roles RBAC, módulos on/off por cliente, matriz Odoo (integración). |

## Cómo lo vive el usuario

- **Panel tipo ERP**: menú lateral por áreas; pestañas horizontales dentro de cada módulo.
- **Configuración** en engranaje (correo, logo, usuarios, impuestos) separada del trabajo diario.
- **Web y app móvil** pueden compartir la misma sesión (según despliegue del cliente).
- Usuarios con **varias empresas** eligen organización tras el login.

## Multi-empresa (concepto operativo)

Cada **organización** es un «tenant»: datos, logo, métodos de pago y módulos propios. Easy Technology activa solo lo que el contrato incluye. Un usuario puede pertenecer a más de una organización.

Políticas especiales por institución (ej. campus cerrado): ver [[04_Clientes/iius]].

## Catálogo de módulos EN1 (referencia)

Estos son los módulos que la plataforma puede encender por empresa. Los marcados como **núcleo** vienen activos por defecto y no se apagan desde el admin de módulos.

| Código | Nombre en pantalla | Uso típico |
|--------|-------------------|------------|
| `payments` | Pagos | Checkout, cobros (**núcleo**) |
| `appointments` | Citas | Agenda y citas |
| `events` | Eventos | Eventos, inscripciones, participantes |
| `chatbot` | IA / Chatbots | Asistentes y configuración IA |
| `crm_contacts` | Contactos CRM | Contactos del tenant |
| `crm` | CRM | Menú y funciones comerciales |
| `marketing_email` | Marketing email | Campañas y cola de correo |
| `certificates` | Certificados | Certificados y plantillas |
| `policies` | Normativas | Políticas públicas |
| `communications` | Comunicaciones | Integraciones y mensajería |
| `office365` | Office 365 (correo) | Solicitudes de correo institucional |
| `sales` | Ventas | Cotizaciones, facturación, impuestos |
| `analytics` | Analítica | KPIs y tableros |
| `accounting` | Contabilidad | Reservado contabilidad avanzada |
| `workshop` | Taller + SLA | Órdenes de trabajo, inspección, tiempos | Ver [[07_Operaciones/modulo_taller]] |
| `academic` | Educación / LMS | Programas, matrículas, Moodle |
| `contador` | Contador | Conteos físicos de inventario |
| `contacts` | Contactos | Maestro clientes/proveedores/fiscal |
| `efactura` | Facturación electrónica | FE Panamá (PAC) |
| `qr_generator` | Generador QR | QR estáticos e historial |
| `security_matrix` | Matriz Odoo | Importar permisos desde Odoo |
| `rbac_matrix` | Permisología EN1 | Roles × permisos del tenant |
| `memberships` | Membresías | Planes, beneficios, portal miembro |

## Pagos (lo que debe saber operación)

- Métodos configurables **por organización** (no global a toda la plataforma).
- **Yappy manual**: el cliente sube comprobante; el equipo valida en administración.
- **Transferencia**: instrucciones visibles en checkout (datos bancarios del tenant).
- Checkout por **pasos** (elegir método → instrucciones → confirmar).
- Pagos completados pueden **reconciliar** matrículas académicas (IIUS) vía scripts de operación en el producto.

## Novedades recientes (junio 2026 — resumen cliente)

- Panel ERP con pestañas y sidebar por módulo.
- **Contactos** unificados para cotizaciones y facturas.
- **Ventas** y tienda con cotizaciones por correo.
- **Pagos** Yappy + transferencia por empresa.
- **Taller** con semáforo SLA por etapa.
- **Eventos**: participantes, importación masiva, certificados.
- **Facturación electrónica** Panamá (fase inicial, si el módulo está activo).
- **Campus académico cerrado** para instituciones tipo IIUS.

## Implementación y entornos

Easy Technology despliega EN1 en silos controlados:

| Silo | Uso |
|------|-----|
| Desarrollo | Donde se escribe código y se hace commit |
| Staging | Pruebas antes de producción |
| Producción | Clientes en vivo |

**Regla:** no se edita código a mano en staging/prod; solo actualización desde Git + migraciones + reinicio. Detalle: [[07_Operaciones/deploy]].

## Presencia en CODITO (jun 2026)

Host compartido `194.60.201.29` — inventario completo: [[02_Suite/inventario_easy_suite]].

| Silo | Dominio | BD | Comercial |
|------|---------|-----|-----------|
| Dev | `appdev.easynodeone.com` | `easynodeone_dev` | Laboratorio |
| Staging | `apptst.easynodeone.com` | `easynodeone_staging` | Staging |
| Prod | `appprd.easynodeone.com` | `easynodeone_prod` | Producción |
| Relatic | `apps.relatic.org`, `miembros.relatic.org` | `easynodeone_relatic` | Producción (cliente) |

Repo: `github.com/shidalgo0925/Easy-NodeOne` · ramas `develop` (dev/relatic) y `main` (staging/prod).

Proyecto interno wiki: `05_Proyectos/en1/`

## Clientes de referencia en wiki

- [[04_Clientes/iius]] — campus, programas, matrícula.
- [[04_Clientes/modecosa]] — Odoo 19 + catálogo de seguridad EN1.

## Arquitectura (resumen)

[[06_Arquitectura/arquitectura_en1]] — capas, autenticación, integraciones.

## Productos relacionados

- [[03_Productos/eposone]] — punto de venta.
- [[03_Productos/eclassone]] — aula / campus (concepto suite).
- [[03_Productos/integrations]] — Odoo y otros ERP.

---

**Suite:** [[02_Suite/mapa_suite]] · **Empresa:** [[01_Empresa/easytechnology]]
