import cairo
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

# Final image dimensions
# Threadless wall art recommended: 12000 x 8400px JPG
# Blanket recommended: 12500 x 9375px JPG
IMG_HEIGHT = 6000
IMG_WIDTH = int(IMG_HEIGHT * 1.5)


def nested_squares(ctx, x, y, width, palette, step=100):
    center_x = x + int(width/2)
    center_y = y + int(width/2)
    previous_color = None
    for current_width in range(width, 0, -2*step):
        if current_width < (step/2):
            break
        current_x = center_x - int(current_width/2)
        current_y = center_y - int(current_width/2)
        color = palettes.random_color(palette)
        while color == previous_color:
            color = palettes.random_color(palette)
        previous_color = color
        ctx.set_source_rgb(*color)
        ctx.rectangle(current_x, current_y, current_width, current_width)
        ctx.fill()

def main(palette=palettes.PALETTE_1, filename="output-1-palette.png"):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    rows = 8
    columns = rows * 1.5
    cell_size = int(IMG_WIDTH / columns)
    num_squares_per_cell = 4
    step_size = int(cell_size / (2 * num_squares_per_cell))
    for y in range(0, IMG_HEIGHT, cell_size):
        for x in range(0, IMG_WIDTH, cell_size):
            nested_squares(ctx, x, y, cell_size, palette, step=step_size)

    ims.write_to_png(filename)


if __name__ == "__main__":
    # for idx, p in enumerate(palettes.PALETTES):
    #     main(palette=p, filename="output-{}.png".format(idx))
    main(palette=palettes.DTG_PALETTE_BLUES)
