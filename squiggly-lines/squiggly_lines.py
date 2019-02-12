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

def line(ctx, y, line_interval, color, x_increment=(IMG_WIDTH // 40), fill=True):
    x = 0
    ctx.move_to(x, y)
    while x < IMG_WIDTH:
        x += random.randint(x_increment // 2, x_increment)
        y_offset = random.randint(0, line_interval // 2)
        y_offset = y_offset if random.random() < 0.5 else -1 * y_offset
        ctx.line_to(x, y + y_offset)
    ctx.set_source_rgb(*color)
    if fill:
        ctx.line_to(IMG_WIDTH, IMG_HEIGHT)
        ctx.line_to(0, IMG_HEIGHT)
        ctx.line_to(0, y)
        ctx.fill()
    else:
       ctx.set_line_width(line_interval // 20)
       ctx.stroke()


def main(filename="output.png", palette=random.choice(palettes.PALETTES), lines=20, fill=True):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    #ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.set_source_rgb(*(palette['background']))
    ctx.fill()

    line_interval = IMG_HEIGHT // lines
    for y in range(0, IMG_HEIGHT, line_interval):
        color = palettes.hex_to_tuple(random.choice(palette['colors']))
        line(ctx, y, line_interval, color, fill=fill)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, l in enumerate([5, 10, 20, 50]):
        f = True if random.random() < 0.5 else False
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), lines=l, fill=f)
