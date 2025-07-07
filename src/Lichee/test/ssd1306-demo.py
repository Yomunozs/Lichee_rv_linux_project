# SSD1306 OLED Display Demo for Lichee RV Dock
# Original Author: Tony DiCola (Adafruit)
# Modified by: Indrek Kruusa, 2023
# Further modified to show "WELCOME"

import smbus
import os
import sys

# Constants
SSD1306_I2C_ADDRESS = 0x3C
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETSTARTLINE = 0x40
SSD1306_CHARGEPUMP = 0x8D
SSD1306_MEMORYMODE = 0x20
SSD1306_SEGREMAP = 0xA0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETCONTRAST = 0x81
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

class SSD1306Base:
    def __init__(self, width, height, i2c_bus=None):
        self.width = width
        self.height = height
        self._pages = height // 8
        self._buffer = [0] * (width * self._pages)
        self._i2c = smbus.SMBus(i2c_bus)

    def command(self, c):
        self._i2c.write_byte_data(SSD1306_I2C_ADDRESS, 0x00, c)

    def data(self, c):
        self._i2c.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, c)

    def begin(self, vccstate=SSD1306_SWITCHCAPVCC):
        self._vccstate = vccstate
        self._initialize()
        self.command(SSD1306_DISPLAYON)

    def display(self):
        self.command(SSD1306_COLUMNADDR)
        self.command(0)
        self.command(self.width - 1)
        self.command(SSD1306_PAGEADDR)
        self.command(0)
        self.command(self._pages - 1)

        for i in range(0, len(self._buffer), 16):
            self._i2c.write_i2c_block_data(SSD1306_I2C_ADDRESS, 0x40, self._buffer[i:i+16])

    def clear(self):
        self._buffer = [0] * (self.width * self._pages)

    def set_contrast(self, contrast):
        self.command(SSD1306_SETCONTRAST)
        self.command(contrast)

    def say_hi(self):
        # "WELCOME" using 5x7 font + spacing
        welcome = [
            # W
            0x7C, 0x02, 0x1C, 0x02, 0x7C, 0x00,
            # E
            0x7E, 0x4A, 0x4A, 0x4A, 0x42, 0x00,
            # L
            0x7E, 0x40, 0x40, 0x40, 0x40, 0x00,
            # C
            0x3C, 0x42, 0x40, 0x42, 0x3C, 0x00,
            # O
            0x3C, 0x42, 0x42, 0x42, 0x3C, 0x00,
            # M
            0x7E, 0x04, 0x18, 0x04, 0x7E, 0x00,
            # E
            0x7E, 0x4A, 0x4A, 0x4A, 0x42
        ]
        self.clear()
        for i in range(len(welcome)):
            self._buffer[i] = welcome[i]
        self.display()

class SSD1306_128_64(SSD1306Base):
    def __init__(self, i2c_bus=None):
        super().__init__(128, 64, i2c_bus)

    def _initialize(self):
        self.command(SSD1306_DISPLAYOFF)
        self.command(SSD1306_SETDISPLAYCLOCKDIV)
        self.command(0x80)
        self.command(SSD1306_SETMULTIPLEX)
        self.command(0x3F)
        self.command(SSD1306_SETDISPLAYOFFSET)
        self.command(0x00)
        self.command(SSD1306_SETSTARTLINE | 0x00)
        self.command(SSD1306_CHARGEPUMP)
        self.command(0x14)
        self.command(SSD1306_MEMORYMODE)
        self.command(0x00)
        self.command(SSD1306_SEGREMAP | 0x01)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)
        self.command(0x12)
        self.command(SSD1306_SETCONTRAST)
        self.command(0xCF)
        self.command(SSD1306_SETPRECHARGE)
        self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)
        self.command(SSD1306_NORMALDISPLAY)

# Main Execution
i2c_device = 1
if not os.path.exists(f"/dev/i2c-{i2c_device}"):
    print(f"I2C device /dev/i2c-{i2c_device} not found.")
    print("Check your devicetree or enable i2c2 in u-boot.")
    sys.exit(1)

disp = SSD1306_128_64(i2c_bus=i2c_device)
disp.begin()
disp.clear()
disp.display()
disp.say_hi()
