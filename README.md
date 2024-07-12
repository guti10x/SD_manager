# SD MANAGER: 
#### Proyecto de ejemplo desarrollado en STM32CubeIDE para guardar datos en fromato CSV y TXT en una tarjeta SD

## Esquema de conexiones:
![esquema_conexiones_sd_p1](https://github.com/guti10x/SD_manager/assets/82153822/59fc2bb2-901b-4948-96a2-d676cf8a941c)
![esquema_conexiones_sd_p2](https://github.com/guti10x/SD_manager/assets/82153822/e0d491bb-a936-49f1-b9cb-f4eab4eb6b4b)

## Configuración de FatFs y la placa STM32F103C8T6
#### Consulta la web: https://www.micropeta.com/video29#google_vignette
    
## Importación y uso de la la libreria para guardar datos:
1. Incluir la biblioteca `sd_lib.h`:
    ```c
    #include "sd_lib.h
    ```
2. Habilitar el controlador SPI `hspi1`:
    ```c
    SPI_HandleTypeDef hspi1;
    ```
    *Si utilizas un controlador SPI diferente, asegúrate de modificar el encabezado de la biblioteca `sd_lib.h ` para reflejar el cambio.

4. Configuras dentro del main el sistema de archivos en la tarjeta SD:
    ```c
    if (f_mount(&fs, "", 0) != FR_OK) {
      // Manejar el error de montaje del sistema de archivos
      Error_Handler();
    }
    ```

5. LLamada y uso de la función para guardar datos en la sd:
   ```c
      save_sd(0,"MCU initialized", "timestamp");
   ```
