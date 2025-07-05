#include "uart_com.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static const char *TAG = "UART_COM";

static detected_pattern_t detected_flag = NONE; // Bandera para el patrón detectado
int min = 0;                                    // Valor mínimo extraído de los datos
int max = 0;                                    // Valor máximo extraído de los datos

// *****************************************************************************************************************

void init_uart(void)
{
    const uart_config_t uart_config = {
        .baud_rate = 115200,                   // Velocidad de transmisión
        .data_bits = UART_DATA_8_BITS,         // Bits de datos
        .parity = UART_PARITY_DISABLE,         // Paridad deshabilitada
        .stop_bits = UART_STOP_BITS_1,         // Bit de parada
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE, // Control de flujo deshabilitado
        .source_clk = UART_SCLK_DEFAULT,       // Reloj por defecto
    };

    // Instalación del driver UART con búfer de recepción y transmisión
    uart_driver_install(UART_NUM, RX_BUF_SIZE * 2, RX_BUF_SIZE * 2, 20, NULL, 0);
    // Configuración de los parámetros del UART
    uart_param_config(UART_NUM, &uart_config);
    // Configuración de los pines TX y RX
    uart_set_pin(UART_NUM, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    // Habilitación de la detección de patrones
    uart_enable_pattern_det_baud_intr(UART_NUM, '#', PATTERN_CHR_NUM, 9, 0, 0);
    // Reinicio de la cola de patrones
    uart_pattern_queue_reset(UART_NUM, 20);
}

// *****************************************************************************************************************

int sendData(const char *logName, const char *data)
{
    const int len = strlen(data);                                // Longitud de los datos
    const int txBytes = uart_write_bytes(UART_NUM_2, data, len); // Escritura de los datos
    return txBytes;                                              // Retorna el número de bytes enviados
}

// *****************************************************************************************************************


// *****************************************************************************************************************

detected_pattern_t check_pattern(const char *data)
{
   
    if (strstr(data, PATTERN_1))
    {
        char str [50]; // Búfer para almacenar la cadena de temperatura
        float temperature, humidity; // Variables para almacenar temperatura y humedad
        aht10_measure(I2C_MASTER_NUM, &temperature, &humidity);
        sprintf(str, "%.2f,%.2f ", temperature, humidity); // Formatea los datos de temperatura y humedad
        // ESP_LOGI(TAG, "Datos AHT10: %s", str); // Log de los datos de AHT10
        sendData("UART", str);

        return PAT1; // Verifica el patrón 1
    }
    if (strstr(data, PATTERN_2)){}
        return PAT2; // Verifica el patrón 2
    return NONE; // Retorna NONE si no se detecta ningún patrón
}


// *****************************************************************************************************************

detected_pattern_t rx_task(void)
{
    static const char *RX_TASK_TAG = "RX_TASK";
    static char pattern;
    uint8_t *data = (uint8_t *)malloc(RX_BUF_SIZE + 1); // Asigna memoria para los datos recibidos

    const int rxBytes = uart_read_bytes(UART_NUM, data, RX_BUF_SIZE, 1000 / portTICK_PERIOD_MS); // Lee los datos del UART
    if (rxBytes > 0)
    {
        data[rxBytes] = 0;                     // Asegura que la cadena esté terminada en null
        pattern = check_pattern((char *)data); // Verifica el patrón en los datos recibidos
        vTaskDelay(100 / portTICK_PERIOD_MS);  // Espera 1 segundo
    }

    free(data);     // Libera la memoria asignada
    return pattern; // Retorna el patrón detectado
}

// *****************************************************************************************************************

// *****************************************************************************************************************


void command_task(void *pvParameters)
{
    while (1)
    {
        detected_pattern_t detected_flag = rx_task(); // Detecta el patrón en los datos recibidos

        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void uart_com_task_init(void)
{
    xTaskCreatePinnedToCore(&command_task, "uart_com_task", 4096, NULL, 5, NULL, 1);
}
