#-------------------------------------------------------------------#
#                                                                   #
#                      Script by FW-K4S   V1.2                      #
#                                                                   #
#      Run this script in Python Virtual Environment (VENV)         #
#                                                                   #
#-------------------------------------------------------------------#

#          -           V1.2 - Wifi Implementation            -


import time
import os
import board
import busio
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306
import adafruit_ahtx0

# -------------------------- I2C --------------------------
i2c = busio.I2C(board.SCL, board.SDA)

# -------------------------- SENSOR --------------------------
sensor = adafruit_ahtx0.AHTx0(i2c)

# -------------------------- DISPLAY --------------------------

WIDTH = 128
HEIGHT = 64

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# Create image buffer
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()


# -------------------------- Text Size + spacing --------------------------

def draw_big_text(text, x, y, scale=2, spacing=1):
    # Temporary image for the normal-size text
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Add extra width for letter spacing
    temp = Image.new(
        "1",
        (text_width + (len(text) - 1) * spacing + 2, text_height + 2),
        0
    )

    temp_draw = ImageDraw.Draw(temp)

    current_x = 1 - bbox[0]

    # Draw each character separately
    for char in text:
        temp_draw.text(
            (current_x, 1 - bbox[1]),
            char,
            font=font,
            fill=255
        )

        char_bbox = font.getbbox(char)
        current_x += char_bbox[2] - char_bbox[0] + spacing

    # Scale it up
    temp = temp.resize(
        (temp.width * scale, temp.height * scale)
    )

    image.paste(temp, (x, y))



# -------------------------- USB CHECK --------------------------

USB_PATH = "/dev/serial/by-id/usb-STMicroelectronics"

def check_ender():
    try:
        for dev in os.listdir("/dev/serial/by-id/"):
            if "STMicroelectronics" in dev:
                return True
    except:
        return False
    return False




# -------------------------- WIFI CHECK --------------------------

def check_wifi():
    try:
        # Get default gateway
        result = os.popen(
            "ip route | awk '/default/ {print $3; exit}'"
        ).read().strip()

        # No default gateway
        if not result:
            return False

        # Ping gateway once, 1 second timeout
        result = os.system(
            f"ping -c 1 -W 1 {result} > /dev/null 2>&1"
        )

        return result == 0

    except:
        return False




# -------------------------- 3D PRINTER ICON --------------------------

def draw_printer(draw, x, y, ready):
    # Outer 3D printer frame
    draw.rectangle((x + 2, y + 2, x + 17, y + 18), outline=255)

    # Top gantry
    draw.line((x + 4, y + 5, x + 15, y + 5), fill=255)

    # Vertical rails
    draw.line((x + 5, y + 3, x + 5, y + 15), fill=255)
    draw.line((x + 14, y + 3, x + 14, y + 15), fill=255)

    # Print head
    draw.rectangle((x + 8, y + 5, x + 11, y + 8), outline=255)

    # Nozzle
    draw.line((x + 9, y + 8, x + 9, y + 10), fill=255)

    # Build plate
    draw.line((x + 5, y + 14, x + 15, y + 14), fill=255)

    # Status symbol
    if ready:
        draw.line((x - 2, y + 3, x + 4, y + 10), fill=255, width=2)
        draw.line((x + 4, y + 10, x + 14, y - 2), fill=255, width=2)

    else:
        draw.line((x - 2, y - 2, x + 12, y + 12), fill=255, width=2)
        draw.line((x + 12, y - 2, x - 2, y + 12), fill=255, width=2)




# -------------------------- WIFI ICON --------------------------

def draw_wifi(draw, x, y, ready):
    # Wi-Fi symbol
    draw.arc(
        (x + 1, y + 2, x + 19, y + 20),
        225, 315,
        fill=255,
        width=2
    )

    draw.arc(
        (x + 5, y + 6, x + 15, y + 16),
        225, 315,
        fill=255,
        width=2
    )

    # Wi-Fi dot
    draw.ellipse(
        (x + 8, y + 13, x + 12, y + 17),
        fill=255
    )

    # X only when not ready
    if not ready:
        draw.line((x - 2, y - 2, x + 12, y + 12), fill=255, width=2)
        draw.line((x + 12, y - 2, x - 2, y + 12), fill=255, width=2)




# -------------------------- WIFI CACHE --------------------------

wifi_ready = False
last_wifi_check = 0
WIFI_CHECK_INTERVAL = 10  # seconds




# -------------------------- LOOP --------------------------

while True:
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    temp = sensor.temperature
    hum = sensor.relative_humidity

    # Text
    draw_big_text(f"{temp:.1f} °C", 2, 5, 2)
    draw_big_text(f"{hum:.1f} %", 2, 34, 2)

    # Check printer every loop
    ready = check_ender()

    # Check Wi-Fi only every 10 seconds
    current_time = time.monotonic()

    if current_time - last_wifi_check >= WIFI_CHECK_INTERVAL:
        wifi_ready = check_wifi()
        last_wifi_check = current_time

    # 3D printer status - top right
    draw_printer(draw, 104, 6, ready)

    # Wi-Fi status - bottom right
    draw_wifi(draw, 104, 34, wifi_ready)

    oled.image(image)
    oled.show()

    time.sleep(1)
