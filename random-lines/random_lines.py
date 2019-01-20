from shapely.geometry import Point, LineString
from shapely.ops import unary_union

import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840


def cell(ctx, x, y, width, height, palette, min_width=1, max_width=random.randint(8, 15), line_count=100):
    for _ in range(line_count):
        if random.random() <= 0.5:
            # Left to right
            start_x = x
            start_y = random.randint(y, y + height)
            end_x = x + width
            end_y = random.randint(y, y + height)
        else:
            # Top to bottom
            start_x = random.randint(x, x + width)
            start_y = y
            end_x = random.randint(x, x + width)
            end_y = y + height
        ctx.move_to(start_x, start_y)
        ctx.line_to(end_x, end_y)
        ctx.set_source_rgb(
            *palettes.hex_to_tuple(random.choice(palette['colors'])))
        ctx.set_line_width(random.randint(min_width, max_width))
        ctx.stroke()


def main(filename="output.png", palettes=palettes.PALETTES, rows=15, columns=19):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Black background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(0, 0, 0)
    ctx.fill()

    cell_width = IMG_WIDTH // columns
    cell_height = IMG_HEIGHT // rows
    for y in range(0, IMG_HEIGHT, cell_height):
        for x in range(0, IMG_WIDTH, cell_width):
            cell(ctx, x, y, cell_width, cell_height, random.choice(palettes))

    ims.write_to_png(filename)


if __name__ == "__main__":
    main(filename="output.png", palettes=[palettes.DTG_PALETTE_REDS], rows=1, columns=1)
