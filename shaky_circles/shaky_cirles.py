import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def tile(ctx, x, y, size, cols, count=4):
    shake_factor = (size / 2) / 8
    radius = (size / 2) - shake_factor
    for _ in range(count):
        x_shake = random.uniform(-1 * shake_factor, shake_factor)
        y_shake = random.uniform(-1 * shake_factor, shake_factor)
        ctx.arc(x + size / 2 + x_shake, y + size / 2 + y_shake, radius, 0, 2 * math.pi)
        color = colors.hex_to_tuple(random.choice(cols))
        ctx.set_source_rgb(*color)
        ctx.set_line_width(max(shake_factor / 5, 1))
        ctx.stroke()

def main(filename="output.png", img_width=2000, n=10, shake_count=5, palette=random.choice(palettes.PALETTES)):
    img_height = img_width   # Work only with square images
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*colors.hex_to_tuple(palette['background']))
    ctx.fill()

    frame = 20  # empty space around image border
    size = (img_width - 2*frame) / n
    for r in range(n):
        for c in range(n):
            tile(ctx, frame + c * size, frame + r * size, size, palette['colors'], count=shake_count)

    ims.write_to_png(filename)


def make_random(filename="output.png"):
    n = random.randint(4, 32)
    p = random.choice(palettes.PALETTES)
    c = random.randint(4, 10)
    main(filename=filename, n=n, palette=p, shake_count=c)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
