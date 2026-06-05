# IIUS (cliente)

**IIUS** es el cliente de referencia de [[01_Empresa/easytechnology|Easy Technology Services]] sobre [[03_Productos/en1_platform|EN1 Platform]] con enfoque **educación, inscripciones en línea y campus académico cerrado**.

## Qué es IIUS (negocio)

Institución de programas formativos (diplomados, cursos, talleres, certificaciones) que necesita:

- **Landings e inscripción** por programa (slug, planes de pago).
- **Cobro en línea** (membresía, programas; PayPal u otros según configuración del tenant).
- **Campus virtual** al que solo entra quien tiene **matrícula activa** o pago confirmado.
- **Certificados y eventos** cuando los módulos SaaS correspondientes están activos.

## Política de campus: `academic_closed`

En EN1 la organización IIUS usa la política de registro **`academic_closed`** (campus cerrado). En lenguaje de negocio:

| Quién | Experiencia |
|-------|-------------|
| Administrador / roles con permiso admin | Acceso completo al panel del tenant |
| Alumno **sin** matrícula en estado válido | Puede ver dashboard e **inscribirse / pagar**; **no** navega el catálogo abierto ni el campus completo |
| Alumno **con** matrícula `paid` o `confirmed` | Accede al **campus académico** y servicios según módulos activos |

Estados de matrícula que abren campus: **`paid`**, **`confirmed`** (tabla de inscripciones académicas del producto).

Ruta principal del campus para el alumno: **`/mi-campus`** (vista campus académico).

## Qué entregamos

| Entrega | Descripción |
|---------|-------------|
| Tenant EN1 | Organización IIUS con branding y preset de colores |
| Módulo `academic` | Programas, matrículas, flujos de inscripción |
| Módulo `payments` | Checkout alineado a programas y membresías |
| Landings | URLs de inscripción y «continuar pago» por programa |
| Campus cerrado | Política `academic_closed` activa en la organización |
| Operación | Reconciliación de pagos → matrícula; scripts de validación en despliegues |
| Soporte | Canal acordado; incidencias con hora, usuario y pantalla |

## Flujo que se explica al alumno

1. Elige programa en la landing o portal.
2. Se inscribe y paga si el plan lo requiere.
3. Cuando el pago queda **confirmado** (o matrícula en estado válido), entra a **Mi campus**.
4. Certificados y eventos según lo contratado para ese programa.

Frase corta: *«Inscríbete, paga si aplica, y entra al campus cuando tu matrícula esté activa.»*

## Operación y soporte (equipo Easy)

Incidencias frecuentes y qué pedir al cliente:

| Síntoma | Revisar |
|---------|---------|
| «No veo el campus» | Estado de matrícula; si el pago quedó pendiente de validación (Yappy manual) |
| «No puedo inscribirme» | Programa publicado, fechas, cupos |
| Error tras actualización de plataforma | Si afecta solo pagos o dashboard — escalar con pantalla y usuario |

Tareas de operación en el producto (equipo técnico): reconciliar matrículas tras pagos completados; pruebas automáticas de campus en entorno de desarrollo antes de subir a producción.

## Módulos SaaS típicos en IIUS

| Módulo | Rol |
|--------|-----|
| `academic` | Programas y matrículas |
| `payments` | Cobros |
| `memberships` | Planes de membresía si aplica |
| `events` / `certificates` | Congresos y certificados |
| `marketing_email` | Comunicaciones masivas |

## Proyecto interno wiki

Detalle de alcance, URLs y contactos: [[05_Proyectos/iius/README]]

## Productos de suite

- [[03_Productos/en1_platform]] (principal)
- [[03_Productos/eclassone]] — narrativa de aula; la implementación vive en EN1 + campus

---

**Otros clientes:** [[04_Clientes/modecosa]] · [[04_Clientes/clientes_generales]]
