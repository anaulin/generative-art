import math
import os
import random
import sys

import cairo
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840


def bar(ctx, color, line_width, img_width, img_height, existing_shapes, max_attempts=10):
    def getStartXY():
        x = random.randint(line_width // 2, img_width - line_width // 2)
        y = random.randint(line_width // 2, img_height - line_width // 2)
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
        if not existing_shapes.intersects(new_bar) and within_canvas(end_x, end_y, img_width - line_width, img_height - line_width):
            end_x = new_end_x
            end_y = new_end_y
            bar = new_bar
        else:
            failed_attempts += 1
            max_increment = int(max_increment * 3/4)
            if max_increment < 1:
                break

    # Draw line
    color_t = palettes.hex_to_tuple(color)
    draw_line(ctx, start_x, start_y, end_x, end_y, color_t, line_width)

    # Draw highlights
    tints = colors.tints(color_t, 5)
    ctx.save()
    ctx.translate(line_width//4, line_width//4)
    highlight_width = max(line_width // 5, 2)
    draw_line(ctx, start_x, start_y, end_x, end_y, tints[-2], highlight_width)
    ctx.translate(max(highlight_width//2, 1), 0)
    draw_line(ctx, start_x, start_y, end_x, end_y, tints[-1], max(highlight_width// 4, 1))
    ctx.restore()

    return existing_shapes.union(bar)

def draw_line(ctx, start_x, start_y, end_x, end_y, color, line_width):
    ctx.move_to(start_x, start_y)
    ctx.line_to(end_x, end_y)
    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_source_rgb(*color)
    ctx.stroke()

def within_canvas(x, y, width, height):
    return x > 0 and x < width and y > 0 and y < height

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
    for idx, count in enumerate([20, 50, 100, 40]):
        main(filename="output-{}.png".format(idx), count=count, line_width=random.randint(40, 160), palette=random.choice(palettes.PALETTES))
