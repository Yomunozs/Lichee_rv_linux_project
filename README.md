# 🌐 IoT Sensor Gateway: Lichee RV Dock + ESP32

This project implements an **IoT gateway system** using a **Lichee RV Dock** (RISC-V), which receives environmental data from an **ESP32** over **UART**, stores it temporarily, and displays it on an **OLED SSD1306** via **I2C**.

---

## 🎯 Objective

Design a embedded system to:

- Interface with an **ESP32 sensor node** sending `temperature,humidity` via UART
- Parse and store incoming data locally
- Display real-time values on a 128x64 OLED screen using I2C
- Autostart scripts on boot via `systemd`

---

## 🧩 Devices and Materials

| Component                   | Description                                          |
|-----------------------------|------------------------------------------------------|
| **Lichee RV Dock**          | Embedded RISC-V board, main gateway                  |
| **ESP32 Dev Board**         | Sends data via UART when it receives "getdata"       |
| **AHT10 Sensor**            | Sensor operates on 0x38 and 0x39 address             |
| **OLED Display (SSD1306)**  | 128x64 monochrome, I2C address `0x3C`                |
| **Dupont Wires**            | For I2C and UART connections                         |
| **Laptop (x86_64)**         | For development and cross-compilation                |

---

## 🖼️ System Architecture Diagram
--
    ```
        ┌────────────┐        UART        ┌──────────────────────┐
        │            │ <----------------- │                      │
        │   Lichee   │  "getdata"         │     ESP32 Sensor     │
        │  RV Dock   │ -----------------> │ (TEMP + HUM via UART)|
        │            │                    │                      │
        └─────┬──────┘                    └─────────┬────────────┘
              │                                     │
           I2C│                                  I2C AHT10
              v
       ┌──────────────┐
       │   OLED       │
       │  SSD1306     │
       └──────────────┘
    ---


## 🧰 Requirements

### Hardware

- **Lichee RV Dock**:
  - UART0 (/dev/ttyS0) connected to ESP32 UART (PB8=TX, PB9=RX)
  - I2C0 (/dev/i2c-0) connected to OLED (PB0=SCL, PB1=SDA)
  
- **ESP32 microcontroller**:
  - Programmed to respond with "TEMP,HUM\n" on "getdata" command
  
- **SSD1306 OLED display**, 128x64 I2C

### Software

- **Lichee RV Dock**:
  - OS: Ubuntu 22.10 RISC-V (Kernel 5.17.0)
  - Python 3, python3-smbus
  - Systemd

---

## ⚙️ Configuration Steps

### 1. ESP32 Firmware 

Main features:
- Waits for "getdata" via UART
- Responds with values like: 25.3,60.1

Firmware Location (repository):  
`src/esp32/main/`

Information Location (repository):  
`src/README.md`

### 2. Enable I2C on Lichee RV Dock

Configured and activated through .dtb system file.

---

## 📜 Scripts and Code Summary

### 🔁 uart-poller.sh

Location: `/usr/local/bin/uart-poller.sh`

Purpose:
- Configures UART0
- Sends "getdata" to ESP32 every 5 seconds
- Validates and saves response to /tmp/data.txt

Main Loop:
1. **Clear Previous Data**  
   `cat < $DEVICE > /dev/null & sleep 0.1; kill $!`  
   → Flushes any residual data from the UART buffer

2. **Start Background Reader**  
   `cat < $DEVICE > "$OUTPUT" &`  
   → Begins listening for ESP32 responses in background  
   → Saves output to temporary file (`/tmp/data.txt`)

3. **Send Request Command**  
   `echo -n "getdata" > $DEVICE`  
   → Sends the exact "getdata" string (no line endings) to ESP32

4. **Wait for Response**  
   `sleep 3`  
   → Allows 3 seconds for sensor data transmission

5. **Cleanup**  
   `kill $CAT_PID`  
   → Stops the background reader after data capture

6. **Repeat**  
   `sleep $INTERVAL`  
   → Waits 5 seconds before next poll (adjustable)

## 🖥️ oled_display.py

**Location**: `/usr/local/bin/oled_display.py`  

**Purpose**:
- Initializes SSD1306 display
- Reads `/tmp/data.txt`
- Displays `TEMP:` and `HUM:` with custom 5x7 font
- Update cycle: every 5 seconds

---

## 📂 Systemd Services

### uart-poller.service
**Path**: `/etc/systemd/system/uart-poller.service`  

### oled-display.service  
**Path**: `/etc/systemd/system/oled-display.service`  

**Enable auto-start at boot**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable name*.service
sudo systemctl start name*.service

---

## xx. 📁 Repository Structure

```
LICHEE_RV_LINUX_PROJECT/
├── /docs/
│   └── wiring_diagrams.svg
│   └── Requirements.xlsx
├── /src/
│   └── /Lichee
|       ├──src
|       └──Test
|           ├──Uart_test
|           |  └── uart_poller.sh
|           ├──Oled_test
|           |  ├── oled_display.py
|           |  └── ssd1306-demo.py
|           └──Server_test
|              └── iot_server.py
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

