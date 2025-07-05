#include <stdio.h>
#include "driver/i2c.h"
#include "esp_log.h"
#include "uart_com.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "aht10.h"


void app_main() {
    aht10_init(I2C_MASTER_NUM);
    init_uart();
    uart_com_task_init(); // Initialize UART communication task
}
