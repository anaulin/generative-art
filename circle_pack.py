from PIL import Image, ImageDraw
import math
import random


# Palette #1
YELLOW = '#EEC525'
LIGHT_PINK = '#C05F73'
RASPBERRY = '#9D2045'
PURPLE = '#511253'
PLUM = '#3A1B3D'
PALETTE_1 = {
    # Bright yellow
    'background': YELLOW,
    'colors': [LIGHT_PINK, RASPBERRY, PURPLE, PLUM]
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


def main():
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT),
                    color=PALETTE_3['background'])

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
        draw.ellipse([c.x, c.y, c.x + 2 * c.r, c.y + 2 * c.r],
                     fill=random.choice(PALETTE_3['colors']))

    img.show()
    #img.save('images/circle-pack-palette1-4.jpg', 'jpeg')


if __name__ == "__main__":
    main()
