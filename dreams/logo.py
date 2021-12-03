import random
from math import pi, sqrt
import numpy as np
import cv2

import cairo

from lib import colors, palettes

warhol_palette = [
    (220, 200, 39),
    (37, 202, 193),
    (55, 184, 162),
    (93, 123, 172),
    (239, 170, 214),
    (207, 24, 49)
]

neon_palette = [
    (53, 91, 193),
    (196, 113, 209),
    (17, 226, 220),
    (255, 97, 159),
    (247, 233, 48),
    (255, 43, 78),
]

xmas_palette = [
    (21, 80, 46),
    (18, 96, 52),
    (246, 171, 52),
    (231, 67, 50),
    (178, 40, 41)
]

def rgb_to_bgr(rgb):
    (r, g, b) = rgb
    return (b, g, r)

def palette_to_bgr(p):
    return [rgb_to_bgr(c) for c in p]

local_palettes = [palette_to_bgr(warhol_palette), palette_to_bgr(neon_palette), palette_to_bgr(xmas_palette)]
for p in palettes.PALETTES:
    p_255 = [colors.hex_to_255_tuple(c) for c in p['colors']]
    local_palettes.append(palette_to_bgr(p_255))

class Logo:
    def __init__(self, filename="output.png", img_width=2000, img_height=2000, rows=6, columns=5, palette=random.choice(palettes.PALETTES)):
        self.filename = filename
        self.palette = palette
        self.width = img_width
        self.height = img_height
        self.rows = rows
        self.columns = columns
        self.ims = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.ims)

    def make_solid_background(self):
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.set_source_rgb(
            *palettes.hex_to_tuple(self.palette['background']))
        self.ctx.fill()

    def write_to_file(self):
        self.ims.write_to_png(self.filename)

    def dream1(self):
        logo = cv2.imread("logo_1000x1000.png")
        final = None
        for _ in range(self.rows):
            row = None
            for _ in range(self.columns):
                colored = np.zeros_like(logo)
                colored[:] = random.choice(self.palette)
                val = 0.75
                colorized_logo = cv2.addWeighted(colored, val, logo, 1 - val, 0)
                if row is not None:
                    row = cv2.hconcat([row, colorized_logo])
                else:
                    row = colorized_logo
            if final is not None:
                final = cv2.vconcat([final, row])
            else:
                final = row
        cv2.imwrite(self.filename, final)

    def dream2(self):
        # Import image as grayscale
        logo = cv2.imread("logo_500x500.png", 0)
        # extract dimensions
        original_image_height, original_image_width = logo.shape
        new_logo_width = int(self.width/self.columns)
        logo = cv2.resize(logo, (new_logo_width, int(original_image_height*(new_logo_width/original_image_width))))

        # extract dimensions
        original_image_height, original_image_width = logo.shape

        max_dots = 150
        # down size to number of dots
        if original_image_height == max(original_image_height,original_image_width):
            downsized_image = cv2.resize(logo,(int(original_image_height*(max_dots/original_image_width)),max_dots))
        else:
            downsized_image = cv2.resize(logo,(max_dots,int(original_image_height*(max_dots/original_image_width))))
        # extract dimensions of new image
        downsized_image_height, downsized_image_width = downsized_image.shape
        # set how big we want our final image to be
        #multiplier = 100
        multiplier = int(new_logo_width / max_dots)

        # set the size of our blank canvas
        blank_img_height = downsized_image_height * multiplier
        blank_img_width = downsized_image_width * multiplier

        # set the padding value so the dots start in frame (rather than being off the edge
        padding = int(multiplier/2)

        final = None
        for _ in range(self.rows):
            print("making row")
            row = None
            for _ in range(self.columns):
                print("making column")
                #background_color = random.choice(self.palette)
                #dots_color = (0,0,0)
                [background_color, dots_color] = random.sample(self.palette, 2)

                # create canvas containing just the background colour
                blank_image = np.full(((blank_img_height),(blank_img_width),3), background_color,dtype=np.uint8)

                # run through each pixel and draw the circle on our blank canvas
                for y in range(0,downsized_image_height):
                    for x in range(0,downsized_image_width):
                        cv2.circle(blank_image,(((x*multiplier)+padding),((y*multiplier)+padding)), int((0.6 * multiplier) * ((255-downsized_image[y][x])/255)), dots_color, -1)

                if row is not None:
                    row = cv2.hconcat([row, blank_image])
                else:
                    row = blank_image
            if final is not None:
                final = cv2.vconcat([final, row])
            else:
                final = row
        cv2.imwrite(self.filename, final)


    @staticmethod
    def make_random(filename="output.png", p=random.choice([neon_palette, warhol_palette]), img_width=10000, img_height=10000):
        r = random.randint(3, 10)
        c = random.randint(r, r * 2 - 1)

        logo = Logo(filename=filename, palette=p, rows=r, columns=c,
                      img_height=img_height, img_width=img_width)
        logo.dream2()


if __name__ == "__main__":
    i = 0
    for p in local_palettes:
        Logo.make_random(filename=f"tiled-{i}.png", p=p)
        i +=1
        break
