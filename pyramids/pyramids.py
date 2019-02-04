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
IMG_WIDTH = 2000


def pyramid(ctx, x, y, width, height, color, random_center=True):
    if random_center:
        center = ( random.randint(x + 3, x + width - 3), random.randint(y + 3, y + height - 3))
    else:
        center = (x + width // 2, y + height // 2)
    tl = (x, y)
    tr = (x + width, y)
    bl = (x, y + height)
    br = (x + width, y + height)
    cols = colors.shades(color, 5)
    triangle(ctx, tl, tr, center, cols[0])
    triangle(ctx, tr, br, center, cols[1])
    triangle(ctx, br, bl, center, cols[2])
    triangle(ctx, bl, tl, center, cols[3])


def triangle(ctx, p1, p2, p3, color):
    ctx.move_to(*p1)
    for p in [p1, p2, p3]:
        ctx.line_to(*p)
    ctx.set_source_rgb(*color)
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
            color = (random.random(), random.random(), random.random())
            #pyramid(ctx, x, y, IMG_WIDTH // columns, IMG_HEIGHT // rows, palettes.hex_to_tuple(random.choice(palette['colors'])))
            pyramid(ctx, x, y, IMG_WIDTH // columns, IMG_HEIGHT // rows, color)

    ims.write_to_png(filename)


if __name__ == "__main__":
    #for idx, params in enumerate([(10, 9), (7, 5), (17, 14)]):
    #    (c, r) = params
        main(filename="output-random-{}.png".format(1), palette=palettes.PALETTE_8, columns=10, rows=10)
