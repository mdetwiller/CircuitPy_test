import board
import time
import neopixel
from adafruit_seesaw import seesaw, rotaryio, digitalio
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

i2c = board.STEMMA_I2C()

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

seesaw = seesaw.Seesaw(i2c, addr=0x36)
seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product{}".format(seesaw_product))

if seesaw_product != 4991:
    print("Wrong firmware loaded? Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

# display setup

displayio.release_displays()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
WIDTH = 128
HEIGHT = 64
BORDER = 5
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

animal = ['eagle', 'trout', 'salamander']

# bitmap = displayio.OnDiskBitmap("/images/swirl.bmp")
# tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

while True:

    # negate the position to make the clockwise rotation positive
    position = -encoder.position

    if position != last_position:
        last_position = position
        print("Position: {}".format(position))
        if position >= 0 and position < 3:
            splash = displayio.Group()
            display.show(splash)
            text = animal[position]
            text_area = label.Label(
                terminalio.FONT, text=text, color=0xFFFFFF, x=63, y=HEIGHT // 2 - 1
            )
            splash.append(text_area)

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")
        if position >= 0 and position < 3:
            pixels.fill((255, 255, 255))

    if button.value and button_held:
        button_held = False
        print("Button released")

    if position == 0 and button_held is False:
        pixels.fill((255, 0, 0))

    if position == 1 and button_held is False:
        pixels.fill((0, 255, 0))
        # display.show(trout)

    if position == 2 and button_held is False:
        pixels.fill((0, 0, 255))
        # display.show(salamander)

    if position >= 3 or position < 0:
        pixels.fill((0, 0, 0))
