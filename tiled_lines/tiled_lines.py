import cairo
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

IMG_HEIGHT = 2160
IMG_WIDTH = 3840

LINE_WIDTH = 5

def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def draw_line(ctx, x, y, width, height, line_width, palette):
    leftToRight = random.random() >= 0.5

    if leftToRight:
        start = (x, y)
        end = (x + width, y + height)
    else:
        start = (x + width, y)
        end = (x, y + height)

    ctx.move_to(start[0], start[1])
    ctx.line_to(end[0], end[1])

    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LineCap.ROUND)

    g = cairo.LinearGradient(start[0], start[1], end[0], end[1])
    colors = [hex_to_tuple(c) for c in random.choices(palette['colors'], k=2)]
    g.add_color_stop_rgb(0, *colors[0])
    g.add_color_stop_rgb(1, *colors[1])
    ctx.set_source(g)
    ctx.stroke()


def main(filename="output.png", step=50, line_width=5, palette=random.choice(palettes.PALETTES)):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    for x in range(0, IMG_WIDTH, step):
        for y in range(0, IMG_HEIGHT, step):
            draw_line(ctx, x, y, step, step, line_width=line_width, palette=palette)

    ims.write_to_png(filename)

def make_random(filename="output.png", p=random.choice(palettes.PALETTES)):
    step_size = IMG_WIDTH // random.randint(3, 90)
    line_width = step_size // random.randint(2, 8)
    print(filename, os.path.basename(__file__), step_size, line_width, p)
    main(filename=filename, step=step_size, line_width=line_width, palette=p)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-random-{}.png".format(idx))
