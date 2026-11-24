"""Copy the front-page image to the output directory.

Standard library only. Reads entry.png next to this file, checks it is
a whole PNG or JPEG of at most 1024 by 1024 pixels and at most 1 MiB,
copies it to MAKEFUN_OUTPUT_DIR (default /output), and verifies the
copy against the original with sha256.
"""

import hashlib
import os
import shutil
import struct
import sys

MAX_SIDE = 1024
MAX_SIZE = 1024 * 1024
NAME = "entry.png"


def die(message):
    print("error: " + message, file=sys.stderr)
    return 1


def png_size(data):
    if len(data) < 33:
        return None
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_size(data):
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(data):
            return None
        seg_len = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if seg_len < 2 or pos + 2 + seg_len > len(data):
            return None
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + seg_len
    return None


def run():
    base = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base, NAME)
    if not os.path.isfile(src):
        return die("missing " + NAME + " beside main.py (looked in "
                   + base + ")")
    try:
        with open(src, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        return die("cannot read " + NAME + ": " + str(exc))
    if not blob:
        return die(NAME + " is empty")
    if len(blob) > MAX_SIZE:
        return die(NAME + " is larger than 1 MiB")
    size = png_size(blob)
    kind = "PNG"
    if size is None:
        size = jpeg_size(blob)
        kind = "JPEG"
    if size is None:
        return die(NAME + " is not a PNG or JPEG image")
    width, height = size
    if width > MAX_SIDE or height > MAX_SIDE:
        return die("image is %dx%d, larger than 1024x1024"
                   % (width, height))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        return die("cannot create output dir: " + str(exc))
    dest = os.path.join(out_dir, NAME)
    try:
        shutil.copyfile(src, dest)
    except OSError as exc:
        return die("cannot write " + dest + ": " + str(exc))
    digest = hashlib.sha256(blob).hexdigest()
    try:
        with open(dest, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        return die("cannot read back " + dest + ": " + str(exc))
    if hashlib.sha256(written).hexdigest() != digest:
        return die("copy check failed: sha256 mismatch")
    print("copied %s %s (%dx%d, %d bytes, sha256 %s) to %s"
          % (NAME, kind, width, height, len(blob), digest, dest))
    return 0


if __name__ == "__main__":
    sys.exit(run())
