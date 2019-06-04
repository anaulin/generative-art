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
    triangle(
        ctx,
        (x - size / 2, y),
        (x, y + size),
        (x + size/2, y),
        cols)

def tile_B(ctx, x, y, size, cols):
    triangle(
        ctx,
        (x, y),
        (x + size, y),
        (x + size / 2 , y + size),
        cols)
    triangle(
        ctx,
        (x, y),
        (x - size / 2, y + size),
        (x + size/2, y + size),
        cols)

def triangle(ctx, p1, p2, p3, cols):
    chosen_cols = [colors.hex_to_tuple(c) for c in random.sample(cols, 2)]
    draw_triangle(ctx, p1, p2, p3, chosen_cols[0])

    # Inner triangle
    points = [p1, p2, p3]
    inner_points = [point_on_line(p, points[idx-1]) for (idx, p) in enumerate(points)]
    draw_triangle(ctx, *inner_points, chosen_cols[1], outline=False)

def draw_triangle(ctx, p1, p2, p3, color, outline=False):
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.line_to(*p3)
    ctx.set_source_rgb(*color)
    ctx.fill()

def point_on_line(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    slope = (y2 - y1)/(x2 - x1)
    x3 = random.uniform(x1, x2)
    y3 = slope * (x3 - x1) + y1
    return (x3, y3)

def main(filename="output.png", img_width=2000, n=10, palette=random.choice(palettes.PALETTES)):
    img_height = img_width   # Work only with square images
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*colors.hex_to_tuple(palette['background']))
    ctx.fill()

    size = (img_width) / n
    for r in range(n):
        for c in range(n + 1):
            tile_fn = tile_A if r % 2 == 0 else tile_B
            tile_fn(ctx, c * size, r * size, size, palette['colors'])
    ims.write_to_png(filename)


def make_random(filename="output.png"):
    n = random.randint(6, 42)
    p = random.choice(palettes.PALETTES)
    print(filename, n, p)
    main(filename=filename, n=n, palette=p)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
