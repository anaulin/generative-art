import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840


def diagonal(ctx, color, line_width):
    if random.random() < 0.5:
        start_x = -line_width
        start_y = random.randint(IMG_HEIGHT // 3, IMG_HEIGHT - line_width)
        ctx.move_to(start_x, start_y)
    else:
        start_x = random.randint(-line_width, IMG_WIDTH // 3)
        start_y = IMG_HEIGHT + line_width
        ctx.move_to(start_x, start_y)

    end_x = random.randint(start_x + 2 * line_width, IMG_WIDTH)
    end_y = random.randint(0, start_y - 2*line_width)
    ctx.line_to(end_x, end_y)
    ctx.set_source(gradient(color, start_x, start_y, end_x, end_y))
    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

def gradient(color, start_x, start_y, end_x, end_y):
    g = cairo.LinearGradient(start_x, start_y, end_x, end_y)
    tints = colors.tints(palettes.hex_to_tuple(color), 5)
    g.add_color_stop_rgb(0, *tints[0])
    g.add_color_stop_rgb(1, *tints[4])
    return g



def main(filename="output.png", palette=random.choice(palettes.PALETTES), count=30, line_width=30):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for _ in range(count):
        diagonal(ctx, color=random.choice(palette['colors']), line_width=line_width)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, params in enumerate([(50, 30), (10, 100), (20, 40), (10, 300)]):
        (count, line_width) = params
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), count=count, line_width=line_width)
