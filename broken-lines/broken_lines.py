import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors

# Final image dimensions
IMG_HEIGHT = 2000
IMG_WIDTH = int(IMG_HEIGHT * (16/9))

def line(ctx, y, line_height, color, x_increment, fill_factor, brokenness_factor):
    x = 0
    ctx.move_to(x, y)
    while x < IMG_WIDTH:
        x += random.randint(x_increment // 2, x_increment)
        if random.random() < brokenness_factor:
            ctx.line_to(x, y)
            ctx.set_source_rgb(*color)
            ctx.set_line_width(int(line_height * fill_factor))
            ctx.stroke()
        ctx.move_to(x, y)


def main(filename="output.png", palette=random.choice(palettes.PALETTES), lines=20, fill_factor=1, brokenness_factor=0.3):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    line_height = IMG_HEIGHT // lines
    x_increment = IMG_WIDTH // 40
    for y in range(line_height // 2, IMG_HEIGHT, line_height):
        color = palettes.hex_to_tuple(random.choice(palette['colors']))
        line(ctx, y, line_height, color, x_increment, fill_factor, brokenness_factor)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, l in enumerate([5, 20, 50, 100, 200, 400, 500, 600, 1000]):
        fill_factor = random.uniform(0.5, 1)
        brokenness_factor = random.uniform(0.2, 0.8)
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), lines=l, fill_factor=fill_factor, brokenness_factor=brokenness_factor)
