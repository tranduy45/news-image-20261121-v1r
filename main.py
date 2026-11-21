"""Entrypoint for news-image-20261121 v1r.

Renders the front page once, deterministically, and writes entry.png to
the output directory. The output directory comes from MAKEFUN_OUTPUT_DIR
when set, otherwise the repository root (this file's directory).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import render  # noqa: E402


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    os.makedirs(outdir, exist_ok=True)
    image, problems = render()
    if problems:
        for problem in problems:
            print("OVERFLOW:", problem, file=sys.stderr)
        sys.exit(1)
    path = os.path.join(outdir, "entry.png")
    image.save(path, format="PNG")
    print("wrote %s (%dx%d, %d bytes)"
          % (path, image.size[0], image.size[1], os.path.getsize(path)))


if __name__ == "__main__":
    main()
