from generate import generate, create_image
from settings import config


def main():
    for n in range(1):
        nft = generate()
        image = create_image(nft)

        print(f"{n}: {nft.get_properties()}")

        image.save(f"{config.output_dir}/{n}.png")


if __name__ == '__main__':
    main()
