#ifndef UART_COM_H  
#define UART_COM_H

#include <stdio.h>
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "driver/uart.h"
#include "string.h"
#include "driver/gpio.h"
#include "aht10.h"


static const int RX_BUF_SIZE = 1024;
#define RD_BUF_SIZE (BUF_SIZE)

// Configuracion del UART
#define TXD_PIN (GPIO_NUM_17)
#define RXD_PIN (GPIO_NUM_16)
#define UART_NUM UART_NUM_2

// Comandos para el UART
#define PATTERN_CHR_NUM    (3)         /*!< Número de caracteres consecutivos e idénticos recibidos que definen un patrón UART*/

// Pattern detection
#define PATTERN_MAX_LEN 10  // Longitud máxima de cualquier patrón
#define RD_BUF_SIZE 1024

// Definición de 5 patrones
#define PATTERN_1 "getdata"
#define PATTERN_2 "# Data Off"


// Enumeración de patrones detectados
typedef enum {
    PAT1,  // Patrón 1 detectado
    PAT2,  // Patrón 2 detectado
    NONE,  // Ningún patrón detectado
} detected_pattern_t;

// *****************************************************************************************************************

/**
 * @brief Inicializa la configuración del UART.
 */
void init_uart(void);

// *****************************************************************************************************************

/**
 * @brief Tarea de recepción de datos por UART.
 * @return El patrón detectado en los datos recibidos.
 */
detected_pattern_t rx_task(void);

// *****************************************************************************************************************

/**
 * @brief Envía datos a través del UART.
 * @param logName Nombre del log para identificar la operación.
 * @param data Datos a enviar.
 * @return Número de bytes enviados.
 */
int sendData(const char* logName, const char* data);

// *****************************************************************************************************************
// *****************************************************************************************************************

/**
 * @brief Verifica si los datos recibidos coinciden con algún patrón.
 * @param data Datos recibidos.
 * @return El patrón detectado.
 */
detected_pattern_t check_pattern(const char *data);

// *****************************************************************************************************************
// *****************************************************************************************************************

/**
 * @brief Procesa el comando según el patrón detectado.
 * @param command Patrón detectado a procesar.
 */
void command_process(detected_pattern_t command);

/**
 * @brief Inicializa la tarea de comunicación UART.
 * This function sets up the UART communication task, which includes configuring the UART parameters,
 */
void uart_com_task_init(void);
#endif