import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

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

    def pack(self, circles, max_radius, img_width, img_height):
        if self.r >= max_radius:
            return self

        grown_radius = self.r + 1
        grown_circle = Circle(self.x, self.y, grown_radius)
        while not grown_circle.intersectsAnythingElse(circles) and grown_circle.insideCanvas(img_width, img_height):
            grown_radius += 1
            if grown_radius >= max_radius:
                break
            grown_circle = Circle(self.x, self.y, grown_radius)

        grown_circle = Circle(self.x, self.y, grown_radius - 1)
        if not grown_circle.intersectsAnythingElse(circles) and grown_circle.insideCanvas(img_width, img_height):
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

    def insideCanvas(self, img_width, img_height):
        return ((self.x + 2 * self.r <= img_width)
                and (self.y + 2 * self.r) <= img_height)


def randomCircleWithRadius(radius, img_width, img_height):
    return Circle(
        random.randint(0, img_width - 2 * radius),
        random.randint(0, img_height - 2 * radius),
        radius
    )


def makeRandomCircle(circles, min_radius, max_radius, img_width, img_height):
    # simple version, without "growing" circles to pack the space
    # return makeRandomCircleSeed(circles, radius=random.randint(MIN_RADIUS, MAX_RADIUS))
    c = maybeMakeRandomCircleSeed(circles, min_radius, img_width, img_height)
    if not c:
        return None

    return c.pack(circles, max_radius, img_width, img_height)


def maybeMakeRandomCircleSeed(circles, radius, img_width, img_height):
    c = randomCircleWithRadius(radius, img_width, img_height)
    if c.intersectsAnythingElse(circles):
        # Did not succeed at finding a good spot
        return None

    return c


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def concentric(ctx, circle, palette, min_radius, step=1.5):
    colors = palette['colors']
    background = palette['background']
    (center_x, center_y) = circle.center()
    radii = range(circle.r, min_radius, - int(min_radius * step))
    for idx, radius in enumerate(radii):
        if idx % 2 == 0:
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.set_source_rgb(*hex_to_tuple(random.choice(colors)))
            ctx.fill()
        else:
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.set_source_rgb(*hex_to_tuple(background))
            ctx.fill()

def main(palette=random.choice(palettes.PALETTES), filename="output.png", img_width=3840, img_height=2160):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Background
    ctx.rectangle(0, 0, img_width, img_width)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    min_radius = int(img_height / 150)
    max_radius = int(img_height / 7)
    circles = []
    for _ in range(TOTAL_CIRCLE_ATTEMPTS):
        c = makeRandomCircle(circles, min_radius, max_radius, img_width, img_height)
        if c:
            print("New circle added. Total circles: ", len(circles))
            circles.append(c)
        else:
            print(".")

    for c in circles:
        step = random.uniform(1.1, 5)
        concentric(ctx, c, palette, min_radius, step=step)

    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=3840, img_height=2160):
    print(filename, p)
    main(filename=filename, palette=p, img_height=img_height, img_width=img_width)

if __name__ == "__main__":
    for idx in range(1):
        main(palette=random.choice(palettes.PALETTES), filename="output-{}.png".format(idx))
