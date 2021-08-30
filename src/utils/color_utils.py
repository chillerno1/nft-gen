from PIL import Image
import numpy as np
import colorsys


RGB_TO_HSV = np.vectorize(colorsys.rgb_to_hsv)
HSV_TO_RGB = np.vectorize(colorsys.hsv_to_rgb)


def colorize(image, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    img = image.convert('RGBA')
    arr = np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(_shift_hue(arr, hue / 360.).astype('uint8'), 'RGBA')

    return new_img


def _shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = RGB_TO_HSV(r, g, b)
    h = hout
    r, g, b = HSV_TO_RGB(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr
