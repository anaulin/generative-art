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

SPACING = 2

def circle(ctx, color, min_r=IMG_HEIGHT//20, max_r=IMG_HEIGHT//10):
    r = random.randint(min_r, max_r)
    x = random.randint(r, IMG_WIDTH -r)
    y = random.randint(r, IMG_HEIGHT -r)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    alpha = random.uniform(0.2, 0.8)
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()

def main(filename="output.png", palette=random.choice(palettes.PALETTES), circles=100):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for _ in range(circles):
        color = palettes.hex_to_tuple(random.choice(palette['colors']))
        circle(ctx, color)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, c in enumerate([50, 100, 500, 1000]):
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), circles=c)
