# QA (control de calidad)

Lista mínima antes de **promover un release de EN1** de staging a producción.

## Smoke test general

- [ ] Login admin plataforma y admin tenant.
- [ ] Dashboard sin error 500.
- [ ] Selector de organización (si multi-org).
- [ ] Logout y login de usuario miembro.

## Por módulo activo en staging

Marcar solo lo que el release toca o lo que el cliente usa:

| Módulo | Prueba rápida |
|--------|----------------|
| `contacts` | Crear/editar contacto |
| `sales` | Cotización guardar y enviar (si correo configurado) |
| `payments` | Checkout hasta instrucciones Yappy/transferencia |
| `workshop` | Crear OT, ver monitor SLA ([[07_Operaciones/modulo_taller]]) |
| `events` | Listar participantes, importar plantilla pequeña |
| `academic` | Inscripción programa de prueba |
| `security_matrix` | Importar catálogo Odoo (staging Modecosa) |

## Cliente IIUS (si en release)

- [ ] Usuario sin matrícula: no accede campus completo.
- [ ] Usuario con matrícula de prueba: accede `/mi-campus`.
- [ ] Landing de programa de prueba carga.

## Cliente Modecosa (si en release)

- [ ] Importación catálogo Odoo HTTP 200.
- [ ] Preview matriz muestra grupos con `xml_id`.

## Post-deploy prod

- [ ] Misma revisión Git que staging validó.
- [ ] Migración terminó sin error en log.
- [ ] Servicio `easynodeone-prod` activo.
- [ ] Aviso al cliente si hay cambios visibles.

---

**Deploy:** [[07_Operaciones/deploy]]
