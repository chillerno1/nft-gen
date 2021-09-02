import sys
import traceback
import warnings
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
            try:
                cm.execute(args[0], *args[1:])
            except Exception:
                traceback.print_exc()


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

        image_path = f"{out}/{nft.name}.png"
        try:
            image.save(image_path)
        except Exception:
            traceback.print_exc()
            warnings.warn(f"Could not save \"{image_path}\". Make sure that the file is not open in another program!")


def c_quit(*args):
    sys.exit()


if __name__ == '__main__':
    main()
