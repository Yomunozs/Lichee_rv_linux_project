#ifndef AHT10_H
#define AHT10_H

#include <stdint.h>
#include "driver/i2c.h"


#define I2C_MASTER_NUM I2C_NUM_0
#define I2C_MASTER_SDA_IO 21
#define I2C_MASTER_SCL_IO 22
#define I2C_MASTER_FREQ_HZ 100000

#define AHT10_I2C_ADDR 0x38
#define AHT10_CMD_INIT 0xE1
#define AHT10_CMD_MEASURE 0xAC



/**
 * @brief Initialize the AHT10 sensor
 * @param i2c_num I2C port number
 */
void aht10_init(i2c_port_t i2c_num);

/**
 * @brief Measure temperature and humidity
 * @param i2c_num I2C port number
 * @param[out] temperature Pointer to store temperature value (°C)
 * @param[out] humidity Pointer to store humidity value (%)
 */
void aht10_measure(i2c_port_t i2c_num, float *temperature, float *humidity);

/**
 * @brief Task to read AHT10 sensor data
 * @param pvParameters Pointer to task parameters (not used)
 */
void aht10_read(void *pvParameters);


#endif // AHT10_H