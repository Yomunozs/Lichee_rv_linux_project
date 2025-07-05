#include "aht10.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include "freertos/task.h"

static const char *TAG = "AHT10";

void aht10_init(i2c_port_t i2c_num) {
    // Configure I2C master
    i2c_config_t i2c_config = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_param_config(I2C_MASTER_NUM, &i2c_config));
    ESP_ERROR_CHECK(i2c_driver_install(I2C_MASTER_NUM, i2c_config.mode, 0, 0, 0));
    uint8_t init_cmd[] = {AHT10_CMD_INIT, 0x08, 0x00};
    esp_err_t ret = i2c_master_write_to_device(i2c_num, AHT10_I2C_ADDR, 
                     init_cmd, sizeof(init_cmd), 1000 / portTICK_PERIOD_MS);
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "AHT10 initialized successfully");
    } else {
        ESP_LOGE(TAG, "Failed to initialize AHT10");
    }
}

void aht10_measure(i2c_port_t i2c_num, float *temperature, float *humidity) {
    uint8_t measure_cmd[] = {AHT10_CMD_MEASURE, 0x33, 0x00};
    uint8_t data[6];

    // Send measurement command
    esp_err_t ret = i2c_master_write_to_device(i2c_num, AHT10_I2C_ADDR, 
                     measure_cmd, sizeof(measure_cmd), 1000 / portTICK_PERIOD_MS);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to send measurement command");
        return;
    }

    vTaskDelay(100 / portTICK_PERIOD_MS);

    // Read measurement data
    ret = i2c_master_read_from_device(i2c_num, AHT10_I2C_ADDR, 
          data, sizeof(data), 1000 / portTICK_PERIOD_MS);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to read data");
        return;
    }

    // Parse temperature and humidity
    uint32_t raw_humidity = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4);
    uint32_t raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5];

    *humidity = ((float)raw_humidity / 1048576.0) * 100.0;
    *temperature = ((float)raw_temperature / 1048576.0) * 200.0 - 50.0;

    ESP_LOGI(TAG, "Temperature: %.2f °C, Humidity: %.2f %%", *temperature, *humidity);
}

void aht10_read(void *pvParameters) {
    float temperature = 0.0, humidity = 0.0;
    float data[2]; // Array to hold temperature and humidity
    
    while (1) {
        aht10_measure(I2C_MASTER_NUM, &temperature, &humidity);
        data[0] = temperature; // Store temperature in the first element
        data[1] = humidity;    // Store humidity in the second element
        // Send data to UART communication task
        
        ESP_LOGI("AHT10", "Temperature: %.2f C, Humidity: %.2f %%", temperature, humidity);
        vTaskDelay(2000 / portTICK_PERIOD_MS); // Delay for 2 seconds
    }
}
