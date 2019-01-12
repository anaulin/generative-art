import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

# Final image dimensions
IMG_HEIGHT = 1200
IMG_WIDTH = IMG_HEIGHT


PANTONE_LIVING_CORAL_TCX = '#FF6F61'
DARK_TEAL = '#004c4c'

SPACING = 1

def polyp(ctx, x, y, width, height, color):
    min_dimension = min(width, height)
    center_x = x + int(width/2)
    center_y = y + int(width/2)
    radius = random.randint(int(min_dimension / 10), int(min_dimension / 6))

    for _ in range(12):
        line_width = radius // 5
        ball_radius = int(line_width * 1.5)

        ctx.save()
        ctx.translate(center_x, center_y)
        ctx.move_to(0, 0)
        end_x = random.randint(-width // 2 + ball_radius, width // 2 - ball_radius)
        end_y = random.randint(-height // 2 + ball_radius, height // 2 - ball_radius)
        ctx.line_to(end_x, end_y)
        ctx.set_line_width(line_width)
        ctx.set_line_cap(cairo.LineCap.ROUND)
        g = cairo.LinearGradient(0, 0, end_x, end_y)
        add_gradient_stops(color, g)
        ctx.set_source(g)
        ctx.stroke()
        # Ball at the end

        g = cairo.RadialGradient(end_x, end_y, 0, end_x, end_y, ball_radius)
        add_gradient_stops(color, g)
        ctx.set_source(g)
        ctx.arc(end_x, end_y, ball_radius, 0, 2 * math.pi)
        ctx.fill()
        ctx.restore()

    # Draw in center
    g = cairo.RadialGradient(center_x, center_y, 0, center_x, center_y, radius)
    add_gradient_stops(color, g)
    ctx.set_source(g)
    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
    ctx.fill()


def color_variant(color):
    original = palettes.hex_to_tuple(color)
    adjust_by = random.uniform(0.0, 0.5)
    if random.random() < 0.5:
        return tuple(((1 - c) * adjust_by + c) for c in original)
    else:
        return tuple((c * adjust_by + c) for c in original)


def add_gradient_stops(color, gradient):
    gradient.add_color_stop_rgb(0, *color_variant(color))
    gradient.add_color_stop_rgb(1, *color_variant(color))


def main(filename="output.png"):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.set_source_rgb(*palettes.hex_to_tuple(DARK_TEAL))
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    rows = 4
    columns = 4
    cell_width = int(IMG_WIDTH / columns)
    cell_height = int(IMG_HEIGHT / rows)
    for y in range(0, IMG_HEIGHT, cell_height):
        for x in range(0, IMG_WIDTH, cell_width):
            polyp(ctx, x, y, cell_width, cell_height, PANTONE_LIVING_CORAL_TCX)

    ims.write_to_png(filename)


if __name__ == "__main__":
    main(filename="output.png")
