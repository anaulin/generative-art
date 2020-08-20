import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def tile(ctx, x, y, width, height, color1, color2, fill):
    radius = min(width/2, height/2)
    # Tile corners
    tl = (x, y)
    tr = (x + width, y)
    br = (x + width, y + height)
    bl = (x, y + height)
    # Tile side midpoints
    mt = (x + radius, y)
    mb = (x + radius, y + height)
    ml = (x, y + radius)
    mr = (x + width, y + radius)

    def paint(color):
        ctx.set_source_rgb(*color)
        if fill:
            ctx.fill()
        else:
            ctx.set_line_width(max(width / 50, 1))
            ctx.stroke()


    if random.random() < 0.5:
        ctx.arc(*tl, radius, 0, (1/2) * math.pi)
        if fill:
            ctx.line_to(*tl)
            ctx.line_to(*mt)
        paint(color1)

        ctx.arc(*br, radius, 1 * math.pi,  (3/2) * math.pi)
        if fill:
            ctx.line_to(*br)
            ctx.line_to(*mb)
        paint(color2)
    else:
        ctx.arc(*bl, radius, (3/2) * math.pi , 2 * math.pi)
        if fill:
            ctx.line_to(*bl)
            ctx.line_to(*ml)
        paint(color1)

        ctx.arc(*tr, radius, (1/2) * math.pi, 1 * math.pi)
        if fill:
            ctx.line_to(*tr)
            ctx.line_to(*mr)
        paint(color2)

def polygon(ctx, points, color):
    for point in points:
        ctx.line_to(*point)
    ctx.set_source_rgb(*color)
    ctx.set_line_width(1)
    ctx.stroke()



def main(filename="output.png", img_width=2000, img_height=2000, rows=10, columns=10, palette=random.choice(palettes.PALETTES), fill=True):
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
            hex_colors = random.choices(palette['colors'], k=2)
            color1 = palettes.hex_to_tuple(hex_colors[0])
            color2 = palettes.hex_to_tuple(hex_colors[1])
            tile(ctx, c * col_width, r * row_height, col_width, row_height, color1, color2, fill)

    ims.write_to_png(filename)

def make_random(filename="output.png", p=random.choice(palettes.PALETTES)):
    n = random.randint(4, 16)
    fill = random.choice([True, False])
    print(filename, n, fill, p)
    main(filename=filename, rows=n, columns=n, palette=p, fill= fill)

if __name__ == "__main__":
    for idx in range(5):
        n = random.randint(4, 16)
        fill = random.choice([True, False])
        main(filename="output-{}.png".format(idx), rows=n, columns=n, palette=random.choice(palettes.PALETTES), fill=fill)
