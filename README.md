# SD Manager

Este repositorio ofrece las herramientas para la recopilación y análisis de las mediciones de los difenrentes sensores del coche de Formula Student en formato CSV, incluyendo:

- **Librería `sd_nextion_lib`**: permite el almacenamiento de datos en tarjetas microSD y la verificación de su integridad.
- **Proyecto de Ejemplo (`Sd_manager_V4`)**: Muestra cómo utilizar la librería para guardar datos en formato CSV y TXT en una tarjeta SD.
- **Aplicación `CSV_data_plotter`**: Permite analizar y visualizar los datos almacenados, generando gráficos detallados, informes en PDF personalizados, exportando a Excel y, opcionalmente, subiendo los datos a la nube.

## Esquema del proyecto

![FUEdddM_cawr](https://github.com/user-attachments/assets/caed8593-ae45-4999-9ca5-03207b536eb0)


## Desarrolo del contenido del Repositorio

### `sd_nextion_lib`
Esta librería facilita el almacenamiento de datos en formato CSV en tarjetas microSD y proporciona una función para verificar la integridad del almacenamiento en la memoria externa. Está diseñada para su uso en la placa Nexus (STM32F103R8T6) del monoplaza, permitiendo recopilar en un único archivo CSV todos los valores medidos por los distintos sensores del coche. El objetivo es almacenar estos datos para su posterior análisis detallado utilizando la herramienta `CSV_data_plotter`, que permite realizar estudios estadísticos y generar gráficas detalladas de los datos recopilados.


- **Instalación:**
  Consulta el manual de instalación y configuración de la biblioteca en STM32CubeIDE en el [Manual de Instalación de nextion_comunication_lib](sd_nextion_lib/doc/Manual_de_instalación_y_configuración_sd_nextion_lib.pdf).

- **Documentación:**
  Para obtener más información sobre cómo utilizar la librería y sus características, revisa la [Documentación de nextion_comunication_lib](./sd_nextion_lib/doc/Documentación%20sd_nextion_lib.pdf).

### `Sd_manager_V4`
Proyecto de ejemplo desarrollado en STM32CubeIDE que implementa la librería `sd_nextion_lib`. En el se muestra cómo utlizar las funciones para guardar datos en formato CSV y TXT en una tarjeta SD, asi como el uso de una función que garantiza el correcto almacenamiento de los datos en la memoria micorSd.

### `CSV_data_plotter`
Aplicación diseñada para analizar los datos almacenados en la tarjeta microSD provenientes de diversos sensores del coche. Esta herramienta facilita la realización de estudios estadísticos detallados sobre los datos recopilados. Ofrece funcionalidades para:

- **Generar Gráficas Detalladas**: Visualiza los datos en gráficos para una mejor comprensión.
- **Crear PDFs Personalizados**: Exporta informes en PDF con gráficos y datos personalizados.
- **Generar Archivos Excel**: Exporta los datos a formatos Excel para un análisis adicional.
- **Subir Datos a la Nube**: (Opcional) Permite la carga de datos a plataformas en la nube para un acceso y análisis más amplio.

![Captura de pantalla 2024-07-19 101ddd511](https://github.com/user-attachments/assets/acea53e0-7292-4773-b677-39b1eff41f2e)

