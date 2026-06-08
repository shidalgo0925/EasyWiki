# Ajuste Egresos Directos — Motivo OTROS: Selección Manual de Cuenta Contable

## Información General

| Campo | Valor |
|---|---|
| **Cliente** | MODECOSA |
| **Módulo Afectado** | `easytech_check_expense_reason` |
| **Tipo** | Ajuste funcional / Correción de flujo |
| **Prioridad** | Alta |
| **Estado** | Pendiente de implementación |

---

## Objetivo

Corregir el flujo de egresos directos sin factura en el módulo `easytech_check_expense_reason`, para que cuando el usuario seleccione el motivo **OTROS**, el sistema permita escoger manualmente la cuenta contable que se usará como contrapartida del pago.

---

## Contexto Funcional

Actualmente los egresos directos usan un catálogo de motivos para asignar automáticamente una cuenta contable.

| Motivo | Comportamiento Actual |
|---|---|
| PLANILLA | Cuenta automática |
| DÉCIMO | Cuenta automática |
| PRESTACIONES | Cuenta automática |
| VIÁTICOS | Cuenta automática |
| CAJA MENUDA | Cuenta automática |
| REEMBOLSO | Cuenta automática |
| IMPUESTOS | Cuenta automática |
| SERVICIOS PROF. | Cuenta automática |
| GASTOS ADMIN. | Cuenta automática |
| **OTROS** | **Debe permitir selección manual** |

El motivo **OTROS** es especial porque puede representar diferentes tipos de gastos. Por eso el usuario debe poder seleccionar la cuenta contable manualmente.

---

## Reglas Funcionales Requeridas

### Cuando el usuario seleccione el motivo OTROS:

- El campo de cuenta contable debe quedar **visible**.
- El campo de cuenta contable debe quedar **editable**.
- El campo de cuenta contable debe ser **obligatorio**.
- La cuenta seleccionada debe **guardarse en el pago**.
- Esa cuenta debe usarse como **contrapartida contable** del asiento del egreso.
- Debe mantenerse **obligatorio el comentario/motivo adicional** para auditoría.

### Cuando el usuario seleccione cualquier otro motivo distinto de OTROS:

- La cuenta debe asignarse **automáticamente** desde la configuración del motivo.
- El campo de cuenta contable debe quedar **no editable o bloqueado**.
- No se debe permitir cambiar manualmente la cuenta.
- El asiento contable debe usar la cuenta configurada en el motivo.

---

## Alcance Técnico

| Campo | Valor |
|---|---|
| **Módulo afectado** | `easytech_check_expense_reason` |
| **Modelo principal esperado** | `account.payment` |
| **Campos involucrados esperados** | `expense_reason_id`, `expense_reason_code`, `expense_account_id`, `expense_reason_note` |
| **Nota** | Ajustar nombres reales según el código existente |

---

## Comportamiento Esperado en Pantalla

### Caso 1 — Motivo diferente de OTROS (Ejemplo: VIÁTICOS)

| Campo | Estado |
|---|---|
| Motivo | VIÁTICOS |
| Cuenta contable | Se llena automáticamente |
| Cuenta contable | **No editable** |
| Comentario | Obligatorio si ya estaba definido por la regla actual |

### Caso 2 — Motivo OTROS

| Campo | Estado |
|---|---|
| Motivo | OTROS |
| Cuenta contable | **Visible** |
| Cuenta contable | **Editable** |
| Cuenta contable | **Obligatorio** |
| Comentario | **Obligatorio** |

---

## Validaciones Obligatorias

### Validación 1 — Cuenta contable vacía en OTROS

**Condición:** `Motivo = OTROS` y `Cuenta contable está vacía`

**Acción:** Impedir guardar/publicar el pago.

**Mensaje sugerido:**
> Debe seleccionar una cuenta contable cuando el motivo del egreso es OTROS.

---

### Validación 2 — Comentario vacío en OTROS

**Condición:** `Motivo = OTROS` y `Comentario está vacío`

**Acción:** Impedir guardar/publicar el pago.

**Mensaje sugerido:**
> Debe indicar una descripción o justificación cuando el motivo del egreso es OTROS.

---

## Reglas Contables

### Para egresos directos sin factura:

| Débito | Crédito |
|---|---|
| Banco / Caja / Diario de pago | Cuenta contable del motivo |

### Si el motivo es OTROS:

| Débito | Crédito |
|---|---|
| Banco / Caja / Diario de pago | **Cuenta seleccionada manualmente por el usuario** |

**Importante:** No debe tomar una cuenta genérica fija.

---

## Criterios de Aceptación

El cambio se considera correcto si cumple:

- [ ] Al seleccionar OTROS, aparece/habilita la cuenta contable manual.
- [ ] El usuario no puede confirmar el pago OTROS sin cuenta.
- [ ] El usuario no puede confirmar el pago OTROS sin comentario.
- [ ] El asiento contable usa la cuenta seleccionada manualmente.
- [ ] Al seleccionar otro motivo, la cuenta se llena automáticamente.
- [ ] Al seleccionar otro motivo, la cuenta no queda editable.
- [ ] No se rompe el flujo actual de egresos directos.
- [ ] No afecta pagos asociados a facturas.
- [ ] Funciona por compañía.
- [ ] Respeta permisos contables actuales.

---

## Pruebas Mínimas

| Prueba | Escenario | Resultado Esperado |
|---|---|---|
| **Prueba 1** | OTROS sin cuenta | Debe bloquear y mostrar mensaje de validación |
| **Prueba 2** | OTROS con cuenta y comentario | Debe permitir guardar/publicar y generar asiento usando la cuenta seleccionada |
| **Prueba 3** | VIÁTICOS | Debe asignar cuenta automática, no permitir editar cuenta, generar asiento con cuenta configurada |
| **Prueba 4** | Cambiar de VIÁTICOS a OTROS | Debe limpiar o desbloquear la cuenta, obligar selección manual |
| **Prueba 5** | Cambiar de OTROS a PLANILLA | Debe reemplazar cuenta manual por cuenta automática del motivo, bloquear edición manual |

---

## Commit Sugerido

```bash
git add easytech_check_expense_reason
git commit -m "fix: allow manual expense account for OTROS direct payments"
```

---

## Notas Importantes

1. **No crear un flujo nuevo.** Es un ajuste sobre el procedimiento existente.
2. **No crear otro módulo.** Se modifica `easytech_check_expense_reason`.
3. Todos los motivos usan cuenta automática, excepto **OTROS**, que debe permitir selección manual obligatoria.
4. Este ajuste es específico para el cliente **MODECOSA**.

---

## Historial de Cambios

| Fecha | Autor | Cambio |
|---|---|---|
| 2026-06-08 | EasyTech | Creación de instrucción técnica |