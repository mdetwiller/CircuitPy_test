import time
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_bno055

i2c = board.STEMMA_I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
last_accX = sensor.acceleration[0]
last_accY = sensor.acceleration[1]
last_accZ = sensor.acceleration[2]

displayio.release_displays()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
WIDTH = 128
HEIGHT = 64
BORDER = 5
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# display context
splash = displayio.Group()
display.show(splash)

# labels
text = " hey "
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
    )
splash.append(text_area)

rightarrow = " -> "
rightarrow_area = label.Label(
    terminalio.FONT, text=rightarrow, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
    )

leftarrow = " <- "
leftarrow_area = label.Label(
    terminalio.FONT, text=leftarrow, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
    )

uparrow = " ^ "
uparrow_area = label.Label(
    terminalio.FONT, text=uparrow, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
    )

downarrow = " v "
downarrow_area = label.Label(
    terminalio.FONT, text=downarrow, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
    )

while True:
    accX = sensor.acceleration[0]
    accY = sensor.acceleration[1]
    accZ = sensor.acceleration[2]

    if accY < 3 and abs(accX) < 3:
        if last_accY >= 3:
            splash.pop(0)
            splash.append(uparrow_area)
            display.show(splash)

    if accY >= 3 and abs(accX) < 3:
        if last_accY < 3:
            splash.pop(0)
            splash.append(downarrow_area)
            display.show(splash)

    if accX >= 5:
        if last_accX < 5:
            splash.pop(0)
            splash.append(rightarrow_area)
            display.show(splash)

    if accX < -5:
        if last_accX >= -5:
            splash.pop(0)
            splash.append(leftarrow_area)
            display.show(splash)

    last_accX = accX
    last_accY = accY
    last_accZ = accZ

    # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
