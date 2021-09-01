from pathlib import Path

from nftgen.generate import generate, create_image
from nftgen.settings import config


def main():
    for n in range(1):
        nft = generate(str(n))
        image = create_image(nft)

        print(f"{nft.name}: {nft.get_properties()}")

        out = config.output_dir
        Path(out).mkdir(parents=True, exist_ok=True)
        image.save(f"{out}/{n}.png")


if __name__ == '__main__':
    main()
