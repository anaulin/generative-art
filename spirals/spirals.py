import cairo
import math
import os
import sys
import random

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def spiral(ctx, height, width, color):
    x = width / 2
    y = height / 2
    angle = 0.0
    delta_x = 0.2
    delta_y = 0.2
    maxPoints = [x * 0.1 for x in range(0, 390)]
    ctx.move_to(x, y)
    for i in maxPoints:
        theta = delta_y * i
        angle = delta_x * math.exp(theta)
        x = angle * math.cos(i) + width/2
        y = angle * math.sin(i) + height/2
        ctx.line_to(x, y)
    ctx.set_line_width(3)
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_source_rgb(*palettes.hex_to_tuple(color))
    ctx.stroke()

def main(filename="output.png", img_width=2000, img_height=2000, palette=random.choice(palettes.PALETTES)):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    spiral(ctx, img_height, img_width, random.choice(palette['colors']))

    ims.write_to_png(filename)

def make_random(filename="output.png"):
    p = random.choice(palettes.PALETTES)
    print(filename, os.path.basename(__file__), p)
    main(filename=filename, palette=p)

if __name__ == "__main__":
    for idx in range(1):
        make_random(filename="output-{}.png".format(idx))
