# 📦 IoT Sensor Gateway: ESP32 + Lichee RV Dock

> Third commit – Lichee rv dock i2c configured and tested oled screen (ssd1306).

---

## 1. 🧾 Existing Documentation Review

### 🔍 AHT10 (ESP32 Side — Temp/Humidity Sensor)

* **ESP-IDF/RTOS Support:**
  AHT10 basic library:

  * [ESPBoards](https://www.espboards.dev/sensors/aht10/)
  * [i2c_and_oled] (https://github.com/ikruusa/)
  

* **I2C Protocol:**
  - Sensor operates on 0x38 and 0x39 address, 3.3V logic, supports repeated measurements and    status reading.
  - Ssd1306 oled operates on 0x3C, 3,3V.

* **Measurement Ranges from aht10:**

  Temperature: -40°C to 85°C, ±0.3°C accuracy
  Humidity: 0% to 100% RH, ±2% typical accuracy

---

## 2. 🔧 ESP32 Firmware Overview

The firmware running on the ESP32 is developed using **ESP-IDF** within **VS Code**. It enables the board to:

* Initialize and read data from the **AHT10** temperature and humidity sensor using the I2C interface.
* Configure and open a **UART interface** to receive specific commands.
* Detect an incoming pattern over UART — currently, the keyword **"getdata"** — and respond with the latest sensor measurements formatted as a string.

### 🔧 Main Functional Components

* **`aht10_init()`**: Initializes the I2C bus and sends the configuration sequence to prepare the AHT10 sensor.
* **`aht10_measure()`**: Executes a measurement request to the sensor and reads the resulting temperature and humidity values.
* **`init_uart()`**: Sets up UART communication parameters including baud rate, data bits, and buffer size.
* **`rx_task()`**: A UART reception task that continuously listens for input, checking if a known pattern (like "getdata") is received.
* **`check_pattern()`**: Parses incoming data to detect pre-defined patterns and triggers appropriate responses (e.g., measuring and sending sensor data).
* **`sendData()`**: Sends the formatted string containing temperature and humidity via UART.
* **`command_task()`**: A FreeRTOS task that continuously manages incoming commands using the detection routine.

This architecture enables the ESP32 to operate autonomously and interactively, serving sensor data on-demand through UART when it receives the expected command pattern.

## 2.1. 🧪 UART Communication Test (Validated)

The UART interface and pattern detection logic have been tested and validated.

### ✅ Test Scenario

* **Command Sent:** `getdata`
* **Expected Response Format:** `temperature,humidity`

  * **Example Output:** `23.34,67.58`

### 🔄 Test Steps

1. Connect to the ESP32 via UART (e.g., using `minicom`, `screen`, or `idf.py monitor`) at **115200 baud**.
2. Send the string `getdata` followed by Enter.
3. Observe the UART output response from the ESP32.

### 🧪 Validation Criteria

* The response is received within \~1 second.
* The format follows `XX.XX,YY.YY`.
* Output values are within:

  * **Temperature:** -40°C to 85°C
  * **Humidity:** 0% to 100% RH

This confirms the correct operation of UART communication and sensor readout.

---
## 3. 📊 SSD1306 OLED Display Setup (Lichee RV Dock)

### 🔺 Hardware Wiring

* **SCL (Clock):** Connect to **PB0**
* **SDA (Data):** Connect to **PB1**
* The I2C2 interface is enabled via Device Tree on the Lichee RV Dock, mapped to `/dev/i2c-1`.

### ⚖️ I2C Detection

Once the device tree update is active:

```bash
sudo i2cdetect -y 1
```

The terminal displays an array that shows an entry at `0x3c`, indicating a detected SSD1306 display

### 📑 Script Functionality (welcome display)

* Initializes and configures the SSD1306 via low-level commands
* Writes the "WELCOME" message directly to the OLED display buffer
* Performs display control (clear, contrast, on/off)

### 💡 Required Libraries

* Python 3 

### ✨ Expected Output

Run with:

```bash
python3 ssd1306-demo.py
```

* Upon execution, the OLED displays **WELCOME** in the upper-left area of the screen.
* Script safely exits if `/dev/i2c-1` is not present, giving suggestions to enable I2C2.

---

## x. 🧩 Original Code / Libraries

### © Code Attribution

* [ESPBoards](https://www.espboards.dev/sensors/aht10/)
- aht10 and i2c configuration

* ssd1306-demo.py: **Indrek Kruusa (2023)** 
- https://github.com/ikruusa/lichee-rv-dock-demos/blob/main/i2c/oled/ssd1306-demo.py

* Adapted and integrated in this project by **Yonnier Muñoz (2025)** for the Lichee RV Dock setup.

---

## xx. 📁 Suggested Repository Structure

```
LICHEE_RV_LINUX_PROJECT/
├── /docs/
│   └── wiring_diagrams.svg
│   └── Requirements.xlsx
├── /src/
│   └── /Lichee
|       ├──test
|          └── ssd1306-demo.py
│   └── /esp32/
│       └── main/
│           ├── main.c
│           ├── aht10.c
│           ├── aht10.h
│           ├── uart_com.h
│           └── uart_com.c
└── README.md (this file)
```
---