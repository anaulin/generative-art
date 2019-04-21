import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def tile(ctx, x, y, size, color1, color2, fill):
    def paint(color):
        ctx.set_source_rgb(*color)
        if fill:
            ctx.fill()
        else:
            ctx.set_line_width(max(size / 50, 1))
            ctx.stroke()


    if random.random() < 0.5:
        ctx.rectangle(x, y, size / 2, size / 2)
        paint(color1)

        ctx.rectangle(x + size / 2, y + size / 2, size / 2, size / 2)
        paint(color2)
    else:
        ctx.rectangle(x + size / 2, y, size / 2, size / 2)
        paint(color1)

        ctx.rectangle(x, y + size / 2, size / 2, size / 2)
        paint(color2)

def main(filename="output.png", img_width=2000, n=10, palette=random.choice(palettes.PALETTES), fill=True):
    img_height = img_width   # Work only with square images
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    size = img_width / n
    for r in range(n):
        for c in range(n):
            hex_colors = random.choices(palette['colors'], k=2)
            color1 = palettes.hex_to_tuple(hex_colors[0])
            color2 = palettes.hex_to_tuple(hex_colors[1])
            tile(ctx, c * size, r * size, size, color1, color2, fill)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx in range(5):
        n = random.randint(4, 32)
        fill = random.choice([True, False])
        main(filename="output-{}.png".format(idx), n=n, palette=random.choice(palettes.PALETTES), fill=fill)
