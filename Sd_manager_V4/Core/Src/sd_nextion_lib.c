#include "sd_nextion_lib.h"
#include "main.h"
#include <stdio.h>

/**
 * @brief Guarda datos en un archivo CSV en la tarjeta SD.
 *
 * Esta función abre (o crea si no existe) un archivo llamado "data.csv" en la tarjeta SD,
 * se posiciona al final del archivo y escribe una nueva línea con los datos proporcionados.
 *
 * @param id El identificador que se va a guardar.
 * @param value El valor que se va a guardar.
 * @param timestamp La marca de tiempo asociada a los datos.
 */
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

/**
 * @brief Verifica si un archivo puede ser abierto y escrito.
 *
 * Esta función intenta abrir un archivo en modo de escritura y verifica si el archivo se puede escribir.
 *
 * @param filename nombre del archivo a verificar.
 * @return int Devuelve 1 si el archivo puede ser abierto y escrito correctamente, de lo contrario devuelve 0.
 */
int verificarSd(const char* filename) {
    FIL fil;
    FRESULT res;

    // Intentar abrir el archivo en modo de escritura
    res = f_open(&fil, filename, FA_OPEN_ALWAYS | FA_WRITE);
    if (res != FR_OK) {
        return 0;
    }

    // Verificar si el archivo está abierto y se puede escribir
    if ((fil.flag & FA_WRITE) == 0) {
        f_close(&fil);
        return 0;
    }

    // Cerrar el archivo y devolver 1 (todo ok)
    f_close(&fil);
    return 1;
}

