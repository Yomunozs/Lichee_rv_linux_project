# 📦 IoT Sensor Gateway: ESP32 + Lichee RV Dock

> Initial commit documentation for integrating SSD1306 and AHT10 via Lichee RV Dock and ESP32.

---

## 1. 🧾 Existing Driver Documentation Review

### 🔍 SSD1306 (Lichee Side — I2C Display)

* **Oled Driver:**
  From the [Adafruit CircuitPython SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306) library, which is actively maintained and works with Linux.

* **Deprecated Alternative:**
  [Adafruit\_Python\_SSD1306](https://github.com/adafruit/Adafruit_Python_SSD1306) is no longer maintained and is not recommended for new projects, but just in case.


### 🔍 AHT10 (ESP32 Side — Temp/Humidity Sensor)

* **ESP-IDF/RTOS Support:**
  AHT10 is not included in the official ESP-IDF drivers, but userland drivers exist:

  * [UncleRus/esp-idf-lib](https://github.com/UncleRus/esp-idf-lib/tree/master/components/aht)
  * [lbernstone/esp32-aht10](https://github.com/lbernstone/esp32-aht10)

* **I2C Protocol:**
  Sensor operates on 0x38 address, 3.3V logic, supports repeated measurements and status reading.

---

## 2. 🔧 Testing process

### ✅ SSD1306 (Lichee RV Dock — Ubuntu)

Via 📡 UART Communication (to Lichee from Ubuntu PC)


#### 📜 OLED I2C Driver Test (Python)

```bash
sudo apt install python3-pip i2c-tools python3-smbus
pip3 install adafruit-circuitpython-ssd1306
```

##### Example Test Script:

```python
import board, busio, adafruit_ssd1306
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)
display.text("SSD1306 Ready", 0, 0, 1)
display.show()
```

### ✅ AHT10 (ESP32 — ESP-IDF with VS Code)

#### ⚙️ ESP-IDF Configuration

Take required files from repository and configure it code via project enviroment

#### 🧪 Example Test Case

```c
#include "aht.h"

void app_main() {
    aht_init(I2C_NUM_0, GPIO_NUM_X, GPIO_NUM_X);
    while (1) {
        float temp, hum;
        aht_read_data(&temp, &hum);
        printf("Temp: %.2f°C, Hum: %.2f%%\n", temp, hum);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
```

---

## 3. 🧩 Original Code / Libraries

### Attribution & Licensing:

* [Adafruit CircuitPython SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306) – MIT License
* [UncleRus esp-idf-lib](https://github.com/UncleRus/esp-idf-lib) – Apache 2.0 License
* Original code by this project’s authors — Licensed under MIT (see `LICENSE` file)

---

## 4. 📁 Suggested Repository Structure

```
iot-gateway-project/
├── /docs/
│   └── README.md (this file)
│   └── wiring_diagrams.svg
├── /src/
│   ├── /drivers/
│   │   ├── ssd1306_display.py
│   │   └── uart_bridge.py
│   └── /esp32/
│       ├── main/
│       │   ├── main.c
│       │   └── aht_test.c
├── /components/
│   └── aht10/  (ESP-IDF reusable driver)
├── /tests/
│   ├── test_ssd1306.py
│   └── test_uart_rx.py
├── /images/
│   └── architecture_diagram.png
└── LICENSE
```

---