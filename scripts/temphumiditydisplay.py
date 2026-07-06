#-------------------------------------------------------------------#
#                                                                   #
#                           Script by FW-K4S                        #
#                                                                   #
#      Run this script in Python Virtual Environment (VENV)         #
#                                                                   #
#-------------------------------------------------------------------#



# -------- Modules --------
import time
import os
import board
import busio
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306
import adafruit_ahtx0


# -------- I2C --------
i2c = busio.I2C(board.SCL, board.SDA)


# -------- SENSOR --------
sensor = adafruit_ahtx0.AHTx0(i2c)


# -------- DISPLAY --------
WIDTH = 128
HEIGHT = 64

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# Create image buffer
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

# --------------------- USB CHECK ---------------------

USB_PATH = "/dev/serial/by-id/usb-DEVICE" #Change "DEVICE" To the port name displaying the serial connection with the printer

def check_ender():
    try:
        for dev in os.listdir("/dev/serial/by-id/"):
            if "STMicroelectronics" in dev:
                return True
    except:
        return False
    return False



# ----------------------- Loop -----------------------

while True:
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    temp = sensor.temperature
    hum = sensor.relative_humidity

    # Temp&Humidity Text
    draw.text((0, 0), f"Temp: {temp:.1f} C", font=font, fill=255)
    draw.text((0, 16), f"Hum : {hum:.1f} %", font=font, fill=255)

    # Printer Status
    if check_ender():
        status = "E3 READY"
    else:
        status = "[X] NOT DETECTED [X]"

    draw.text((0, 40), status, font=font, fill=255)

    oled.image(image)
    oled.show()

    time.sleep(1) #Changed from 0.5 to 1
