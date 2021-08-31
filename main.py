from generate import generate
from settings import config


def main():
    for n in range(1):
        nft = generate()
        print(f"{n}: {nft.attributes}")
        nft.image.save(f"{config.output_dir}/{n}.png")


if __name__ == '__main__':
    main()
