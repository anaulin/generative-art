import cairo
import os
import sys
import random

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes

def draw_line(ctx, x, y, x2, y2, line_width, color):
    def draw_it(width, col):
        ctx.move_to(x, y)
        ctx.line_to(x2, y2)

        ctx.set_line_width(width)
        ctx.set_line_cap(cairo.LineCap.ROUND)
        ctx.set_source_rgb(*col)
        ctx.stroke()

    outline_col = colors.shades(color, 3)[-2]
    outline_width = max(2, line_width / 8)

    # Draw slightly thicker "outline" first, then thinner "inner" line
    draw_it(line_width, outline_col)
    draw_it(line_width - outline_width, color)

def main(filename="output.png", img_width=2000, img_height=2000, count=40, layers=80, palette=random.choice(palettes.PALETTES)):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    line_width = int(img_width / count)
    layer_height = int(img_height / layers)
    layer_offset = 0
    for l in range(layers + 1):
        if layer_offset == 0:
            layer_offset = int(line_width / 2)
        else:
            layer_offset = 0
        for x in range(layer_offset, img_width + line_width, line_width):
            end = random.randint(l * layer_height,
                                 (l + 1) * layer_height) - int(layer_height / 2)
            draw_line(ctx, x, img_height, x, max(end, line_width / 2), line_width,
                palettes.hex_to_tuple(random.choice(palette['colors'])))

    ims.write_to_png(filename)

def make_random(filename="output.png", p=random.choice(palettes.PALETTES)):
    l = random.randint(5, 25)
    c = random.randint(5, 25)
    print(filename, os.path.basename(__file__), c, l, p)
    main(filename=filename, count=c, layers=l, palette=p)

if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx))
