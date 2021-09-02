import sys
from pathlib import Path

from nftgen.command.Command import Command
from nftgen.command.CommandManager import CommandManager
from nftgen.generate import create_image, generate
from nftgen.settings import config

cm = CommandManager()


def main():
    register_commands()
    start_listening()


def start_listening():
    while True:
        args = input(">").split()
        if len(args) > 0:
            cm.execute(args[0], *args[1:])


def register_commands():
    cm.register(Command(
        name="generate",
        aliases=["g", "gen", "create", "c", "build", "b"],
        executor=c_generate,
    ))

    cm.register(Command(
        name="quit",
        aliases=["q", "exit", "stop", "leave"],
        executor=c_quit,
    ))


def c_generate(*args):
    amount = 1

    if len(args) > 0:
        arg = args[0]
        try:
            int_arg = int(arg)
            if int_arg > 0:
                amount = int_arg
            else:
                print(f"Has to be a positive integer: \"{arg}\"")
                return
        except ValueError:
            print(f"Not a number: \"{arg}\"")
            return

    for n in range(amount):
        nft = generate(str(n))
        image = create_image(nft)

        print(f"{nft.name}: {nft.get_properties()}")

        out = config.output_dir
        Path(out).mkdir(parents=True, exist_ok=True)
        image.save(f"{out}/{n}.png")


def c_quit(*args):
    sys.exit()


if __name__ == '__main__':
    main()
