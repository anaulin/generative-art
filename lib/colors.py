import cairo
import math
import random

import palettes

# Final image dimensions
IMG_HEIGHT = 1000
IMG_WIDTH = 1500


def gradient(start_col, end_col, steps):
    colors = []
    pairs = list(zip(start_col, end_col))
    for s in range(steps):
        color = tuple(s * (p[1] - p[0]) / steps + p[0] for p in pairs)
        colors.append(color)
    return colors

def tints(color, n):
    return gradient(color, (1, 1, 1), n + 1)[0:n]

def shades(color, n):
    return gradient(color, (0, 0, 0), n + 1)[0:n]

# For testing
def draw_gradient(filename, start_col, end_col, steps):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    colors = tints(start_col, steps)
    width = IMG_WIDTH // len(colors)
    for idx, c in enumerate(colors):
        ctx.rectangle(idx * width, 0, width, IMG_HEIGHT)
        ctx.set_source_rgb(*c)
        ctx.fill()
    ims.write_to_png(filename)


if __name__ == "__main__":
    c = palettes.hex_to_tuple(palettes.DARK_BLUE)
    draw_gradient("output.png", c, c, 5)
