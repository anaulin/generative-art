import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors

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

def main(filename="output.png", img_width=2000, img_height=2000, palette=random.choice(palettes.PALETTES), columns=15, rows=10):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for x in range(0, img_width, img_width // columns):
        for y in range(0, img_height, img_height // rows):
            pyramid(ctx, x, y, img_width // columns, img_height // rows, palettes.hex_to_tuple(random.choice(palette['colors'])))

    ims.write_to_png(filename)


def make_random(filename="output.png"):
    p = random.choice(palettes.PALETTES)
    c = random.randint(5, 20)
    r = random.randint(5, 20) if random.random() < 0.5 else c
    main(filename=filename.format(1), palette=p, columns=c, rows=r)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
