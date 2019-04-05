import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def tile(ctx, x, y, width, height, color1, color2):
    # Tile corners
    tl = (x, y)
    tr = (x + width, y)
    br = (x + width, y + height)
    bl = (x, y + height)

    # Rotate context around the center of the tile, then shift axes back to top-left corner
    variant = random.randint(1, 4)
    if variant == 1:
        polygon(ctx, [tl, bl, br, tl], color1)
        polygon(ctx, [tl, tr, br, tl], color2)
    elif variant == 2:
        polygon(ctx, [tl, tr, br, tl], color1)
        polygon(ctx, [tl, bl, br, tl], color2)
    elif variant == 3:
        polygon(ctx, [bl, br, tr, bl], color1)
        polygon(ctx, [bl, tl, tr, bl], color2)
    else:
        polygon(ctx, [bl, tl, tr, bl], color1)
        polygon(ctx, [bl, br, tr, bl], color2)

def polygon(ctx, points, color):
    for point in points:
        ctx.line_to(*point)
    ctx.set_source_rgb(*color)
    ctx.fill()

def main(filename="output.png", img_width=2000, img_height=2000, rows=20, columns=20, palette=random.choice(palettes.PALETTES)):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()


    col_width = img_width // columns
    row_height = img_height // rows
    for r in range(rows):
        for c in range(columns):
            hex_colors = random.choices(palette['colors'] + [palette['background']], k=2)
            color1 = palettes.hex_to_tuple(hex_colors[0])
            color2 = palettes.hex_to_tuple(hex_colors[1])
            tile(ctx, c * col_width, r * row_height, col_width, row_height, color1, color2)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx in range(5):
        r = random.randint(5, 50)
        main(filename="output-{}.png".format(idx), rows=r, columns=r, palette=random.choice(palettes.PALETTES))
