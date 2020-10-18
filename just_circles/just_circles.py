import sys
import os
sys.path.append(os.path.abspath('..'))

from lib import colors
from lib import palettes
import cairo
import math
import random


def circle(ctx, color, img_width, img_height, min_r, max_r):
    r = random.randint(min_r, max_r)
    x = random.randint(r, img_width - r)
    y = random.randint(r, img_height - r)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    alpha = random.uniform(0.2, 0.8)
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()


def main(filename="output.png", palette=random.choice(palettes.PALETTES), circles=100, img_width=3840, img_height=2160):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for _ in range(circles):
        color = palettes.hex_to_tuple(random.choice(palette['colors']))
        circle(ctx, color, img_width, img_height,
               img_height//20, img_height//10)

    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    circles = random.randint(50, 500)
    print(filename, p, circles)
    main(filename=filename, palette=p, img_height=img_height,
         img_width=img_width, circles=100)


if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="refactor-output-{}.png".format(idx),
                    p=random.choice(palettes.PALETTES))
