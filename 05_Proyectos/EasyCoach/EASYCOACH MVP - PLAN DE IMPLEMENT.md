# EASYCOACH MVP - PLAN DE IMPLEMENTACIÓN COMPLETO

## Objetivo

Construir la primera versión funcional de EasyCoach utilizando como base el proyecto 1% Better Every Day.

La primera versión NO debe enfocarse en IA avanzada.

La primera versión debe resolver:

"¿Qué debo hacer hoy para acercarme a mis metas?"

---

# FASE 0 - LEVANTAMIENTO

## Objetivos

Analizar el código existente.

Inventariar:

* Modelos
* Rutas
* Servicios
* Templates
* Integraciones Google Calendar
* Integraciones IA

## Entregable

Documento:

ANALISIS_ACTUAL.md

---

# FASE 1 - REBRANDING

## Objetivo

Transformar conceptualmente:

1% Better Every Day

en

EasyCoach

## Cambios

Actualizar:

* Nombre aplicación
* Menús
* Dashboard
* Logo temporal
* Descripciones

NO eliminar funcionalidad existente.

## Entregable

Sistema funcionando bajo nombre EasyCoach.

---

# FASE 2 - NUEVO MODELO DE DATOS

## Crear modelos

### visions

Campos:

* id
* title
* description
* created_at
* updated_at

### projects

Campos:

* id
* name
* description
* status
* priority

### objectives

Campos:

* id
* project_id
* title
* description
* target_date
* status

### daily_focus

Campos:

* id
* user_id
* focus_date
* primary_goal
* secondary_goal
* notes

### daily_reflections

Campos:

* id
* user_id
* reflection_date
* wins
* blockers
* next_actions

## Entregable

Migraciones completas.

---

# FASE 3 - DASHBOARD EJECUTIVO

## Objetivo

Pantalla principal.

Mostrar:

Visión actual

Objetivos activos

Prioridad principal

Proyecto principal

Próxima acción

Pendientes

Calendario de hoy

## NO mostrar

Métricas irrelevantes.

## Entregable

Dashboard responsive.

---

# FASE 4 - PLAN DIARIO

## Objetivo

Permitir registrar:

Hoy quiero lograr:

* Acción 1
* Acción 2
* Acción 3

Cada acción debe tener:

* Prioridad
* Tiempo estimado
* Estado

## Entregable

Plan diario operativo.

---

# FASE 5 - CIERRE DEL DÍA

## Objetivo

Registrar:

¿Qué lograste?

¿Qué aprendiste?

¿Qué te bloqueó?

¿Qué harás mañana?

## Entregable

Bitácora diaria.

---

# FASE 6 - SISTEMA DE COACHING

## Objetivo

Crear flujo inicial.

Preguntas:

¿Qué quieres lograr?

¿Por qué?

¿Cuál es tu situación actual?

¿Qué te impide avanzar?

¿Cuál sería una victoria dentro de 12 meses?

Guardar respuestas.

## Entregable

Wizard de onboarding.

---

# FASE 7 - GOOGLE CALENDAR

## Objetivo

Reutilizar integración existente.

Mostrar:

Eventos de hoy.

Eventos próximos.

Permitir asociar tareas a eventos.

## Entregable

Agenda integrada.

---

# FASE 8 - MOTOR DE RECOMENDACIONES

SIN IA.

Reglas simples.

Ejemplos:

Si no existe plan diario:
Mostrar sugerencia.

Si existen objetivos atrasados:
Mostrar alerta.

Si no hay actividad en 3 días:
Mostrar recordatorio.

Si se cumple objetivo:
Mostrar reconocimiento.

## Entregable

Motor basado en reglas.

---

# FASE 9 - IA KIMI

NO IMPLEMENTAR HASTA APROBACIÓN.

Preparar arquitectura.

Crear:

services/coach_ai.py

Diseñar:

Context Builder

Prompt Builder

Memory Builder

Sin consumir API todavía.

## Entregable

Arquitectura preparada.

---

# FASE 10 - DOCUMENTACIÓN

Actualizar EasyWiki.

Crear:

* Arquitectura
* Base de datos
* Flujo usuario
* Roadmap
* Manual técnico

## Entregable

Documentación completa.

---

# CRITERIO DE ÉXITO MVP

Al finalizar el MVP el usuario debe poder:

1. Definir visión.
2. Definir objetivos.
3. Definir proyectos.
4. Crear plan diario.
5. Registrar cierre del día.
6. Consultar calendario.
7. Recibir recomendaciones básicas.

La IA avanzada queda fuera del MVP.

---

# RESTRICCIÓN

NO construir nuevas funcionalidades fuera de este documento.

Cualquier desviación requiere aprobación previa.

Objetivo principal:

Entregar MVP funcional antes de incorporar Kimi, OpenRouter o cualquier arquitectura multi-modelo.
