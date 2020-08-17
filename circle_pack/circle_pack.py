import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

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

        grown_radius = self.r + 1
        grown_circle = Circle(self.x, self.y, grown_radius)
        while not grown_circle.intersectsAnythingElse(circles) and grown_circle.insideCanvas():
            grown_radius += 1
            if grown_radius >= MAX_RADIUS:
                break
            grown_circle = Circle(self.x, self.y, grown_radius)

        grown_circle = Circle(self.x, self.y, grown_radius - 1)
        if not grown_circle.intersectsAnythingElse(circles) and grown_circle.insideCanvas():
            return grown_circle
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


def concentric(ctx, circle, palette, step=1.5):
    colors = palette['colors']
    background = palette['background']
    (center_x, center_y) = circle.center()
    radii = range(circle.r, MIN_RADIUS, -int(MIN_RADIUS * step))
    for idx, radius in enumerate(radii):
        if idx % 2 == 0:
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.set_source_rgb(*hex_to_tuple(random.choice(colors)))
            ctx.fill()
        else:
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.set_source_rgb(*hex_to_tuple(background))
            ctx.fill()


def main(palette=random.choice(palettes.PALETTES), filename="output.png"):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    circles = []
    for _ in range(TOTAL_CIRCLE_ATTEMPTS):
        c = makeRandomCircle(circles)
        if c:
            print("New circle added. Total circles: ", len(circles))
            circles.append(c)
        else:
            print(".")

    for c in circles:
        step = random.uniform(1.1, 5)
        concentric(ctx, c, palette, step=step)

    ims.write_to_png(filename)


def make_random(filename="output.png"):
    p = random.choice(palettes.PALETTES)
    print(filename, p)
    main(filename=filename, palette=p)

if __name__ == "__main__":
    for idx in range(1):
        main(palette=random.choice(palettes.PALETTES), filename="output-{}.png".format(idx))
