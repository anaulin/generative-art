import random

from esses import esses
from fingers import fingers
from pyramids import pyramids
from reeds import reeds
from shaky_circles import shaky_cirles
from shaky_squares import shaky_squares

experiments = [
    fingers.make_random,
    pyramids.make_random,
    reeds.make_random,
    esses.make_random,
    shaky_cirles.make_random,
    shaky_squares.make_random
]

if __name__ == "__main__":
    for idx in range(10):
        exp = random.choice(experiments)
        exp(filename="output-{}.png".format(idx))
