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

def ess(ctx, x, y, width, height, color, line_width):
    tl = (x, y)
    bl = (x, y + height)
    tr = (x + width, y)
    br = (x + width, y + height)
    points = [tl, bl, tr, br]
    random.shuffle(points)
    make_curve(ctx, points, color, line_width)
    # Lighter core
    tints = colors.tints(color, 3)
    make_curve(ctx, points, tints[1], max(line_width // 5, 2))
    make_curve(ctx, points, tints[2], max(line_width // 10, 1))

def make_curve(ctx, points, color, line_width):
    ctx.move_to(*points[0])
    ctx.curve_to(*points[1], *points[2], *points[3])
    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*color)
    ctx.stroke()


def main(filename="output.png", palette=random.choice(palettes.PALETTES), rows=20, columns=20, line_width=20):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    cell_width = IMG_WIDTH // columns
    cell_height = IMG_WIDTH // rows
    for x in range(0, IMG_WIDTH, cell_width):
        for y in range(0, IMG_HEIGHT, cell_height):
            color = palettes.hex_to_tuple(random.choice(palette['colors']))
            ess(ctx, x, y, cell_width, cell_height, color, line_width)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, p in enumerate([(20, 20, 20), (100, 50, 20), (200, 100, 5), (5, 5, 200), (10, 10, 200), (50, 50, 50), (10, 10, 300)]):
        (r, c, lw) = p
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), rows=r, columns=c, line_width=lw)
