from PIL import Image, ImageDraw
import math
import random


YELLOW = '#EEC525'
TAN = '#A68260'
LIGHT_PINK = '#C05F73'
RASPBERRY = '#9D2045'
PURPLE = '#511253'
PLUM = '#3A1B3D'

# 4K resolution: 3840 x 2160
IMG_HEIGHT = 2160
IMG_WIDTH = 3840
#IMG_HEIGHT = 1000
#IMG_WIDTH = 1000

MIN_RADIUS = int(IMG_HEIGHT / 100)
MAX_RADIUS = int(IMG_HEIGHT / 4)

MAX_NEW_CIRCLE_ATTEMPTS = 100

SPACING = 1


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
    c = makeRandomCircleSeed(circles)
    if not c:
        return None

    return c.pack(circles)


def makeRandomCircleSeed(circles, radius=MIN_RADIUS):
    c = randomCircleWithRadius(radius)
    for _ in range(MAX_NEW_CIRCLE_ATTEMPTS):
        if not c.intersectsAnythingElse(circles):
            break
        c = randomCircleWithRadius(radius)

    if c.intersectsAnythingElse(circles):
        # For the case where despite all the tries it didn't work
        return None

    return c


def main():
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color=YELLOW)

    circles = []
    for _ in range(500):
        c = makeRandomCircle(circles)
        if c:
            circles.append(c)

    draw = ImageDraw.Draw(img)
    for c in circles:
        draw.ellipse([c.x, c.y, c.x + 2 * c.r, c.y + 2 * c.r],
                     fill=random.choice([PURPLE, LIGHT_PINK, RASPBERRY, PLUM]))

    img.show()


if __name__ == "__main__":
    main()
