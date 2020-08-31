import cairo
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes


# Mondrian colors
YELLOW = '#FEFC0D'
RED = '#FD0100'
BLUE = '#002DFD'
PALETTE = {
    'background': '#FFFFFF',
    'colors': [YELLOW, RED, BLUE]
}


def random_color(palette):
    hex = random.choice(palette['colors'])
    return hex_to_tuple(hex)


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def area(x1, y1, x2, y2, ratio):
    return abs((x2 - x1) * (y2 - y1) * ratio)


def cleave_rectangle(x1, y1, x2, y2, ratio):
    print("cleaving: ", x1, y1, x2, y2)
    if (x2 - x1) >= (y2 - y1):
        # X is biggest dimension
        new_x = random.randint(x1, x2)
        r1 = (x1, y1, new_x, y2)
        r2 = (new_x, y1, x2, y2)
    else:
        # Y is biggest dimension
        new_y = random.randint(y1, y2)
        r1 = (x1, new_y, x2, y2)
        r2 = (x1, y1, x2, new_y)

    if area(*r1, ratio) < 60 or area(*r2, ratio) < 60:
        # If it's too small, try again
        return cleave_rectangle(x1, y1, x2, y2, ratio)

    # Return the biggest rectangle first
    if area(*r1, ratio) >= area(*r2, ratio):
        return (r1, r2)
    else:
        return (r2, r1)

def main(palette=PALETTE, filename="output.png", img_width=3840, img_height=2160):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(ims)

    # Set background color
    ctx.set_source_rgb(256, 256, 256)
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.fill()

    remaining = (0, 0, img_width, img_height)
    rectangles = []
    ratio = img_width / img_width
    for _ in range(8):
        (bigger_r, smaller_r) = cleave_rectangle(*remaining, ratio)
        remaining = bigger_r
        rectangles.append(smaller_r)
    rectangles.append(remaining)

    to_paint = random.sample(rectangles, k=len(palette['colors']))
    for (r, c) in zip(to_paint, palette['colors']):
        print("painting: ", r)
        (x1, y1, x2, y2) = r
        ctx.rectangle(x1, y1, x2-x1, y2-y1)
        ctx.set_source_rgb(*hex_to_tuple(c))
        ctx.fill()

    line_width = 20
    for (x1, y1, x2, y2) in rectangles:
        line_width = 20
        ctx.move_to(x1, y1)
        ctx.line_to(x1, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        ctx.move_to(x1, y2)
        ctx.line_to(x2, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        ctx.move_to(x2, y2)
        ctx.line_to(x1, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        ctx.move_to(x1, y2)
        ctx.line_to(x1, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

    # Also line the entire outer rectangle
    ctx.move_to(0,0)
    ctx.line_to(img_width, 0)
    ctx.set_line_width(line_width)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()

    ctx.move_to(img_width, 0)
    ctx.line_to(img_width, img_height)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()

    ctx.move_to(img_width, img_height)
    ctx.line_to(0, img_height)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()

    ctx.move_to(0, img_height)
    ctx.line_to(0, 0)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()


    ims.write_to_png(filename)

def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    if random.randint(1, 10) <= 3:
        p = PALETTE
    print(filename, p)
    main(filename=filename, palette=p, img_height=img_height, img_width=img_width)


if __name__ == "__main__":
    for i in range(5):
        make_random(filename="output-{}.png".format(i), p=random.choice(palettes.PALETTES), img_width=2000, img_height=2000)
