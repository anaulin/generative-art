import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors


def petal(ctx, x, y, width, height, color):
    tl = (x, y)
    tr = (x + width, y)
    bl = (x, y + height)
    br = (x + width, y + height)
    if random.random() < 0.5:
        ctx.curve_to(*tl, *tr, *br)
        ctx.move_to(*tl)
        ctx.curve_to(*tl, *bl, *br)
    else:
        ctx.curve_to(*bl, *tl, *tr)
        ctx.move_to(*bl)
        ctx.curve_to(*bl, *br, *tr)

    ctx.set_source_rgb(*palettes.hex_to_tuple(color))
    ctx.fill()

def main(filename="output.png", palette=random.choice(palettes.PALETTES), columns=15, rows=10, img_width=3840, img_height=2160):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for x in range(0, img_width, img_width // columns):
        for y in range(0, img_height, img_height // rows):
            petal(ctx, x, y, img_width // columns, img_height // rows, random.choice(palette['colors']))

    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    c = random.randint(4, 20)
    r = random.randint(int(0.5 * c), int(1.5 * c))
    print(filename, p, c, r)
    main(filename=filename, palette=p, columns=c, rows=r, img_height=img_height, img_width=img_width)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx), p=random.choice(palettes.PALETTES))
