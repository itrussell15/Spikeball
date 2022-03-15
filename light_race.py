import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30)

color = (100,100,100)
num_leds = 30

while True:
    for i in num_leds:
        pixels.fill((0,0,0))
        pixels[i] = color
