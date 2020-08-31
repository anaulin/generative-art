import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors


def diagonal(ctx, color, line_width, img_width, img_height):
    if random.random() < 0.5:
        start_x = -line_width
        start_y = random.randint(img_height // 3, img_height - line_width)
        ctx.move_to(start_x, start_y)
    else:
        start_x = random.randint(-line_width, img_width // 3)
        start_y = img_height + line_width
        ctx.move_to(start_x, start_y)

    end_x = random.randint(start_x + 2 * line_width, img_width)
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


def main(filename="output.png", palette=random.choice(palettes.PALETTES), count=30, line_width=30, img_width=3840, img_height=2160):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for _ in range(count):
        diagonal(ctx, random.choice(palette['colors']), line_width, img_width, img_height)

    ims.write_to_png(filename)

def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    c = random.randint(10, 50)
    lw = random.randint(30, 300)
    print(filename, p, c, lw)
    main(filename=filename, palette=p, count=c, line_width=lw, img_height=img_height, img_width=img_width)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx), p=random.choice(palettes.PALETTES))
