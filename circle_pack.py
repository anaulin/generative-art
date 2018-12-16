from PIL import Image, ImageDraw
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

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840

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


def concentric(draw, circle, colors, background):
    (center_x, center_y) = circle.center()
    # First color is outside color -- not background
    next_color = random.choice(colors)
    for radius in range(circle.r, MIN_RADIUS, -int(MIN_RADIUS * 1.5)):
        top_left_x = center_x - radius
        top_left_y = center_y - radius
        draw.ellipse([top_left_x, top_left_y, top_left_x + 2 *
                      radius, top_left_y + 2 * radius], fill=next_color)
        if next_color == background:
            next_color = random.choice(colors)
        else:
            next_color = background


def main(palette=PALETTE_1, filename=None):
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT),
                    color=palette['background'])

    circles = []
    for _ in range(TOTAL_CIRCLE_ATTEMPTS):
        c = makeRandomCircle(circles)
        if c:
            print("New circle added. Total circles: ", len(circles))
            circles.append(c)
        else:
            print(".")

    draw = ImageDraw.Draw(img)
    for c in circles:
        concentric(draw, c, palette['colors'], palette['background'])
        # draw.ellipse([c.x, c.y, c.x + 2 * c.r, c.y + 2 * c.r],
        #             fill=random.choice(palette['colors']))

    img.show()
    if filename:
        img.save(filename, 'jpeg')


if __name__ == "__main__":
    palettes = [PALETTE_1, PALETTE_2, PALETTE_3,
                PALETTE_4, PALETTE_5, PALETTE_6]
    #palettes = [PALETTE_6]
    counter = 1
    for p in palettes:
        main(palette=p)
        counter += 1
