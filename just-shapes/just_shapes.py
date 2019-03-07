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

SPACING = 2

def shape(ctx, color, min_size=IMG_HEIGHT//20, max_size=IMG_HEIGHT//10):
    r = random.random()
    if r < 0.3:
        square(ctx, color, min_size=min_size, max_size=max_size)
    elif r < 0.6:
        circle(ctx, color, min_r=min_size, max_r=max_size)
    else:
        line(ctx, color, random.randint(min_size//10, min_size//2))

def square(ctx, color, min_size, max_size):
    size = random.randint(min_size, max_size)
    x = random.randint(0, IMG_WIDTH - size)
    y = random.randint(0, IMG_HEIGHT - size)
    ctx.rectangle(x, y, size, size)
    alpha = random.uniform(0.2, 0.8)
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()

def circle(ctx, color, min_r, max_r):
    r = random.randint(min_r, max_r)
    x = random.randint(r, IMG_WIDTH -r)
    y = random.randint(r, IMG_HEIGHT -r)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    alpha = random.uniform(0.2, 0.8)
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()

def line(ctx, color, line_width):
    x1 = random.randint(0, IMG_WIDTH)
    y1 = random.randint(0, IMG_HEIGHT)
    x2 = random.randint(0, IMG_WIDTH)
    y2 = random.randint(0, IMG_HEIGHT)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    # Make lines more transparent, they tend to overtake things because they're long.
    alpha = random.uniform(0.09, 0.4)
    ctx.set_source_rgba(*color, alpha)
    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()


def main(filename="output.png", palette=random.choice(palettes.PALETTES), shape_count=100):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for _ in range(shape_count):
        color = palettes.hex_to_tuple(random.choice(palette['colors']))
        shape(ctx, color)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, c in enumerate([50, 100, 200, 400, 500]):
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), shape_count=c)
