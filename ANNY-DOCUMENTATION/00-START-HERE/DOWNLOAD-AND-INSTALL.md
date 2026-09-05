# ANNY: Download & Install Guide

Bienvenido a ANNY. Sigue estos pasos para instalar tu propia instancia de ANNY, la cual operará como una entidad completamente aislada, 100% bajo tu control, sin compartir memoria ni datos con ninguna otra organización.

## 1. Dónde descargar
La única fuente oficial para descargar el código fuente y el motor genérico de ANNY es el repositorio de distribución oficial en GitHub (por ejemplo, `<OFICIAL_DISTRIBUTION_ORG>/ANNY`).

## 2. Cómo descargar
Dirígete a la sección **Releases** en GitHub y descarga el artefacto oficial de la última versión estable, típicamente nombrado `ANNY-v1.0.0.zip`.

## 3. Cómo verificar SHA-256
Abre tu terminal y ejecuta el siguiente comando para garantizar que el archivo no ha sido alterado:
`sha256sum ANNY-v1.0.0.zip`
Compara el hash resultante con el hash público anunciado en las notas de la release (Release Manifest).

## 4. Cómo descomprimir
Extrae el contenido en una carpeta local:
`unzip ANNY-v1.0.0.zip -d anny-install`

## 5. Qué archivos/directorios aparecerán
Encontrarás la arquitectura central (Kernel) de ANNY:
- `schemas/`: Los contratos de datos.
- `genesis/`: La lógica de inicialización y generación de actores.
- `governance/`: Las reglas de autoridad y compensación (P1A).
- `starter_pack/`: El generador genérico de estructura base.
- Archivos de configuración como `requirements.txt`.
*Nota: No verás carpetas como `actors`, `missions` o `evidence` todavía; estas nacerán cuando inicialices tu instancia.*

## 6. Cómo crear el repositorio del cliente
Entra a tu propia cuenta de GitHub y crea un **nuevo repositorio privado** (ej. `tu-usuario/ANNY`).

## 7. Cómo copiar/subir ANNY
1. En tu carpeta local `anny-install`, inicializa Git: `git init`
2. Conecta con tu nuevo repositorio remoto: `git remote add origin https://github.com/tu-usuario/ANNY.git`
3. Añade los archivos y haz commit: `git add . && git commit -m "Initial ANNY installation"`
4. Sube los archivos a GitHub: `git push -u origin main`

## 8. Cómo conectar GitHub a ChatGPT
Abre la configuración de integraciones (u otorga acceso al plugin/herramienta de GitHub dentro de tu interfaz ChatGPT / agente). Deberás autorizar el acceso exclusivamente a tu nuevo repositorio `tu-usuario/ANNY`.

## 9. Cómo iniciar ANNY
Abre un nuevo chat. Simplemente saluda a ANNY y dile:
*"Hola ANNY, he instalado el código. Por favor, inicia la configuración."*

## 10. Configuración única
ANNY detectará que es un repositorio virgen y activará su protocolo "Genesis".

## 11. Qué preguntas hace
ANNY te pedirá únicamente los datos mínimos de identidad organizacional:
- El nombre de tu organización.
- Confirmación de tu identidad como la Autoridad Ejecutiva (L0).
- Confirmación para ejecutar la inicialización de la estructura estándar.

## 12. Qué crea automáticamente
Al aprobar, ANNY generará instantáneamente:
- **1 Director L0** (Tú).
- **8 Directores L1** (Finanzas, Producto, Ingeniería, etc.).
- **8 Especialistas L2**.
Y persistirá esta estructura (junto con el registro de Genesis) en tu repositorio GitHub de forma segura e inmutable.

## 13. Cómo utilizarlo después
A partir de este momento, simplemente pide lo que necesites en lenguaje natural (ej. *"Necesitamos preparar una estrategia de lanzamiento de nuestro primer producto"*). ANNY identificará al departamento adecuado, asignará la misión, documentará las decisiones y generará la evidencia automáticamente.

## 14. Cómo cerrar ChatGPT
Cuando termines de trabajar, simplemente cierra la pestaña o la ventana del chat. ANNY guarda **todo** el estado, decisiones y evidencias directamente en tu repositorio de GitHub como archivos durables.

## 15. Cómo volver a abrir una conversación
Inicia un nuevo chat en cualquier momento.

## 16. Cómo recuperar estado desde GitHub
Dile a ANNY: *"Hola, continuamos trabajando en la misión de lanzamiento de producto"*. ANNY leerá tu repositorio de GitHub de forma transparente, reconstruirá el estado organizacional exacto y continuará operando sin perder ningún contexto histórico.
