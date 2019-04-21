import random

from fingers import fingers
from pyramids import pyramids
from reeds import reeds
from esses import esses

experiments = [
    fingers.make_random,
    pyramids.make_random,
    reeds.make_random,
    esses.make_random
]

if __name__ == "__main__":
    for idx in range(10):
        exp = random.choice(experiments)
        exp(filename="output-{}.png".format(idx))