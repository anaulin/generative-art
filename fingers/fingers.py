import cairo
import random

IMG_HEIGHT = 2160
IMG_WIDTH = 3840

LINE_WIDTH = 5

PALETTE = ['#4B5043', '#9BC4BC', '#D3FFE9', '#8DDBE0']

PALETTE_2 = ['#EEC525', '#C05F73', '#9D2045', '#511253',
             '#3A1B3D', '#B892FF', '#FFC2E2', '#FF90B3', '#EF7A85', '#6E44FF']

PALETTE_3 = ['#201A4C', '#31274C', '#263E3F', '#1A274C', '#16384C']

PALETTE_4 = ['#0E1906', '#252D1A', '#593949', '#6B5364', '#756670']

PALETTE_5 = ['#D3AC63', '#D89450', '#DB7741', '#5E2513']

PALETTE_6 = ['#DB5ABA', '#C455A8', '#FF8CC6', '#DE369D', '#6F5E76']

PALETTE_7 = ['#30C5FF', '#44AF69', '#5C946E', '#80C2AF', '#A0DDE6']


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


def main(filename="output.png", count=40, layers=80, palette=PALETTE_7):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
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
            colors = random.choices(palette, k=2)
            color = tuple(((1 - c) * lighten_by + c)
                          for c in hex_to_tuple(colors[0]))
            color2 = tuple(((1 - c) * lighten_by + c)
                           for c in hex_to_tuple(colors[1]))
            draw_line(ctx, x, IMG_HEIGHT, x, end, line_width, color, color2)

    ims.write_to_png(filename)


if __name__ == "__main__":
    params = []
    params.append((5, 10, PALETTE_6))
    params.append((50, 10, PALETTE_6))
    params.append((50, 50, PALETTE_6 + PALETTE_7))
    params.append((10, 20, PALETTE_7))
    params.append((100, 30, PALETTE_7 + PALETTE))
    params.append((6, 5, PALETTE_2))

    count = 1
    for (c, l, p) in params:
        main(filename="output-{}-{}-{}.png".format(c,
                                                   l, count), count=c, layers=l, palette=p)
        count += 1
