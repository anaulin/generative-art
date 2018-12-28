import cairo
import random

IMG_HEIGHT = 2160
IMG_WIDTH = 3840

LINE_WIDTH = 5

PALETTE = ['#4B5043', '#9BC4BC', '#D3FFE9', '#8DDBE0']

PALETTE_2 = ['#EEC525', '#C05F73', '#9D2045', '#511253',
             '#3A1B3D', '#B892FF', '#FFC2E2', '#FF90B3', '#EF7A85', '#6E44FF']


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def draw_line(ctx, x, y, x2, y2, line_width, color):
    ctx.move_to(x, y)
    ctx.line_to(x2, y2)

    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LineCap.ROUND)

    # g = cairo.LinearGradient(start[0], start[1], end[0], end[1])
    # colors = [hex_to_tuple(c) for c in random.choices(PALETTE_2, k=2)]
    # g.add_color_stop_rgb(0, *colors[0])
    # g.add_color_stop_rgb(1, *colors[1])
    # ctx.set_source(g)
    ctx.set_source_rgb(*color)
    ctx.stroke()


def main(filename="output.png", count=15):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    # Drawing horizontal lines
    line_width = int(IMG_HEIGHT / count)
    color = hex_to_tuple('#9D2045')
    for y in range(int(line_width / 2), IMG_HEIGHT, line_width):
        end = random.randint(int(IMG_WIDTH*3/4), IMG_WIDTH - line_width)
        draw_line(ctx, 0, y, end, y, line_width, color)
        # Shade color
        color = tuple(c * 0.9 for c in color)

    ims.write_to_png(filename)


if __name__ == "__main__":
    main()
