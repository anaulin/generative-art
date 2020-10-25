import random
from math import pi, sqrt

import cairo

from lib import colors, palettes


class Drops:
    def __init__(self, filename="output.png", img_width=2000, img_height=2000, count=5, palette=random.choice(palettes.PALETTES)):
        self.filename = filename
        self.palette = palette
        self.width = img_width
        self.height = img_height
        self.count = count
        self.ims = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.ims)
        self.make_solid_background()

    def make_solid_background(self):
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.set_source_rgb(
            *palettes.hex_to_tuple(self.palette['background']))
        self.ctx.fill()

    def write_to_file(self):
        self.ims.write_to_png(self.filename)

    def make_drop(self, x, y, width, height):
        """Make a drop inside the given bounding box."""
        self.ctx.save()
        self.ctx.translate(x, y)

        color = palettes.hex_to_tuple(random.choice(self.palette['colors']))
        radius = width // 2
        cx = radius
        cy = height - radius
        top_middle = (cx, 0)
        (tang1, tang2) = self.tangential_points(cx, cy, radius, *top_middle)
        self.ctx.move_to(*top_middle)
        self.ctx.line_to(*tang1)
        self.ctx.line_to(*tang2)
        self.ctx.set_source_rgb(*color)
        self.ctx.fill()

        self.ctx.arc(cx, cy, radius, 0, 2 * pi)
        self.ctx.set_source_rgb(*color)
        self.ctx.fill()

        self.ctx.restore()

    def tangential_points(self, cx, cy, radius, px, py):
        """Returns the two tangential points from points (px, py) to circle (cx, cy, radius)"""
        dx, dy = px - cx, py - cy
        dxr, dyr = -dy, dx
        d = sqrt(dx**2 + dy**2)
        if d < radius:
            raise ValueError(
                f"({px}, {py}) is inside ({cx}, {cy}, {radius}). No tangential possible.")

        rho = radius / d
        ad = rho**2
        bd = rho*sqrt(1-rho**2)
        tx1 = cx + ad*dx + bd*dxr
        ty1 = cy + ad*dy + bd*dyr
        tx2 = cx + ad*dx - bd*dxr
        ty2 = cy + ad*dy - bd*dyr
        return ((tx1, ty1), (tx2, ty2))

    def dream(self):
        x_interval = self.width // (self.count * 2)
        y_interval = self.height // self.count
        margin = 5
        for y in range(0, self.height, y_interval):
            for x in range(0, self.width, x_interval):
                self.make_drop(x + margin, y + margin, x_interval - 2 * margin, y_interval - 2 * margin)
        self.write_to_file()

    @staticmethod
    def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=2000, img_height=2000):
        c = random.randint(3, 10)
        drops = Drops(filename=filename, palette=p, count=c,
                      img_height=img_height, img_width=img_width)
        drops.dream()


if __name__ == "__main__":
    for idx in range(5):
        Drops.make_random(filename="output-{}.png".format(idx),
                          p=random.choice(palettes.PALETTES))
