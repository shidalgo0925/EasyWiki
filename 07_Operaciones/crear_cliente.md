# Crear cliente (nuevo tenant EN1)

Checklist para **dar de alta una organización nueva** en EN1 o preparar un proyecto Easy Technology.

## 1. Datos comerciales

- Razón social y nombre corto para la plataforma.
- Dominio o subdominio deseado (si aplica).
- Contacto principal (email, teléfono).
- Módulos contratados (ver catálogo en [[03_Productos/en1_platform]]).

## 2. Alta en plataforma (operación)

| Paso | Acción |
|------|--------|
| 1 | Crear **organización** en admin plataforma |
| 2 | Activar **módulos SaaS** acordados (no activar todo «por si acaso») |
| 3 | Crear usuario admin del tenant y asignar organización |
| 4 | Configurar logo, correo saliente, métodos de pago |
| 5 | Si es académico: definir política de registro (`academic_closed` u otra) |

## 3. Entorno

- Desarrollo / staging primero.
- Producción solo tras QA y ventana acordada ([[07_Operaciones/deploy]]).

## 4. Documentación wiki

- Ficha en `04_Clientes/` (copiar plantilla de [[04_Clientes/clientes_generales]]).
- Carpeta en `05_Proyectos/<nombre>/README.md` con contactos y URLs.

## 5. Entrega al cliente

- Usuarios iniciales y enlace de acceso.
- Mini manual de lo que **sí** tienen activo (módulos).
- Canal de soporte ([[07_Operaciones/soporte]]).

---

**Relacionado:** [[07_Operaciones/crear_proyecto]]
