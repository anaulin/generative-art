import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes
from lib import colors

# Final image dimensions
IMG_HEIGHT = 2000
IMG_WIDTH = int(IMG_HEIGHT * (16/9))

SPACING = 2

def lines(ctx, colors, x, y, width, height, num_steps, line_width):
    ctx.save()
    ctx.translate(x + width / 2, y + height / 2)
    ctx.rotate(random.uniform(- math.pi / 2, math.pi / 2))
    ctx.translate(-width/2, -height/2)

    step_size = min(width, height) // num_steps
    current_x = 0
    while current_x < width:
        ctx.move_to(current_x, 0)
        ctx.line_to(current_x, height)
        ctx.set_source_rgb(*palettes.hex_to_tuple(random.choice(colors)))
        ctx.set_line_width(line_width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        current_x += step_size
    ctx.restore()

def main(filename="output.png", palette=random.choice(palettes.PALETTES), num_columns=12, num_rows=12, num_steps=[1, 2, 3], line_width=4):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    column_size = IMG_WIDTH // num_columns
    row_size = IMG_HEIGHT // num_rows
    for c in range(num_columns):
        for r in range(num_rows):
            if r < num_rows // 3:
                current_num_steps = num_steps[0]
            elif r < 2 * num_rows // 3:
                current_num_steps = num_steps[1]
            else:
                current_num_steps = num_steps[2]
            lines(ctx, palette['colors'], c * column_size, r * row_size, column_size, row_size, current_num_steps, line_width)

    ims.write_to_png(filename)


if __name__ == "__main__":
    main(filename="output-0.png", palette=random.choice(palettes.PALETTES), num_columns=12, num_rows=15, num_steps=[1, 2, 3], line_width=6)
    main(filename="output-1.png", palette=random.choice(palettes.PALETTES), num_columns=21, num_rows=21, num_steps=[2, 4, 6], line_width=4)
    main(filename="output-2.png", palette=random.choice(palettes.PALETTES), num_columns=27, num_rows=27, num_steps=[5, 10, 15], line_width=1)
    main(filename="output-3.png", palette=random.choice(palettes.PALETTES), num_columns=12, num_rows=9, num_steps=[1, 2, 3], line_width=3)
    main(filename="output-4.png", palette=random.choice(palettes.PALETTES), num_columns=21, num_rows=6, num_steps=[2, 4, 8], line_width=2)
    main(filename="output-5.png", palette=random.choice(palettes.PALETTES), num_columns=9, num_rows=3, num_steps=[2, 4, 8], line_width=5)
