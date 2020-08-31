import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def main(filename="output.png", img_width=2000, img_height=2000):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    gradient_start_y = random.randint(0, img_height)
    gradient_end_y = random.randint(gradient_start_y, img_height)
    gradient = cairo.LinearGradient(0, gradient_start_y, img_width, gradient_end_y)
    stop = 0
    while stop < 0.98:
        color = (random.random(), random.random(), random.random())
        gradient.add_color_stop_rgb(stop, *color)
        stop = random.uniform(stop, 1)

    ctx.set_source(gradient)
    ctx.fill()

    ims.write_to_png(filename)

# Palette is ignored, here for API consistency.
def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    print(filename)
    main(filename=filename, img_height=img_height, img_width=img_width)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
