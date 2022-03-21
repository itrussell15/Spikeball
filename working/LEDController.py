import board
import neopixel
import math, random

class LEDController:

    def __init__(self, num_leds):
        import board

        self.NUM_LEDS = num_leds
        self._control = neopixel.NeoPixel(board.D18, num_leds)

        self._control.fill((0, 0, 0))
        self._control.show()

        self._pos = 0
        self._index = 0
        self._flag = 0

    def AttachAnimations(self, animations):
        self._animations = animations
        random.shuffle(self._animations )

    def changeAnimations(self):
        if self._index <= len(self._animations) - 1:
            self._index +=1
        else:
            self._index = 0
        self._control.fill((0, 0, 0))

    def RunAnimation(self):
        self._animations[self._index](self._pos)
        if self._pos <= 255:
            self._pos += 1
        else:
            self._pos = 0
        self._control.show()

    def _wheel(self, pos):
        ORDER = neopixel.GRB
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(self, pos):
        # for j in range(255):
        print("Rainbow Cycle")
        for i in range(self.NUM_LEDS):
            pixel_index = (i * 256 // self.NUM_LEDS) + pos
            self._control[i] = self._wheel(pixel_index & 255)
        self._control.show()

    # TODO Fix alternating when running
    def loading_bar(self, pos):
        print("Loading Bar")
        mapped_pos = self._mapValue(pos)
        if mapped_pos < self.NUM_LEDS:
            if self._flag == 0:
                self._control[mapped_pos] = (255, 255, 255)
            else:
                self._control[self.NUM_LEDS - mapped_pos] = (255,255,255)
        else:
            self._flag = 0 if self._flag == 1 else 0

    def single_looping(self, pos):
        print("Single Looping")
        self._control.fill((0, 0, 0))
        mapped_pos = self._mapValue(pos)
        self._control[mapped_pos] = ((200, 200, 200))

    def fillRed(self, pos):
        print("Fill Red")
        self._control.fill((255, 0, 0))

    def fillWhite(self, pos):
        print("Fill White")
        self._control.fill((255, 255, 255))

    def fillBlue(self, pos):
        print("Fill Blue")
        self._control.fill((0, 0, 255))

    def fillGreen(self, pos):
        print("Fill Green")
        self._control.fill((0, 255, 0))

    def breathingWhite(self, pos):
        print("Fill White")
        self._control.fill((i, i, i))

    # Returns a mapped value from 255 to the number of leds in the strip
    def _mapValue(self, value):
        scaled = float(value) / float(255.0)
        return math.floor(scaled * (self.NUM_LEDS - 1))
