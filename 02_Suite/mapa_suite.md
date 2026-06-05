# Mapa de Easy Suite

Vista rápida de **qué vendemos** y **cómo se relaciona** cada pieza.

```text
                    ┌─────────────────────────────┐
                    │   EASY TECHNOLOGY SERVICES   │
                    │      (implementación +       │
                    │         soporte)             │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │        EASY SUITE          │
                    └──────────────┬──────────────┘
         ┌─────────┬─────────┬─────┴─────┬─────────┬─────────┐
         ▼         ▼         ▼           ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
    │  EN1   │ │ ePos   │ │ EClass │ │EThesis │ │EPayRoll│ │Integr. │
    │Platform│ │  One   │ │  One   │ │  One   │ │        │ │ Odoo…  │
    └───┬────┘ └────────┘ └───┬────┘ └────────┘ └────────┘ └────────┘
        │                     │
        │    Módulos EN1 (ejemplos)
        ├── Citas / agenda
        ├── Membresías y beneficios
        ├── Tienda y pagos (Yappy, transferencia…)
        ├── Eventos y certificados
        ├── Taller (órdenes + tiempos SLA)
        ├── Ventas, cotizaciones, contactos
        ├── Campus / programas académicos
        ├── Facturación electrónica (PA)
        └── Analítica, CRM, comunicaciones
```

## Por tipo de cliente

| Necesidad del cliente | Producto principal | Complementos |
|----------------------|-------------------|--------------|
| Instituto / cursos / campus | EN1 + EClassOne | IIUS-type campus, pagos, certificados |
| Retail / ferretería / distribución | ePosOne + EN1 | Inventario (contador), contactos |
| Servicios y membresías | EN1 | Citas, pagos, marketing email |
| Taller automotriz o técnico | EN1 (módulo taller) | Ventas / cotizaciones |
| ERP + catálogo seguridad Odoo | EN1 + integración | Modecosa-type |
| Nómina interna | EPayRoll | Integración con EN1 si aplica |

## Clientes de referencia

| Cliente | Enfoque |
|-------|---------|
| [[04_Clientes/iius]] | Campus académico, inscripciones, programas |
| [[04_Clientes/modecosa]] | ERP Odoo + catálogo EN1 |
| [[04_Clientes/rycom]] | *(completar ficha)* |
| **Relatic Panamá** | EN1 producción en CODITO — ver [[06_Arquitectura/servidores/CODITO]] · [[02_Suite/inventario_easy_suite]] |
| Otros | [[04_Clientes/clientes_generales]] |

## Roadmap de la suite

[[10_Roadmap/roadmap_2026]] — prioridades 2026.

**Despliegue real (jun 2026):** EN1 y Relatic en producción en CODITO; EClassOne y EThesisOne en laboratorio/staging — detalle en [[02_Suite/inventario_easy_suite]].

---

**Inicio:** [[02_Suite/easy_suite]] · [[01_Empresa/easytechnology]]
