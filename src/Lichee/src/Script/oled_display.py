import smbus
import os
import sys
import time

# --- Constantes del SSD1306 ---
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
SSD1306_SWITCHCAPVCC = 0x2
SSD1306_EXTERNALVCC = 0x1

class SSD1306Base:
    def __init__(self, width, height, i2c_bus):
        self.width = width
        self.height = height
        self.pages = height // 8
        self.buffer = [0] * (width * self.pages)
        self.i2c = smbus.SMBus(i2c_bus)

    def command(self, c):
        self.i2c.write_byte_data(SSD1306_I2C_ADDRESS, 0x00, c)

    def data(self, c):
        self.i2c.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, c)

    def begin(self, vccstate=SSD1306_SWITCHCAPVCC):
        self.vccstate = vccstate
        self._initialize()
        self.command(SSD1306_DISPLAYON)

    def _initialize(self):
        self.command(SSD1306_DISPLAYOFF)
        self.command(SSD1306_SETDISPLAYCLOCKDIV)
        self.command(0x80)
        self.command(SSD1306_SETMULTIPLEX)
        self.command(self.height - 1)
        self.command(SSD1306_SETDISPLAYOFFSET)
        self.command(0x00)
        self.command(SSD1306_SETSTARTLINE | 0x00)
        self.command(SSD1306_CHARGEPUMP)
        self.command(0x14 if self.vccstate == SSD1306_SWITCHCAPVCC else 0x10)
        self.command(SSD1306_MEMORYMODE)
        self.command(0x00)
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)
        self.command(0x12)
        self.command(SSD1306_SETCONTRAST)
        self.command(0xCF if self.vccstate == SSD1306_SWITCHCAPVCC else 0x9F)
        self.command(SSD1306_SETPRECHARGE)
        self.command(0xF1 if self.vccstate == SSD1306_SWITCHCAPVCC else 0x22)
        self.command(SSD1306_SETVCOMDETECT)
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)
        self.command(SSD1306_NORMALDISPLAY)

    def clear(self):
        self.buffer = [0] * (self.width * self.pages)

    def display(self):
        self.command(SSD1306_COLUMNADDR)
        self.command(0)
        self.command(self.width - 1)
        self.command(SSD1306_PAGEADDR)
        self.command(0)
        self.command(self.pages - 1)
        for i in range(0, len(self.buffer), 16):
            self.i2c.write_i2c_block_data(SSD1306_I2C_ADDRESS, 0x40, self.buffer[i:i+16])

font5x7 = {
    '0': [0x3E,0x51,0x49,0x45,0x3E], '1': [0x00,0x42,0x7F,0x40,0x00],
    '2': [0x62,0x51,0x49,0x49,0x46], '3': [0x22,0x49,0x49,0x49,0x36],
    '4': [0x18,0x14,0x12,0x7F,0x10], '5': [0x2F,0x49,0x49,0x49,0x31],
    '6': [0x3C,0x4A,0x49,0x49,0x30], '7': [0x01,0x71,0x09,0x05,0x03],
    '8': [0x36,0x49,0x49,0x49,0x36], '9': [0x06,0x49,0x49,0x29,0x1E],
    '.': [0x00,0x60,0x60,0x00,0x00], ',': [0x00,0x60,0x60,0x00,0x00],
    'T': [0x01,0x01,0x7F,0x01,0x01], 'H': [0x7F,0x08,0x08,0x08,0x7F],
    'C': [0x3E,0x41,0x41,0x41,0x22], '%': [0x63,0x13,0x08,0x64,0x63],
    ':': [0x00,0x36,0x36,0x00,0x00], ' ': [0x00,0x00,0x00,0x00,0x00],
    '+': [0x08,0x08,0x3E,0x08,0x08], '-': [0x08,0x08,0x08,0x08,0x08],
    '=': [0x14,0x14,0x14,0x14,0x14], 'e': [0x38,0x54,0x54,0x54,0x18],  
    'I': [0x00,0x41,0x7F,0x41,0x00], 'o': [0x38,0x44,0x44,0x44,0x38],
    'S': [0x24,0x4A,0x4A,0x4A,0x30], 'E': [0x7F,0x49,0x49,0x49,0x41],
    'P': [0x7F,0x09,0x09,0x09,0x06], 'L': [0x7F,0x40,0x40,0x40,0x40],
    'R': [0x7F,0x09,0x19,0x29,0x46], 'D': [0x7F,0x41,0x41,0x41,0x3E],
    'k': [0x7F,0x10,0x28,0x44,0x00], 'v': [0x3C,0x40,0x40,0x3C,0x00],
    'M': [0x7F,0x02,0x04,0x02,0x7F], 'U': [0x3F,0x40,0x40,0x40,0x3F],
    'G': [0x3E,0x41,0x49,0x49,0x2E], 'a': [0x20,0x54,0x54,0x54,0x78],
    't': [0x04,0x3F,0x44,0x40,0x20], 'w': [0x7C,0x10,0x08,0x10,0x7C],
    'y': [0x0C,0x50,0x50,0x50,0x3C], 'n': [0x7C,0x08,0x04,0x04,0x78],
    's': [0x48,0x54,0x54,0x54,0x20], 'r': [0x7C,0x08,0x04,0x04,0x08],

}


def render_text(lines, width=128, height=64):
    buffer = [0x00] * (width * (height // 8))
    total_lines = len(lines)
    top_offset = max((height // 8 - total_lines) // 2, 0)  # Centrado vertical

    for i, line_info in enumerate(lines):
        line = line_info["text"]
        invert = line_info.get("invert", False)
        x = (width - len(line) * 6) // 2  # Centrado horizontal
        y = top_offset + i

        for char in line:
            cols = font5x7.get(char, [0x00]*5)
            for col in cols:
                idx = y * width + x
                if 0 <= idx < len(buffer):
                    buffer[idx] = col ^ 0xFF if invert else col
                    x += 1
            x += 1
    return buffer


def main():
    disp = SSD1306Base(128, 64, i2c_bus=0)
    disp.begin()
    last_text = ""
    last_lines = []

    while True:
        if not os.path.exists("/tmp/data.txt"):
            time.sleep(1)
            continue

        try:
            with open("/tmp/data.txt", "r") as f:
                raw = f.read().strip()

            if not raw or ',' not in raw:
                raise ValueError("Dato vacío o malformado")

            temp, hum = raw.split(",")
            temp = temp.strip()
            hum = hum.strip()

            lines = [
                {"text": "IoT Sensor Gateway", "invert": False},
                {"text": "", "invert": False},
                {"text": "", "invert": False},
                {"text": f"TEMP: {temp}C", "invert": False},
                {"text": f"HUM:  {hum}%", "invert": False},
            ]

            text_repr = "\n".join([line["text"] for line in lines])
            if text_repr != last_text:
                disp.clear()
                disp.buffer = render_text(lines)
                disp.display()
                last_text = text_repr
                last_lines = lines

        except:
            # No se actualiza ni borra la pantalla, solo conserva el contenido anterior
            pass

        time.sleep(5)

if __name__ == "__main__":
    main()
