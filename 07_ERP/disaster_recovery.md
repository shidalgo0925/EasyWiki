# Disaster Recovery — EasyTech ERP (TAMAL)

Documento de **continuidad operativa** para el ERP Odoo 18 en TAMAL.  
Actualizado: **2026-06-05** — tras validación completa export → OCI → restore real.

---

## Resumen ejecutivo

El respaldo PostgreSQL de TAMAL dejó de ser una suposición. Se validó el pipeline completo:

```
TAMAL → pg_dump -Fc → OCI Backup Hub → pg_restore → base funcional
```

**Estado:** capacidad de recuperación **confirmada** para bases productivas. Cron diario activo desde 2026-06-05.

| Campo | Valor |
|---|---|
| **Servidor origen** | TAMAL — `217.216.80.159` (Contabo) |
| **Backup Hub** | OCI — `40.233.1.138` (`backupsrv@…:/backups/tamal/`) |
| **RPO** | **24 h** (backup diario 02:00 CEST) |
| **RTO estimado (1 BD)** | **1–2 h** (descarga dump + `pg_restore` + verificación SQL) |
| **RTO estimado (TAMAL completo)** | **4–8 h** (rebuild VM + 6 BD + nginx/Odoo; filestore aparte) |
| **Responsable operativo** | **EasyTech** — operador infra (`shidalgo`) |
| **Responsable técnico** | Equipo EasyTech / Cursor agent bajo supervisión humana |

---

## Riesgos críticos — registro

| ID | Riesgo | Severidad | Estado | Fecha cierre | Commit referencia |
|---|---|---|---|---|---|
| **R-001** | TAMAL sin backups automáticos de PostgreSQL | Crítico | **RESUELTO** | 2026-06-05 | [`63347e9`](https://github.com/shidalgo0925/EasyWiki/commit/63347e9) |

### R-001 — Detalle de cierre

| Fase | Resultado |
|---|---|
| Fase 1 | Conexión TAMAL → OCI Backup Hub (SSH + scp) |
| Fase 2 | Dump manual Easydb validado |
| Fase 2.5 | Inventario 6 bases (~74 MB/día) |
| Fase 3 | Script `/usr/local/bin/backup_postgresql_tamal.sh` |
| Fase 5 | Restore real **Easydb** + **lahuaca** (5 968 facturas) |
| Fase 4 | Cron 02:00 backup · 04:00 verify |

**Periodo de observación (2026-06-05 → ~2026-06-12):** no modificar TAMAL salvo incidente. Revisar logs, espacio OCI, errores y tiempos diarios.

### Riesgos abiertos relacionados (TAMAL)

| ID | Riesgo | Estado |
|---|---|---|
| R-TAMAL-02 | Single point of failure (1 Odoo, 1 PG) | Abierto |
| R-TAMAL-03 | Filestore sin backup dedicado (`/var/lib/odoo/filestore`) | Abierto |
| R-TAMAL-04 | Tar código custom desactualizado (oct-2025) | Abierto |

Ver [[06_Arquitectura/servidores/TAMAL#Riesgos operativos]].

---

## Ubicación de backups

### TAMAL (origen)

| Recurso | Ruta |
|---|---|
| Dumps diarios | `/backups/tamal/db/YYYY-MM-DD/{Base}.dump` |
| Log backup | `/backups/tamal/logs/backup_postgresql_tamal_YYYY-MM-DD.log` |
| Log verify | `/backups/tamal/logs/verify_backup_postgresql_tamal_YYYY-MM-DD.log` |
| Clave → OCI | `/root/.ssh/id_ed25519_backup_oci` |

### OCI Backup Hub (off-site)

| Recurso | Ruta |
|---|---|
| Dumps diarios | `/backups/tamal/YYYY-MM-DD/{Base}.dump` |
| Usuario | `backupsrv@40.233.1.138` |
| Referencia hub | [[06_Arquitectura/servidores/OCI#Backup Hub]] |

### Bases incluidas en backup automático

| Base | Cliente | Tamaño dump ref. |
|---|---|---:|
| Easydb | Easy Technology Services | 9.7 MB |
| lahuaca | La Huaca | 16 MB |
| SMRC | Servicios Múltiples RC | 13 MB |
| Sanadb | SANAGUA LODGE | 9.5 MB |
| TTTourism | T & T Tourism Plus | 9.7 MB |
| relatic | Relatic / Multiservicios TK | 17 MB |

**Excluida:** `odoo18` (laboratorio).  
**Total referencia:** ~74 MB/día → ~2.2 GB/mes (30 días retención manual; política retención formal pendiente).

### No cubierto por cron PostgreSQL

- **Filestore Odoo** — adjuntos en `/var/lib/odoo/filestore` (~283 MB)
- **Código custom** — `/opt/odoo/custom-addons` (Git + tar manual desactualizado)
- **Config nginx / odoo.conf** — en disco; documentado en wiki
- **EConverso** — app separada

---

## Automatización activa

Archivo cron: `/etc/cron.d/backup-postgresql-tamal`

| Hora (servidor) | Acción |
|---|---|
| **02:00** | `backup_postgresql_tamal.sh` — dump + `pg_restore --list` + scp OCI |
| **04:00** | `verify_backup_postgresql_tamal.sh` — compara tamaños local vs OCI (6/6) |

Ejecución manual: `sudo /usr/local/bin/backup_postgresql_tamal.sh`

---

## Validaciones realizadas (2026-06-05)

| Prueba | Base | Método | Resultado |
|---|---|---|---|
| Integridad dump | 6 bases prod. | `pg_restore --list` | ✅ sin errores |
| Transferencia | 6 bases | scp → OCI, tamaños iguales | ✅ |
| **Restore real** | Easydb | `pg_restore` → base temporal | ✅ conteos idénticos |
| **Restore real** | lahuaca | `pg_restore` → base temporal | ✅ 5 968 `account_move` |
| Verify script | 6 bases | local = remoto bytes | ✅ 6/6 |
| Cron Fase 4 | — | `/etc/cron.d/backup-postgresql-tamal` | ✅ activo |

Detalle técnico: [[06_Arquitectura/servidores/TAMAL#Backup Hub OCI — Fase 5 (restauración real)]].

---

## Procedimiento de recuperación — una base PostgreSQL

**Escenario:** corrupción o pérdida de una BD Odoo; servidor TAMAL operativo.

### Prerrequisitos

- Acceso root a TAMAL (o servidor destino con PostgreSQL 16 + Odoo 18)
- Dump disponible en TAMAL local **o** descargar desde OCI:

```bash
# Desde TAMAL — ejemplo lahuaca
DUMP=/backups/tamal/db/YYYY-MM-DD/lahuaca.dump

# Desde OCI vía TAMAL
scp -i /root/.ssh/id_ed25519_backup_oci backupsrv@40.233.1.138:/backups/tamal/YYYY-MM-DD/lahuaca.dump /tmp/
```

### Pasos

1. **Detener escrituras** — coordinar con operador; no conectar usuarios a la BD afectada.
2. **Crear BD vacía** (nombre según política; en prueba se usó `{base}_restore_YYYYMMDD`):

```bash
sudo -u postgres createdb lahuaca_restored
```

3. **Restaurar:**

```bash
sudo -u postgres pg_restore -d lahuaca_restored --no-owner --no-acl /ruta/lahuaca.dump
```

4. **Validar SQL:**

```sql
SELECT count(*) FROM pg_tables WHERE schemaname='public';
SELECT count(*) FROM res_company, res_users, account_move;
SELECT name FROM res_company;
```

5. **Conectar Odoo** — solo tras aprobación explícita: renombrar/reemplazar BD o ajustar nginx `db=` (fuera de alcance DR automático).
6. **Filestore** — si la BD se restaura a fecha anterior, verificar adjuntos en `/var/lib/odoo/filestore/{db}/`.

### Tiempos observados (2026-06-05)

| Operación | Duración |
|---|---|
| Backup 6 BD + scp | ~33 s |
| Verify 6 BD | ~5 s |
| Restore Easydb | ~34 s |
| Restore lahuaca | ~41–45 s |

---

## Procedimiento de recuperación — disaster total TAMAL

**Escenario:** VPS Contabo perdido o irrecuperable.

| Paso | Acción | RTO contrib. |
|---|---|---|
| 1 | Provisionar VPS Ubuntu 24.04 + PostgreSQL 16 + Odoo 18 | 1–2 h |
| 2 | Restaurar `/etc/odoo/`, nginx, custom-addons (Git + tar) | 1–2 h |
| 3 | Descargar dumps OCI (6 × ~74 MB) | ~15 min |
| 4 | `pg_restore` por cada base productiva | ~5–10 min |
| 5 | Restaurar filestore (si backup disponible) | variable |
| 6 | DNS `*.etsrv.site` → nueva IP | 15 min – 24 h (TTL) |
| 7 | Validación por cliente + FE HKA (SMRC, Sanadb, TTTourism) | 1–2 h |

**RTO total estimado:** 4–8 h trabajo técnico + propagación DNS.

---

## Monitoreo post-implementación (7 días)

Revisar diariamente hasta **~2026-06-12**:

| Qué revisar | Dónde |
|---|---|
| Backup OK 6/6 | `/backups/tamal/logs/backup_postgresql_tamal_$(date +%F).log` |
| Verify OK 6/6 | `/backups/tamal/logs/verify_backup_postgresql_tamal_$(date +%F).log` |
| Espacio OCI | `ssh backupsrv@40.233.1.138 'du -sh /backups/tamal/'` |
| Errores cron | `grep -i error /backups/tamal/logs/*$(date +%F)*` |
| Duración | timestamps inicio/fin en logs |

---

## Responsables

| Rol | Responsable | Acción |
|---|---|---|
| **Dueño infra ERP** | EasyTech | Política DR, aprobación restore prod. |
| **Operador** | shidalgo | Ejecución restore, revisión logs 7 días |
| **Backup Hub OCI** | EasyTech | Espacio, acceso `backupsrv`, retención |
| **Clientes ERP** | Por base | Comunicación si incidente > 1 h downtime |

---

## Próximo activo crítico — CODITO

TAMAL y OCI Backup Hub quedan **documentados y protegidos**. El siguiente proyecto de continuidad:

| Servidor | Contenido crítico | Pregunta abierta |
|---|---|---|
| **CODITO** | EN1 Relatic, Open WebUI, LiteLLM, IA principal | ¿Qué pasa si mañana se pierde CODITO? |

Ver [[06_Arquitectura/servidores/CODITO]]. Proyecto DR CODITO: **pendiente** (prioridad infra 2026).

---

## Referencias

- [[06_Arquitectura/servidores/TAMAL]] — ficha completa + fases backup
- [[07_ERP/odoo18_community]] — bases y cron
- [[06_Arquitectura/servidores/OCI]] — Backup Hub
- Commit cierre R-001: `63347e9`

---

*Un backup no existe hasta que una restauración ha sido validada. TAMAL cumple ese criterio para Easydb y lahuaca (2026-06-05).*
