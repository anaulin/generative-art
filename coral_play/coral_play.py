from shapely.geometry import Point, LineString
from shapely.ops import unary_union

import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes




PANTONE_LIVING_CORAL_TCX = '#FF6F61'
DARK_TEAL = '#004c4c'
CORAL_PALETTE = {
    'background': DARK_TEAL,
    'colors': [PANTONE_LIVING_CORAL_TCX]
}

SPACING = 1

MAX_ATTEMPTS = 20


def make_limb(width, height, ball_radius):
    end_x = random.randint(-width // 2 + ball_radius,
                           width // 2 - ball_radius)
    end_y = random.randint(-height // 2 + ball_radius,
                           height // 2 - ball_radius)
    return (end_x, end_y)


def polyp(ctx, x, y, width, height, color):
    min_dimension = min(width, height)
    center_x = x + width // 2
    center_y = y + height // 2
    radius = random.randint(int(min_dimension / 10), int(min_dimension / 6))

    line_width = radius // 5
    ball_radius = int(line_width * 1.5)
    center = Point(0, 0).buffer(radius)
    existing_shapes = center.buffer(-0.1)
    for _ in range(20):
        for _ in range(MAX_ATTEMPTS):
            (end_x, end_y) = make_limb(width, height, ball_radius)
            ball = Point(end_x, end_y).buffer(ball_radius)
            line = LineString([(0, 0), (end_x, end_y)]).buffer(line_width).difference(center)
            limb = line.union(ball)
            if not existing_shapes.intersects(limb):
                break
        else:
            continue

        existing_shapes = existing_shapes.union(limb)

        # Draw line
        ctx.save()
        ctx.translate(center_x, center_y)
        ctx.move_to(0, 0)
        ctx.line_to(end_x, end_y)
        ctx.set_line_width(line_width)
        ctx.set_line_cap(cairo.LineCap.ROUND)
        g = cairo.LinearGradient(0, 0, end_x, end_y)
        add_gradient_stops(color, g)
        ctx.set_source(g)
        ctx.stroke()

        # Draw ball at the end
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

def main(filename="output.png", img_width=3840, img_height=2160, palette=CORAL_PALETTE, rows=6, columns=6):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.fill()

    cell_width = img_width // columns
    cell_height = img_height // rows
    for y in range(0, img_height, cell_height):
        for x in range(0, img_width, cell_width):
            polyp(ctx, x, y, cell_width, cell_height, random.choice(palette['colors']))

    ims.write_to_png(filename)

def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    count = random.choice([5, 6, 7, 8, 10])
    print(filename, count, p)
    main(filename=filename, rows=count, columns=random.randint(count, int(count * 1.5)), palette=p, img_height=img_height, img_width=img_width)

if __name__ == "__main__":
    for idx, count in enumerate([5, 6, 7, 8, 10]):
        main(filename="output-{}.png".format(idx), rows=count, columns=random.randint(count, int(count * 1.5)), palette=random.choice(palettes.PALETTES))
