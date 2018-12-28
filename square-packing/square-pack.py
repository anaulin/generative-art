import cairo
import random

# Image size
IMG_HEIGHT = 2160
IMG_WIDTH = 3840
RATIO = IMG_HEIGHT / IMG_WIDTH

# Square size parameters
MIN_SIZE_FRACTION = 1/1000
MAX_SIZE_FRACTION = 1/3

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

SQUARE_ATTEMPTS = 10000

SPACING = 1/500


def random_color(palette):
    hex = random.choice(palette['colors'])
    return hex_to_tuple(hex)

def random_colors(palette, n):
    hex = random.choices(palette['colors'], k=n)
    return [hex_to_tuple(h) for h in hex]

def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def intersects(squares, x, y, size):
    for s in squares:
        (sx, sy, ssize) = s
        sx = sx - SPACING * RATIO
        sy = sy - SPACING
        ssize = ssize + SPACING * 2
        # Check for overlap in x and y
        overlap_x = (sx <= x + size * RATIO) and (sx + ssize * RATIO >= x)
        overlap_y = (sy <= y + size) and (sy + ssize >= y)
        if overlap_x and overlap_y:
            return True
    return False


def is_inside_canvas(x, y, size):
    return (x + (SPACING + size) * RATIO < 1.0 and y + SPACING + size < 1.0)


def make_random_square(squares):
    x = random.random()
    y = random.random()
    size = MIN_SIZE_FRACTION
    if intersects(squares, x, y, size) or not is_inside_canvas(x, y, size):
        return None

    while (not intersects(squares, x, y, size) and size <= MAX_SIZE_FRACTION
           and is_inside_canvas(x, y, size)):
        size += 1/1000

    # Remove the last increment that caused us to intersect.
    size -= 1/1000

    return (x, y, size)


def get_random_gradient(square, palette):
    (x, y, size) = square
    g = cairo.LinearGradient(x, y, x + size * RATIO, y + size)
    colors = random_colors(palette, 2)
    g.add_color_stop_rgb(0, *colors[0])
    g.add_color_stop_rgb(1, *colors[1])
    return g


def main(palette=PALETTE_1):
    #ims = cairo.SVGSurface("output.svg", IMG_WIDTH, IMG_HEIGHT)
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)
    ctx.scale(IMG_WIDTH, IMG_HEIGHT)

    # Set background color
    ctx.set_source_rgb(*hex_to_tuple(palette['background']))
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()

    squares = []
    for _ in range(SQUARE_ATTEMPTS):
        s = make_random_square(squares)
        if s:
            print("New square added: ", s)
            squares.append(s)
        else:
            print(".")

    for s in squares:
        (x, y, size) = s
        ctx.rectangle(x, y, size * RATIO, size)
        #(r, g, b) = random_color()
        ctx.set_source(get_random_gradient(s, palette))
        ctx.fill()

    ims.write_to_png("output.png")


if __name__ == "__main__":
    main(PALETTE_3)
