#include "sd_lib.h"
#include "main.h"
#include <stdio.h>


void save_sd(int id, const char* value, const char* timestamp) {
    FIL fil;  // Variable para guardar fivhero
    char buffer[256]; // Variable para guardar fila a insertar

    // Abrir el archivo
    if (f_open(&fil, "data.csv", FA_OPEN_ALWAYS | FA_WRITE) != FR_OK) {
        // Manejar el error de apertura o creación del archivo
        Error_Handler();

        return;
    }

    // Posicionarse al final del archivo para añadir datos
    if (f_lseek(&fil, f_size(&fil)) != FR_OK) {
        // Manejar error
        f_close(&fil) ;
        Error_Handler();
        return;
    }

    // Escribir el id, value y timestamp
    snprintf(buffer, sizeof(buffer), "%d, %s, %s\n", id, value, timestamp);
    if (f_puts(buffer, &fil) == EOF) {
        // Manejar error escritura
        f_close(&fil);
        Error_Handler();
        return;
    }

    // Cerrar el archivo
    f_close(&fil);
}
