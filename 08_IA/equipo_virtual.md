# Equipo virtual (IA)

Easy Technology Services usa un **equipo virtual de inteligencia artificial** para acelerar trabajo; las decisiones y la responsabilidad final son **humanas**.

## Roles

| Rol | Herramienta | Para qué lo usamos |
|-----|-------------|-------------------|
| **Analista** | ChatGPT (y similares) | Requisitos, resúmenes, correos al cliente, revisión de procesos, borradores de wiki. |
| **Programador** | Cursor | Desarrollo EN1, ePosOne, scripts, revisión de código, documentación técnica en repo. |
| **Móvil / consulta rápida** | Kimi (u otra) | Consultas en campo, ideas cortas *(uso según política interna)*. |
| **Operador futuro** | Easy Operator *(planeado)* | Unificar consultas sobre wiki + repos + estado de proyectos. |

Detalle por herramienta:

- [[08_IA/chatgpt_analista]]  
- [[08_IA/cursor_programador]]  
- [[08_IA/kimi_mobile]]  
- [[08_IA/easy_operator]]  

## Reglas de uso

1. **No subir secretos** (contraseñas, `.env`, tokens) a chats públicos.  
2. **Código fuente** solo en entornos autorizados (Git, Cursor con reglas de empresa).  
3. **Cliente** recibe textos revisados por una persona (marketing, soporte, legal si aplica).  
4. **Producción** no se toca solo por sugerencia de IA — siempre checklist humano ([[07_Operaciones/deploy]]).  
5. **Wiki** ([[00_Inicio]]) es la memoria estable; la IA ayuda a redactar, no sustituye el repo Git.

## Flujo típico de trabajo

```text
Idea / incidencia
    → Analista (IA): clarifica y documenta borrador en Easy Wiki
    → Programador (Cursor): implementa en Git, pruebas en dev
    → Humano: valida en staging, despliega a prod, avisa al cliente
```

## Beneficio para el cliente

- Respuestas y entregas **más rápidas**.  
- Documentación y manuales **más completos**.  
- Mismo estándar de calidad porque hay **checklist** y [[00_Gobierno/gobierno_tecnologico]].

## Relación con esta wiki

Easy Wiki es el lugar donde el equipo (humano + IA) deja **verdad operativa**: productos, clientes, roadmap, procedimientos.

---

**Empresa:** [[01_Empresa/easytechnology]] · **Roadmap:** [[10_Roadmap/roadmap_2026]]
