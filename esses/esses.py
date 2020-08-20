import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors

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


def main(filename="output.png", img_width=2000, img_height=2000, palette=random.choice(palettes.PALETTES), rows=20, columns=20, line_width=20):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    cell_width = img_width // columns
    cell_height = img_width // rows
    for x in range(0, img_width, cell_width):
        for y in range(0, img_height, cell_height):
            color = palettes.hex_to_tuple(random.choice(palette['colors']))
            ess(ctx, x, y, cell_width, cell_height, color, line_width)

    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=2000, img_height=2000):
    r = random.randint(5, 80)
    c = random.randint(5, 80) if random.random() < 0.5 else r
    lw = random.randint(5, 25)
    print(filename, r, c, lw, p, img_width, img_height)
    main(filename=filename, palette=p, rows=r, columns=c, line_width=lw, img_height=img_height, img_width=img_width)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
