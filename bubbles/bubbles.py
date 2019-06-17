import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def circle(ctx, x, y, diameter, cols):
    x_fuzz = random.uniform(0, 3) * random.choice([-1, 1])
    y_fuzz = random.uniform(0, 3) * random.choice([-1, 1])
    radius = random.uniform(diameter / 3, diameter / 2) - max(abs(x_fuzz), abs(y_fuzz))
    ctx.arc(x + diameter / 2 + x_fuzz, y + diameter / 2 + y_fuzz, radius, 0, 2 * math.pi)
    ctx.set_source_rgb(*colors.hex_to_tuple(random.choice(cols)))
    ctx.fill()

def main(filename="output.png", img_width=2000, n=10, max_subdiv=5, palette=random.choice(palettes.PALETTES)):
    img_height = img_width   # Work only with square images
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*colors.hex_to_tuple(palette['background']))
    ctx.fill()

    size = img_width // n
    vertical_start = random.randint(0, img_height // 4)
    vertical_end = random.randint(int(img_height * (3/4)), img_height)
    for r in range(vertical_start, vertical_end - size, size):
        row_start = random.randint(0, img_width // 4)
        row_end = random.randint(int(img_width * (3/4)), img_width)
        for c in range(row_start, row_end - size, size):
            subdiv = random.randint(1, max_subdiv)
            step = size // subdiv
            for y in range(subdiv):
                for x in range(subdiv):
                    circle(ctx, c + x * step, r + y * step, step, palette['colors'])

    ims.write_to_png(filename)


def make_random(filename="output.png"):
    n = random.randint(8, 80)
    max_subdiv = random.randint(1, 8)
    p = random.choice(palettes.PALETTES)
    print(filename, os.path.basename(__file__), n, max_subdiv, p)
    main(filename=filename, n=n, max_subdiv=max_subdiv, palette=p)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
