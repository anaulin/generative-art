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

def line(ctx, y, line_interval, color, x_increment=(IMG_WIDTH // 40)):
    line_width = line_interval // 20
    x = 0
    ctx.move_to(x, y)
    nodes = []
    while x < IMG_WIDTH:
        x += random.randint(x_increment // 2, x_increment)
        y_offset = random.randint(0, line_interval // 2 - SPACING)
        y_offset = y_offset if random.random() < 0.5 else -1 * y_offset
        nodes.append((x, y + y_offset))
        ctx.line_to(x, y + y_offset)
    ctx.set_source_rgb(*color)
    ctx.set_line_width(line_width)
    ctx.stroke()
    for node in nodes:
        (node_x, node_y) = node
        r = random.randint(line_width * 2, line_width * 4)
        ctx.arc(node_x, node_y, r, 0, 2 * math.pi)
        ctx.set_source_rgb(*color)
        ctx.fill()
        # Ring around the node
        ctx.arc(node_x, node_y, r, 0, 2 * math.pi)
        ctx.set_source_rgb(*random.choice(colors.shades(color, 5)))
        ctx.set_line_width(line_width)
        ctx.stroke()


def main(filename="output.png", palette=random.choice(palettes.PALETTES), lines=20):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    line_interval = IMG_HEIGHT // lines
    for y in range(line_interval, IMG_HEIGHT, line_interval):
        color = palettes.hex_to_tuple(random.choice(palette['colors']))
        line(ctx, y, line_interval, color)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, l in enumerate([5, 10, 15, 20, 40]):
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), lines=l)
