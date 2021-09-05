import colorsys
from typing import Optional, Tuple

from PIL import Image
import numpy as np

from nftgen.image.ColorMatch import ColorMatch


def _rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype("float")
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv


def _hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype("uint8")
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype("uint8")


def _set_hue(arr, hout, match: Optional[ColorMatch] = None):
    hsv = _rgb_to_hsv(arr)
    for x, a in enumerate(hsv[..., 0]):
        for y, b in enumerate(a):
            if match is None or match.is_match(b * 360):
                hsv[..., 0][x][y] = hout
    rgb = _hsv_to_rgb(hsv)
    return rgb


def _set_color(arr, hsv1):
    hsv = _rgb_to_hsv(arr)
    for y, a in enumerate(hsv[..., 0]):
        for x, b in enumerate(a):
            sat = hsv[y][x][1]
            val = hsv[y][x][2]
            alpha = hsv[y][x][3]
            hsv[y][x] = [hsv1[0], hsv1[1] * sat, hsv1[2] * (val / 255), alpha]
    rgb = _hsv_to_rgb(hsv)
    return rgb


def _shift_hue(arr, hout, match: Optional[ColorMatch] = None):
    hsv = _rgb_to_hsv(arr)
    for x, a in enumerate(hsv[..., 0]):
        for y, b in enumerate(a):
            if match is None or match.is_match(b * 360):
                hsv[..., 0][x][y] = b + hout
    rgb = _hsv_to_rgb(hsv)
    return rgb


def _rainbowify1(arr, hsv1, hsv2):
    hsv = _rgb_to_hsv(arr)
    x_len = len(hsv[..., 0][0])
    for y, a in enumerate(hsv[..., 0]):
        for x, b in enumerate(a):
            sat = hsv[y][x][1]
            val = hsv[y][x][2]
            alpha = hsv[y][x][3]
            if alpha == 0:
                continue
            hsva = [0, 0, 0, alpha]
            hsva[0] = _fade_between(hsv1[0], hsv2[0], x, x_len)
            hsva[1] = _fade_between(hsv1[1], hsv2[1], x, x_len) * sat
            hsva[2] = _fade_between(hsv1[2], hsv2[2], x, x_len) * (val / 255)
            hsv[y][x] = hsva
    rgb = _hsv_to_rgb(hsv)
    return rgb


def _fade_between(start: float, end: float, current: float, max: float) -> float:
    return start + (end - start) * (current / max)


def _rainbowify2(arr):
    hsv = _rgb_to_hsv(arr)
    for x, a in enumerate(hsv[..., 0]):
        for y, b in enumerate(a):
            hsv[..., 0][x][y] = b + 0.3 * (x * y) * 0.0001
    rgb = _hsv_to_rgb(hsv)
    return rgb


def colorize(image, rgb) -> Image:
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    img = image.convert("RGBA")
    arr = np.array(img)
    new_img = Image.fromarray(_set_color(arr, rgb_to_hsv(rgb)), "RGBA")

    return new_img


def rotate_hue(image, rotation, match: Optional[ColorMatch] = None) -> Image:
    """
    Rotate the hue of PIL image `original` with the given
    `rotation` (hue within 0-360); returns another PIL image.
    """
    img = image.convert("RGBA")
    arr = np.array(img)
    new_img = Image.fromarray(_shift_hue(arr, rotation / 360., match), "RGBA")

    return new_img


def gradient(image, rgb1: str, rgb2: str) -> Image:
    img = image.convert("RGBA")
    arr = np.array(img)
    arr = _rainbowify1(arr, rgb_to_hsv(rgb1), rgb_to_hsv(rgb2))
    return Image.fromarray(arr, "RGBA")


def rgb_to_hsv(rgb: str) -> Tuple[float, float, float]:
    h = rgb.lstrip("#")
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(*rgb)


def rgb_to_hue(rgb: str) -> float:
    h = rgb.lstrip("#")
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    hue = colorsys.rgb_to_hsv(*rgb)[0] * 360
    return hue
