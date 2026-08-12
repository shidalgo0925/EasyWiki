# Decisiones Estratégicas

Registro de decisiones clave de Easy Technology Services.

---

## 2026-08-12 — ADR-037 M2M / credenciales (EN1 ↔ ESB) — propuesto

**Decisión (propuesta, pendiente ACCEPT ESB):**

Publicar **ADR-037 — Integrations M2M, Credentials & Operations** como norma de Integration Center, rotación, health y despliegue de secretos **sin** scp artesanal en PROD.

**Documento:** [[00_Gobierno/ADR/ADR-037-INTEGRATIONS-M2M-CREDENTIALS-OPERATIONS]]  
**Canónico EN1:** `Easy-NodeOne` / `develop` / `docs/ADR-037-INTEGRATIONS-M2M-CREDENTIALS-OPERATIONS.md`  
**Nota:** ADR-009 sigue siendo **Caja EN1**; no reutilizar ese número para M2M.

---

## 2026-06-08 — EasyCoach: reutilización de arquitectura existente

**Decisión:**

No desarrollar un nuevo producto desde cero.

Se reutilizará la arquitectura existente de **1% Better Every Day** para construir **EasyCoach**.

**Motivo:**

La plataforma ya contiene:

- Metas
- Hábitos
- Plan diario
- IA Planner
- Google Calendar
- Seguimiento

**Beneficio esperado:**

- Reducir tiempo de desarrollo.
- Acelerar MVP.
- Aprovechar trabajo ya realizado.