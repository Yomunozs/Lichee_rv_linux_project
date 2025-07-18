#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

DATA_FILE = "/tmp/data.txt"
HOST_NAME = "0.0.0.0"
PORT = 1234

# Store last known valid values
last_temp = "N/A"
last_hum = "N/A"

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global last_temp, last_hum

        temp, hum = last_temp, last_hum  # Default to last known values

        # Try reading fresh values
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    line = f.read().strip()
                    if line and "," in line:
                        parts = line.split(",")
                        if len(parts) == 2:
                            temp = "{:.2f}".format(float(parts[0]))
                            hum = "{:.2f}".format(float(parts[1]))
                            last_temp, last_hum = temp, hum  # Update cache
        except Exception:
            pass  # Keep previous values silently

        # Generate HTML
        message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Sensor Data</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body {{ font-family: sans-serif; text-align: center; padding-top: 30px; }}
                h2 {{ color: #333; }}
                p {{ font-size: 1.5em; }}
            </style>
        </head>
        <body>
            <h2>🌡️ IoT Sensor Gateway</h2>
            <p><strong>Temperature:</strong> {temp} °C</p>
            <p><strong>Humidity:</strong> {hum} %</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT), MyHandler)
    httpd.serve_forever()
