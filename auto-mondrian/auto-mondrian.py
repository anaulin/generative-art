import cairo
import random

# Image size
IMG_HEIGHT = 2160
IMG_WIDTH = 3840
RATIO = IMG_WIDTH / IMG_HEIGHT

PALETTE_1 = {
    'background': '#000000',
    'colors': ['#EEC525', '#C05F73', '#9D2045', '#511253', '#3A1B3D',
               '#B892FF', '#FFC2E2', '#FF90B3', '#EF7A85', '#6E44FF']
}

PALETTE_2 = {
    'background': '#090909',
    'colors': ['#4B5043', '#9BC4BC', '#D3FFE9', '#8DDBE0']
}

PALETTE_3 = {
    'background': '#6E44FF',
    'colors': ['#B892FF', '#FFC2E2', '#FF90B3', '#EF7A85']
}

# Mondrian colors
YELLOW = '#FEFC0D'
RED = '#FD0100'
BLUE = '#002DFD'
PALETTE = {
    'background': '#FFFFFF',
    'colors': [YELLOW, RED, BLUE]
}


def random_color(palette):
    hex = random.choice(palette['colors'])
    return hex_to_tuple(hex)


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def area(x1, y1, x2, y2):
    return abs((x2 - x1) * (y2 - y1) * RATIO)


def cleave_rectangle(x1, y1, x2, y2):
    print("cleaving: ", x1, y1, x2, y2)
    if (x2 - x1) >= (y2 - y1):
        # X is biggest dimension
        new_x = random.randint(x1, x2)
        r1 = (x1, y1, new_x, y2)
        r2 = (new_x, y1, x2, y2)
    else:
        # Y is biggest dimension
        new_y = random.randint(y1, y2)
        r1 = (x1, new_y, x2, y2)
        r2 = (x1, y1, x2, new_y)

    if area(*r1) < 60 or area(*r2) < 60:
        # If it's too small, try again
        return cleave_rectangle(x1, y1, x2, y2)

    # Return the biggest rectangle first
    if area(*r1) >= area(*r2):
        return (r1, r2)
    else:
        return (r2, r1)


def main(palette=PALETTE, filename="output.png"):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Set background color
    ctx.set_source_rgb(256, 256, 256)
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    remaining = (0, 0, IMG_WIDTH, IMG_HEIGHT)
    rectangles = []
    for _ in range(8):
        (bigger_r, smaller_r) = cleave_rectangle(*remaining)
        remaining = bigger_r
        rectangles.append(smaller_r)
    rectangles.append(remaining)

    to_paint = random.sample(rectangles, k=len(palette['colors']))
    for (r, c) in zip(to_paint, palette['colors']):
        print("painting: ", r)
        (x1, y1, x2, y2) = r
        ctx.rectangle(x1, y1, x2-x1, y2-y1)
        ctx.set_source_rgb(*hex_to_tuple(c))
        ctx.fill()

    line_width = 20
    for (x1, y1, x2, y2) in rectangles:
        line_width = 20
        ctx.move_to(x1, y1)
        ctx.line_to(x1, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        ctx.move_to(x1, y2)
        ctx.line_to(x2, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        ctx.move_to(x2, y2)
        ctx.line_to(x1, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        ctx.move_to(x1, y2)
        ctx.line_to(x1, y2)
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

    # Also line the entire outer rectangle
    ctx.move_to(0,0)
    ctx.line_to(IMG_WIDTH, 0)
    ctx.set_line_width(line_width)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()

    ctx.move_to(IMG_WIDTH, 0)
    ctx.line_to(IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()

    ctx.move_to(IMG_WIDTH, IMG_HEIGHT)
    ctx.line_to(0, IMG_HEIGHT)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()

    ctx.move_to(0, IMG_HEIGHT)
    ctx.line_to(0, 0)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()


    ims.write_to_png(filename)


if __name__ == "__main__":
    for i in [1, 2, 3]:
        main(filename="output-{}.png".format(i))
