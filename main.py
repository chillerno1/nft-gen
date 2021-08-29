from random import randrange

import attributes_handler
from generate import generate


def test():  # TODO: remove
    attributes_handler.test()


def main():
    n_species = 1
    n_eyes = 3
    n_mouth = 3

    print(f"Unique monsters: {n_species * n_eyes * n_mouth}")

    monster = generate(
        randrange(n_species),
        randrange(n_eyes),
        randrange(n_mouth),
    )
    monster.show()


if __name__ == '__main__':
    test()
