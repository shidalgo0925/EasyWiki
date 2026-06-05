# Cursor — programador (IA)

**Cursor** es el entorno de desarrollo asistido por IA que usa Easy Technology para **EN1, integraciones y scripts**.

## Para qué lo usamos

- Implementar módulos Flask, APIs JSON, plantillas y migraciones.
- Revisar código existente antes de un release.
- Redactar documentación técnica en el **repositorio del producto** (no sustituye Easy Wiki para el cliente).

## Reglas

1. Código solo en **`dev/app`**; commits en rama acordada (`develop`).
2. Reglas del proyecto: no editar staging/prod a mano ([[07_Operaciones/deploy]]).
3. No pegar `.env`, API keys ni contraseñas en el chat.
4. Toda sugerencia de IA se **prueba** en dev/staging antes de prod.

## Flujo con el equipo humano

```text
Ticket / historia → Cursor en dev → pruebas locales → commit → staging QA → prod
```

Ver [[08_IA/equipo_virtual]].
