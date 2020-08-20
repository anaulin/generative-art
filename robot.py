import random

from lib import palettes

from bubbles import bubbles
from coral_play import coral_play
from circle_pack import circle_pack
from esses import esses
from fingers import fingers
from fingers_two import fingers_two
from lanterns import lanterns
from pyramids import pyramids
from quarter_circles import quarter_circles
from reeds import reeds
from shaky_circles import shaky_cirles
from shaky_squares import shaky_squares
from tiled_lines import tiled_lines
from triangles import triangles
from triangles_two import triangles_two

experiments = [
    fingers.make_random,
    pyramids.make_random,
    reeds.make_random,
    esses.make_random,
    shaky_cirles.make_random,
    shaky_squares.make_random,
    lanterns.make_random,
    triangles.make_random,
    triangles_two.make_random,
    tiled_lines.make_random,
    bubbles.make_random,
    fingers_two.make_random,
    quarter_circles.make_random,
    coral_play.make_random,
    circle_pack.make_random
]

if __name__ == "__main__":
    # p = palettes.PALETTE_2
    # for idx, exp in enumerate(experiments):
    #     exp(filename="output-{}.png".format(idx), p=p)
    for idx in range(10):
        exp = random.choice(experiments)
        exp(filename="output-{}.png".format(idx))
