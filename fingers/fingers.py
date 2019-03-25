import cairo
import os
import sys
import random

sys.path.append(os.path.abspath('..'))
from lib import palettes

IMG_HEIGHT = 2160
IMG_WIDTH = 3840

LINE_WIDTH = 5

def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def draw_line(ctx, x, y, x2, y2, line_width, color1, color2):
    ctx.move_to(x, y)
    ctx.line_to(x2, y2)

    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LineCap.ROUND)

    g = cairo.LinearGradient(x, y, x2, y2)
    g.add_color_stop_rgb(0, *color1)
    g.add_color_stop_rgb(1, *color2)
    ctx.set_source(g)
    ctx.stroke()


def main(filename="output.png", count=40, layers=80, palette=random.choice(palettes.PALETTES)):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    line_width = int(IMG_WIDTH / count)
    layer_height = int(IMG_HEIGHT / layers)
    lighten_step = 0.75 / layers
    layer_offset = 0
    for l in range(layers + 1):
        lighten_by = lighten_step * l
        if layer_offset == 0:
            layer_offset = int(line_width / 2)
        else:
            layer_offset = 0
        for x in range(layer_offset, IMG_WIDTH + line_width, line_width):
            end = random.randint(l * layer_height,
                                 (l + 1) * layer_height) - int(layer_height / 2)
            colors = random.choices(palette['colors'], k=2)
            color = tuple(((1 - c) * lighten_by + c)
                          for c in hex_to_tuple(colors[0]))
            color2 = tuple(((1 - c) * lighten_by + c)
                           for c in hex_to_tuple(colors[1]))
            draw_line(ctx, x, IMG_HEIGHT, x, end, line_width, color, color2)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for idx in range(10):
        l = random.randint(5, 100)
        c = random.randint(5, 50)
        p = random.choice(palettes.PALETTES)
        main(filename="output-{}-{}-{}.png".format(c,
                                                   l, idx), count=c, layers=l, palette=p)
