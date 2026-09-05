# ANNY: Updates and Migrations

El código kernel de ANNY está diseñado para evolucionar. Periódicamente, publicaremos nuevas versiones en nuestro repositorio oficial.

## Principio de Inmutabilidad
Tu información, misiones, decisiones y evidencia (estado de instancia) **nunca** se perderán en una actualización. El Kernel de ANNY está completamente separado de tus datos operativos.

## Cómo actualizar
1. Descarga el nuevo archivo de release (ej. `ANNY-v1.1.0.zip`).
2. Descomprime el paquete.
3. Copia el nuevo contenido de los directorios del kernel (`schemas/`, `governance/`, `genesis/`, etc.) sobreescribiendo los archivos en tu repositorio local.
4. Ejecuta el commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Update ANNY Kernel to v1.1.0"
   git push origin main
   ```
5. En tu próximo inicio de sesión con ANNY, el sistema detectará la nueva versión del kernel y aplicará las migraciones de esquema necesarias de forma automática.
