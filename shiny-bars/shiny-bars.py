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

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840


def bar(ctx, color, line_width, img_width, img_height, existing_shapes, max_attempts=100):
    def getStartXY():
        x = random.randint(line_width, img_width - line_width)
        y = random.randint(line_width, img_height - line_width)
        return (x, y)

    # 1. Get a start point that doesn't overlap with anything we already have.
    (start_x, start_y) = getStartXY()
    startPoint = Point(start_x, start_y).buffer(line_width // 2, resolution=8)
    for _ in range(max_attempts * 100):
        if not existing_shapes.intersects(startPoint):
            break
        (start_x, start_y) = getStartXY()
        startPoint = Point(start_x, start_y).buffer(line_width // 2, resolution=8)
    # For the rare case that we did not find a working point.
    if existing_shapes.intersects(startPoint):
        print("Could not find valid start point!")
        return existing_shapes

    end_x = start_x
    end_y = start_y
    bar = LineString([(start_x, start_y), (start_x, start_y)]
                     ).buffer(line_width)

    # 2. Grow the bar as far as possible, randomly.
    failed_attempts = 0
    max_increment = 500
    while failed_attempts < max_attempts:
        new_end_x = end_x
        new_end_y = end_y
        increment = random.randint(1, max_increment)
        if random.random() < 0.5:
            increment = -1 * increment
        if random.random() < 0.5:
            new_end_x += increment
        else:
            new_end_y += increment
        new_bar = LineString(
            [(start_x, start_y), (new_end_x, new_end_y)]).buffer(line_width)
        if not existing_shapes.intersects(new_bar) and within_canvas(new_end_x, new_end_y, img_width, img_height, line_width):
            end_x = new_end_x
            end_y = new_end_y
            bar = new_bar
        else:
            failed_attempts += 1
            max_increment = int(max_increment * 3/4)
            if max_increment < 1:
                break

    if end_x == start_x and end_y == start_y:
        print("Couldn't grow bar")
        return existing_shapes

    # 3. Draw the bar
    color_t = palettes.hex_to_tuple(color)
    tints = colors.tints(color_t, 5)
    shades = colors.shades(color_t, 3)

    ctx.move_to(start_x, start_y)
    ctx.line_to(end_x, end_y)
    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LineCap.ROUND)

    # Compute vector for highlight vector
    dx = end_x - start_x
    dy = end_y - start_y
    length = math.sqrt(pow(end_x - start_x, 2) + pow(end_y - start_y, 2))
    # Center point of the bar
    center_x = start_x + (dx / 2)
    center_y = start_y + (dy / 2)
    # Start and end of highlight vector -- perpendicular to bar
    grad_start_x = (center_x + (dy / length) * line_width / 2)
    grad_start_y = (center_y + (-1) * (dx / length) * line_width / 2)
    grad_end_x = (center_x + (-1) * (dy / length) * (line_width / 2))
    grad_end_y = (center_y + (dx / length) * (line_width / 2))

    gradient = cairo.LinearGradient(grad_start_x, grad_start_y, grad_end_x, grad_end_y)
    gradient.add_color_stop_rgb(0, *shades[-2])
    gradient.add_color_stop_rgb(0.7, *tints[-1])
    gradient.add_color_stop_rgb(0.7, *tints[-1])
    gradient.add_color_stop_rgb(0.75, 1, 1, 1)
    gradient.add_color_stop_rgb(0.75, 1, 1, 1)
    gradient.add_color_stop_rgb(0.8, *tints[-1])
    gradient.add_color_stop_rgb(1, *shades[-1])
    ctx.set_source(gradient)
    ctx.stroke()

    return existing_shapes.union(bar)

def within_canvas(x, y, width, height, line_width):
    return x > line_width and x < width - line_width and y > line_width and y < height - line_width

def main(filename="output.png", img_width=IMG_WIDTH, img_height=IMG_HEIGHT, palette=random.choice(palettes.PALETTES), count=50, line_width=80):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    existing_shapes = Point([(0, 0), (0, 0)])
    for i in range(count):
        print("Making bar {}".format(i))
        existing_shapes = bar(ctx, random.choice(
            palette['colors']), line_width, img_width, img_height, existing_shapes)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx, count in enumerate([20, 50, 100, 40, 80]):
        main(filename="output-{}.png".format(7), count=count, line_width=random.randint(100, 200), palette=random.choice(palettes.PALETTES))
