import cairo
import random

IMG_HEIGHT = 2160
IMG_WIDTH = 3840

LINE_WIDTH = 5

PALETTE = {
    'background': '#090909',
    'colors': ['#4B5043', '#9BC4BC', '#D3FFE9', '#8DDBE0']
}


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))

def draw_line(ctx, x, y, width, height, line_width):
    leftToRight = random.random() >= 0.5

    if leftToRight:
        start = (x, y)
        end = (x + width, y + height)
    else:
        start = (x + width, y)
        end = (x, y + height)

    ctx.move_to(start[0], start[1])
    ctx.line_to(end[0], end[1])

    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LineCap.ROUND)

    g = cairo.LinearGradient(start[0], start[1], end[0], end[1])
    colors = [hex_to_tuple(c) for c in random.choices(PALETTE['colors'], k=2)]
    g.add_color_stop_rgb(0, *colors[0])
    g.add_color_stop_rgb(1, *colors[1])
    ctx.set_source(g)
    #ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()

def main(filename="output.png", step=50, line_width=5):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Make background white
    ctx.set_source_rgb(256, 256, 256)
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    for x in range(0, IMG_WIDTH, step):
        for y in range(0, IMG_HEIGHT, step):
            draw_line(ctx, x, y, step, step, line_width=line_width)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for i in [1, 2, 3]:
        main(filename="output-{}-color.png".format(i), step=i*30, line_width=20)
