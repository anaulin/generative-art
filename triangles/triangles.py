import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def tile_A(ctx, x, y, size, cols):
    triangle(
        ctx,
        (x + size / 2, y),
        (x, y + size),
        (x + size, y + size),
        cols)

def tile_B(ctx, x, y, size, cols):
    triangle(
        ctx,
        (x, y),
        (x + size, y),
        (x + size/2, y + size),
        cols)

def triangle(ctx, p1, p2, p3, cols):
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.line_to(*p3)
    ctx.set_source_rgb(*colors.hex_to_tuple(random.choice(cols)))
    ctx.fill()

def main(filename="output.png", img_width=2000, n=10, palette=random.choice(palettes.PALETTES)):
    img_height = img_width   # Work only with square images
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*colors.hex_to_tuple(palette['background']))
    ctx.fill()

    frame = img_width / 10  # empty space around image border
    size = (img_width - 2*frame) / n
    for r in range(n):
        for c in range(n):
            if r % 2 == 0:
                tile_fn = tile_A if c % 2 == 0 else tile_B
            else:
                tile_fn = tile_B if c % 2 == 0 else tile_A
            tile_fn(ctx, frame + c * size, frame + r * size, size, palette['colors'])
    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES)):
    n = random.randint(4, 24)
    print(filename, n, p)
    main(filename=filename, n=n, palette=p)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
