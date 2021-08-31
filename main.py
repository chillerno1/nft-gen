from generate import generate


def main():
    nft = generate()

    print(nft.attributes)
    nft.image.show()


if __name__ == '__main__':
    main()
