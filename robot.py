import argparse
import random

from lib import palettes

from auto_mondrian import auto_mondrian
from bubbles import bubbles
from circle_pack import circle_pack
from color_field import color_field
from coral_play import coral_play
from esses import esses
from fingers import fingers
from fingers_two import fingers_two
from just_circles import just_circles
from lanterns import lanterns
from nested_squares import nested_squares
from petal_grid import petal_grid
from pyramids import pyramids
from quarter_circles import quarter_circles
from reeds import reeds
from robots import robots
from shaky_circles import shaky_cirles
from shaky_squares import shaky_squares
from thick_diagonals import thick_diagonals
from tiled_lines import tiled_lines
from triangles import triangles
from triangles_two import triangles_two

from dreams.drops import Drops

experiments = [
    auto_mondrian.make_random,
    bubbles.make_random,
    circle_pack.make_random,
    color_field.make_random,
    coral_play.make_random,
    esses.make_random,
    fingers_two.make_random,
    fingers.make_random,
    just_circles.make_random,
    lanterns.make_random,
    nested_squares.make_random,
    petal_grid.make_random,
    pyramids.make_random,
    quarter_circles.make_random,
    reeds.make_random,
    robots.make_random,
    shaky_cirles.make_random,
    shaky_squares.make_random,
    thick_diagonals.make_random,
    tiled_lines.make_random,
    triangles_two.make_random,
    triangles.make_random,
    Drops.make_random
]

if __name__ == "__main__":
    # p = palettes.RAINBOW
    # for idx, exp in enumerate(experiments):
    #     exp(filename="output-{}.png".format(idx), p=p, img_width=9075, img_height=9075)
    parser = argparse.ArgumentParser(description='Run the robot.')
    parser.add_argument('--count', type=int, default=10,
                        help='Number of art pieces to produce')
    parser.add_argument('--img_width', type=int, default=2000,
                        help='Img width to use')
    parser.add_argument('--img_height', type=int, default=2000,
                        help='Img width to use')
    args = parser.parse_args()
    print(
        f"Generating {args.count} images with height/width of ({args.img_height}, {args.img_width})")
    for idx in range(args.count):
        exp = random.choice(experiments)
        exp(filename="output-{}.png".format(idx),
            img_height=args.img_height, img_width=args.img_width)
