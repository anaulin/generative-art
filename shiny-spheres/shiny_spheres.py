import math
import os
import random
import sys

import cairo
from shapely.affinity import rotate
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def sphere(ctx, color, img_width, img_height, existing_shapes, min_radius=10, max_attempts=100):
    def getStartXY():
        x = random.randint(min_radius, img_width - min_radius)
        y = random.randint(min_radius, img_height - min_radius)
        return (x, y)

    # 1. Get a start point that doesn't overlap with anything we already have.
    (start_x, start_y) = getStartXY()
    sphere = Point(start_x, start_y).buffer(min_radius, resolution=8)
    for _ in range(max_attempts * 100):
        if not existing_shapes.intersects(sphere):
            break
        (start_x, start_y) = getStartXY()
        sphere = Point(start_x, start_y).buffer(min_radius, resolution=8)
    # For the rare case that we did not find a working point.
    if existing_shapes.intersects(sphere):
        print("Could not find valid start point!")
        return existing_shapes

    # 2. Grow the sphere as far as possible, randomly.
    failed_attempts = 0
    max_increment = 500
    radius = min_radius
    while failed_attempts < max_attempts:
        new_radius = radius + max_increment
        new_sphere = Point(start_x, start_y).buffer(new_radius, resolution=12)
        if not existing_shapes.intersects(new_sphere) and within_canvas(start_x, start_y, img_width, img_height, new_radius):
            radius = new_radius
            sphere = new_sphere
        else:
            failed_attempts += 1
            max_increment = int(max_increment * 3/4)
            if max_increment < 1:
                break

    # 3. Draw the sphere
    color_t = palettes.hex_to_tuple(color)
    tints = colors.tints(color_t, 5)
    shades = colors.shades(color_t, 3)

    ctx.arc(start_x, start_y, radius, 0, 2 * math.pi)

    gradient = cairo.RadialGradient(start_x - (1/2) * radius, start_y + (1/2) * radius, 0, start_x - (1/4) * radius, start_y + (1/4) * radius, radius * (5/4))
    gradient.add_color_stop_rgb(0, 1, 1, 1)
    gradient.add_color_stop_rgb(0.9, *tints[-1])
    gradient.add_color_stop_rgb(1, *shades[-1])
    ctx.set_source(gradient)
    ctx.fill()

    buffered_sphere = Point(start_x, start_y).buffer(radius + 5, resolution=12)
    return existing_shapes.union(buffered_sphere)

def within_canvas(x, y, width, height, line_width):
    return x > line_width and x < width - line_width and y > line_width and y < height - line_width

def main(filename="output.png", img_width=2000, img_height=2000, palette=random.choice(palettes.PALETTES), count=50):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    existing_shapes = Point([(0, 0), (0, 0)])
    for i in range(count):
        print("Making sphere {}".format(i))
        existing_shapes = sphere(ctx, random.choice(palette['colors']), img_width, img_height, existing_shapes)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, count in enumerate([20, 50, 100, 40, 80]):
        main(filename="output-{}.png".format(idx), count=count, palette=random.choice(palettes.PALETTES))
