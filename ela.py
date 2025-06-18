from PIL import Image, ImageChops
import os

def ela_image(path: str, quality: int = 90, scale: int = 10) -> Image.Image:
    """Perform Error Level Analysis and return the amplified difference image.

    Parameters
    ----------
    path: str
        Path to the input image.
    quality: int, optional
        JPEG quality used when recompressing the image.
    scale: int, optional
        Factor used to amplify the pixel differences.
    """
    temp = "ela_temp.jpg"
    original = Image.open(path)
    try:
        original.save(temp, "JPEG", quality=quality)
        temporary = Image.open(temp)
        diff = ImageChops.difference(original, temporary)
    except Exception:
        original.convert("RGB").save(temp, "JPEG", quality=quality)
        temporary = Image.open(temp)
        diff = ImageChops.difference(original.convert("RGB"), temporary)

    d = diff.load()
    width, height = diff.size
    for x in range(width):
        for y in range(height):
            # In the original notebook each pixel value was printed, which led
            # to huge output and slow execution. We remove that statement and
            # simply scale the difference value.
            d[x, y] = tuple(k * scale for k in d[x, y])

    os.remove(temp)
    return diff
