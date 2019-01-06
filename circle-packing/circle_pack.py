import cairo
import math
import random


# Palette #1
BEIGE = '#EDEDCF'
YELLOW = '#EEC525'
LIGHT_PINK = '#C05F73'
RASPBERRY = '#9D2045'
PURPLE = '#511253'
PLUM = '#3A1B3D'
PALETTE_1 = {
    'background': BEIGE,
    'colors': [LIGHT_PINK, RASPBERRY, PURPLE, PLUM, YELLOW]
}

# Palette #2
BEIGE = '#EDEDCF'
DARK_BLUE = '#102F45'
AQUA = '#27A8A8'
GREY_BLUE = '#78A6A8'
PALETTE_2 = {
    'background': BEIGE,
    'colors': [DARK_BLUE, AQUA, GREY_BLUE]
}

# Palette #3
WHITE = '#F6F3F2'
TAN = '#8B7266'
GREY_PURPLE = '#9B8791'
MAROON = '#7B4955'
DARK_PURPLE = '#35303D'
PALETTE_3 = {
    'background': DARK_PURPLE,
    'colors': [WHITE, TAN, GREY_PURPLE, MAROON]
}

PALETTE_4 = {
    'background': '#090909',
    'colors': ['#4B5043', '#9BC4BC', '#D3FFE9', '#8DDBE0']
}

PALETTE_5 = {
    'background': '#6E44FF',
    'colors': ['#B892FF', '#FFC2E2', '#FF90B3', '#EF7A85']
}

PALETTE_6 = {
    'background': PALETTE_5['background'],
    'colors': PALETTE_1['colors'] + PALETTE_5['colors']
}

# DTG recommended colors
RASPBERRY_RED = '#E60A96'  # (230, 10, 150)
TRUE_RED = '#D21446'  # (210, 20, 70)
PASTEL_PINK = '#FFAFBE'  # (255, 175, 190)
LIGHT_BLUE = '#0AA5E1'  # (10, 165, 225)
VIOLET_PURPLE = '#9B4BA0'  # (155, 75, 160)
BRIGHT_GREEN = '#19FF46'  # (25, 255, 70)
BRIGHT_YELLOW = '#FFF000'  # (255, 240, 0)
BRIGHT_ORANGE = '#F58228'  # (245, 130, 40)
TRUE_BLACK = '#050000'  # (CMYK 55, 55, 55, 100)

DTG_PALETTE_REDS = {
    'background': TRUE_BLACK,
    'colors': [TRUE_RED, '#FFAC81', '#5C0029', '#912F56', PASTEL_PINK]
}

DTG_PALETTE_BLUES = {
    'background': TRUE_BLACK,
    'colors': [LIGHT_BLUE, '#55DDE0', '#587291', '#083D77', '#0B3954']
}

# Final image dimensions
# Threadless wall art recommended: 12000 x 8400px JPG
# Blanket recommended: 12500 x 9375px JPG
#IMG_HEIGHT = 2160
#IMG_WIDTH = 3840
IMG_HEIGHT = 6300  # 4200
IMG_WIDTH = 7200  # 4800

# Circle paramaters
MIN_RADIUS = int(IMG_HEIGHT / 150)
MAX_RADIUS = int(IMG_HEIGHT / 7)

TOTAL_CIRCLE_ATTEMPTS = 100000

# Empty distance between circles
SPACING = 2


class Circle:
    # Defined by top-left corner of bounding box, and radius
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.r)

    def intersects(self, otherCircle):
        center_1 = self.center()
        center_2 = otherCircle.center()
        x_dist = center_1[0] - center_2[0]
        y_dist = center_1[1] - center_2[1]
        return ((self.r + otherCircle.r + SPACING)
                >= math.sqrt(x_dist * x_dist + y_dist * y_dist))

    def center(self):
        return (self.x + self.r, self.y + self.r)

    def pack(self, circles):
        if self.r >= MAX_RADIUS:
            return self

        grown_circle = Circle(self.x, self.y, self.r + 1)
        if not grown_circle.intersectsAnythingElse(circles) and grown_circle.insideCanvas():
            return grown_circle.pack(circles)
        else:
            return self

    def intersectsAnythingElse(self, circles):
        if not circles:
            return False

        for otherCircle in circles:
            if self.intersects(otherCircle):
                return True
        return False

    def insideCanvas(self):
        return ((self.x + 2 * self.r <= IMG_WIDTH)
                and (self.y + 2 * self.r) <= IMG_HEIGHT)


def randomCircleWithRadius(radius):
    return Circle(
        random.randint(0, IMG_WIDTH - 2 * radius),
        random.randint(0, IMG_HEIGHT - 2 * radius),
        radius
    )


def makeRandomCircle(circles):
    # simple version, without "growing" circles to pack the space
    # return makeRandomCircleSeed(circles, radius=random.randint(MIN_RADIUS, MAX_RADIUS))
    c = maybeMakeRandomCircleSeed(circles)
    if not c:
        return None

    return c.pack(circles)


def maybeMakeRandomCircleSeed(circles, radius=MIN_RADIUS):
    c = randomCircleWithRadius(radius)
    if c.intersectsAnythingElse(circles):
        # Did not succeed at finding a good spot
        return None

    return c


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def concentric(ctx, circle, colors):
    (center_x, center_y) = circle.center()
    radii = range(circle.r, MIN_RADIUS, -int(MIN_RADIUS * 1.5))
    for idx, radius in enumerate(radii):
        if idx % 2 == 0:
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.set_source_rgb(*hex_to_tuple(random.choice(colors)))
            ctx.fill()
        else:
            ctx.set_operator(cairo.OPERATOR_SOURCE)
            ctx.set_source(cairo.SolidPattern(0.0, 0.0, 0.0, 0.0))
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.fill()


def main(palette=PALETTE_1, filename="output.png"):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    circles = []
    for _ in range(TOTAL_CIRCLE_ATTEMPTS):
        c = makeRandomCircle(circles)
        if c:
            print("New circle added. Total circles: ", len(circles))
            circles.append(c)
        else:
            print(".")

    for c in circles:
        concentric(ctx, c, palette['colors'])

    ims.write_to_png(filename)


if __name__ == "__main__":
    palettes = [DTG_PALETTE_REDS, DTG_PALETTE_BLUES]
    for idx, p in enumerate(palettes):
        main(palette=p, filename="output-{}.png".format(idx))
