import random

from bubbles import bubbles
from esses import esses
from fingers import fingers
from lanterns import lanterns
from pyramids import pyramids
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
    bubbles.make_random
]

if __name__ == "__main__":
    for idx in range(10):
        exp = random.choice(experiments)
        exp(filename="output-{}.png".format(idx))
