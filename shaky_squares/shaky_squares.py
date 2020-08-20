import math
import os
import random
import sys

import cairo

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def tile(ctx, x, y, size, cols, count=4, shakiness=8, line_width=3):
    shake_factor = (size / 2) / shakiness
    x = x + shake_factor + 1
    y = y + shake_factor + 1
    size = size - 2 * shake_factor - 2
    def shake():
        return random.uniform(-1 * shake_factor, shake_factor)
    for _ in range(count - 1):
        start = (x + shake(), y + shake())
        ctx.move_to(*start)
        ctx.line_to(x + size + shake(), y + shake())
        ctx.line_to(x + size + shake(), y + size + shake())
        ctx.line_to(x + shake(), y + size + shake())
        ctx.line_to(*start)
        color = colors.hex_to_tuple(random.choice(cols))
        ctx.set_source_rgb(*color)
        ctx.set_line_width(line_width)
        ctx.stroke()

def main(filename="output.png", img_width=2000, n=10, shake_count=5, palette=random.choice(palettes.PALETTES), shakiness=8, line_width=5):
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
            tile(ctx, frame + c * size, frame + r * size, size, palette['colors'], count=shake_count, shakiness=shakiness, line_width=line_width)

    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=2000, img_height=2000):
    n = random.randint(4, 32)
    c = random.randint(2, 16)
    s = random.randint(3, 10)
    l = random.randint(1, 8)
    print(filename, n, c, s, l, p, img_width, img_height)
    main(filename=filename, n=n, palette=p, shake_count=c, shakiness=s, line_width=l, img_width=max(img_width, img_height))

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
