import cairo
import math
import random
import randomcolor

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

def random_palette(n=5):
    return {
        'background': '#FFFFFF' if random.random() < 0.5 else '#000000',
        'colors': randomcolor.RandomColor().generate(count=n)
    }

def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))

# For testing
def draw_colors(filename, colors):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    width = IMG_WIDTH // len(colors)
    for idx, c in enumerate(colors):
        ctx.rectangle(idx * width, 0, width, IMG_HEIGHT)
        ctx.set_source_rgb(*c)
        ctx.fill()
    ims.write_to_png(filename)


if __name__ == "__main__":
    p = random_palette()
    print(p)
    colors = [hex_to_tuple(c) for c in p['colors']]
    draw_colors("output.png", colors)
