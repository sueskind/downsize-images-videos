import os

import piexif
from PIL import Image

from .utils import log, format_size


def convert_image(in_path, out_path, filename, quality, max_dim, overwrite):
    if not overwrite and os.path.exists(out_path):
        return 0, 0

    try:
        in_size = os.path.getsize(in_path)
        img = Image.open(in_path)
        exif = piexif.load(img.info["exif"])
        if max(img.size) > max_dim:
            new_size = [int(s * max_dim / max(img.size)) for s in img.size]
            img = img.resize(tuple(new_size), Image.LANCZOS)
        if img.mode == "RGBA":
            background = Image.new(img.mode[:-1], img.size, "white")
            background.paste(img, img.split()[-1])
            img = background
        img.save(out_path, optimize=True, quality=quality, exif=piexif.dump(exif))

        out_size = os.path.getsize(out_path)
        log(f"Converted {filename} {format_size(in_size)} -> {format_size(out_size)} ({out_size / in_size:.2%})")

        return in_size, out_size

    except Exception:
        log(f"ERROR on {in_path}")
        return 0, 0
