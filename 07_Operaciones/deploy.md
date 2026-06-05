# Deploy (procedimiento)

1. Cambios en Git (develop → main según política).  
2. Validar en **staging**.  
3. Ventana acordada con el cliente si es prod.  
4. `git pull` en el servidor del cliente + migraciones + reinicio.  
5. Verificación: login, pantalla crítica, sin error visible.  
6. Comunicado al cliente si aplica.

*Detalle técnico EN1: repositorio Easy-NodeOne — no duplicar aquí en MVP.*
