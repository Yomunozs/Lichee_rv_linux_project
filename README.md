# 📦 IoT Sensor Gateway: ESP32 + Lichee RV Dock

> Second commit – ESP32 firmware complete and tested, also include requirements document for development and check functionality.

---

## 1. 🧾 Existing Driver Documentation Review

### 🔍 AHT10 (ESP32 Side — Temp/Humidity Sensor)

* **ESP-IDF/RTOS Support:**
  AHT10 basic library:

  * [ESPBoards](https://www.espboards.dev/sensors/aht10/)
  

* **I2C Protocol:**
  Sensor operates on 0x38 and 0x39 address, 3.3V logic, supports repeated measurements and status reading.

* **Measurement Ranges:**

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

---

## 3. 🧪 UART Communication Test (Validated)

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

## 4. 🧩 Original Code / Libraries

### Attribution & Licensing:

* [ESPBoards](https://www.espboards.dev/sensors/aht10/)
- aht10 and i2c configuration

* Yonnier Alexander muñoz Salazar
- aht10 code adaptation, uart configuration and firmware struct define

---

## 5. 📁 Suggested Repository Structure

```
LICHEE_RV_LINUX_PROJECT/
├── /docs/
│   └── wiring_diagrams.svg
│   └── Requirements.xlsx
├── /src/
│   └── /esp32/
│       └── drivers
│       ├── main/
│       │   ├── main.c
│       │   ├── aht10.c
│       │   ├── aht10.h
│       │   ├── uart_com.h
│       │   └── uart_com.c
└── README.md (this file)
```
--- 
