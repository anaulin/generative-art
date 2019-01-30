import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840


def petal(ctx, x, y, width, height, color):
    tl = (x, y)
    tr = (x + width, y)
    bl = (x, y + height)
    br = (x + width, y + height)
    if random.random() < 0.5:
        ctx.curve_to(*tl, *tr, *br)
        ctx.move_to(*tl)
        ctx.curve_to(*tl, *bl, *br)
        ctx.set_source_rgb(*palettes.hex_to_tuple(color))
    else:
        ctx.curve_to(*bl, *tl, *tr)
        ctx.move_to(*bl)
        ctx.curve_to(*bl, *br, *tr)

    ctx.fill()

def main(filename="output.png", palette=random.choice(palettes.PALETTES), columns=15, rows=10):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for x in range(0, IMG_WIDTH, IMG_WIDTH // columns):
        for y in range(0, IMG_HEIGHT, IMG_HEIGHT // rows):
            petal(ctx, x, y, IMG_WIDTH // columns, IMG_HEIGHT // rows, random.choice(palette['colors']))

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, params in enumerate([(15, 10), (30, 20), (10, 7)]):
        (c, r) = params
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), columns=c, rows=r)
