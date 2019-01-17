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

def cell(ctx, x, y, width, height, palette):
    remaining_height = height
    current_y = y
    while remaining_height > 0:
        line_height = random.randint(0, remaining_height)
        ctx.rectangle(x, current_y, width, line_height)
        ctx.set_source_rgb(*palettes.hex_to_tuple(random.choice(palette['colors'])))
        ctx.fill()
        remaining_height -= line_height
        current_y += line_height


def main(filename="output.png", palettes=palettes.PALETTES, rows=15, columns=19):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    cell_width = IMG_WIDTH // columns
    cell_height = IMG_HEIGHT // rows
    for y in range(0, IMG_HEIGHT, cell_height):
        for x in range(0, IMG_WIDTH, cell_width):
            cell(ctx, x, y, cell_width, cell_height, random.choice(palettes))

    ims.write_to_png(filename)


if __name__ == "__main__":
    main(filename="output-2.png", palettes=palettes.DTG_PALETTES, rows=25, columns=35)
