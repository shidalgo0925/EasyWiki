# Servidores e infraestructura — Easy Technology

Inventario lógico de **hosts y VPS** usados por Easy Technology Services.  
**Sin contraseñas** en ningún documento; credenciales solo en gestores internos acordados.

## Orden de documentación (acordado)

| # | Nombre lógico | Cliente / uso | Ficha | Estado doc |
|---|---------------|---------------|-------|------------|
| 1 | **CODITO** | Relatic Panamá | [[06_Arquitectura/servidores/CODITO]] | **Completa** |
| 2 | **OCI** | Landing Pages / APIs leads / Ollama auxiliar | [[06_Arquitectura/servidores/OCI]] | **Documentado y Cerrado** |
| 3 | **TAMAL** | ERP Odoo multi-tenant Contabo | [[06_Arquitectura/servidores/TAMAL]] | **Documentado** — Fase 1 Backup Hub OCI pendiente |
| 4 | **Arroz con Pollo** | Laboratorio IA / Easy Wiki / Operator | *(pendiente)* | Por hacer |
| 5 | **Spaguetti** | IIUS (EN1) | *(pendiente)* | Por hacer |
| 6 | **GCP histórico** | Retirado | *(pendiente)* | Por hacer |

## Clasificación (Tarea 14)

| Nombre lógico | Categoría | Notas |
|---------------|-----------|-------|
| **CODITO** | **Producción** | Cliente Relatic Panamá (silo `relatic`); mismo VPS aloja silos EasyTech |
| **OCI** | **Producción** | Landing pages + APIs leads + Ollama local; stack IA productivo en CODITO (Contabo) |
| **TAMAL** | **Producción** | Odoo 18 Community / 19 Enterprise, FE, módulos EasyTech |
| **Arroz con Pollo** | **Laboratorio** / IA | Wiki, Operator, experimentos |
| **Spaguetti** | **Producción** | Instancia EN1 IIUS |
| **GCP Desarrollo** | **Retirado** | Histórico; no usar para deploy nuevo |

Categorías válidas: Producción · Preproducción · Desarrollo · Laboratorio · Histórico · Retirado.

## Plantilla por servidor

Cada ficha incluye:

- Tareas 10–14 (propósito, dependencias, accesos, backups, clasificación)
- Resumen ejecutivo, dominios, aplicaciones, servicios, riesgos, próximos pasos

---

**Operación general EN1:** [[07_Operaciones/deploy]] · **Arquitectura EN1:** [[06_Arquitectura/arquitectura_en1]]
