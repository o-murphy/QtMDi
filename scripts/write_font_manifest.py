"""Writes a checksum manifest for every fetched font asset (Material
Symbols and Simple Icons).

The font binaries themselves are no longer committed to git (they're
fetched fresh at build/CI time, see scripts/fetch_fonts.py,
scripts/fetch_brand_icons.py and .gitignore). This small, git-tracked
manifest is what symbols-update.yml diffs against to decide whether
upstream fonts actually changed - added, removed, or modified - without
needing the (large) binaries in history to tell.
"""

import hashlib
import json
import os

from qtmdi import BRANDS_DIR, SEARCH_DIR, SYMBOLS_DIR

DEST = os.path.join(SEARCH_DIR, "manifest.json")
FONT_EXTENSIONS = (".ttf", ".otf")
SCAN_DIRS = (SYMBOLS_DIR, BRANDS_DIR)


def _hash_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest() -> dict:
    manifest = {}
    for base_dir in SCAN_DIRS:
        for root, _, files in os.walk(base_dir):
            for filename in files:
                if os.path.splitext(filename)[1] not in FONT_EXTENSIONS:
                    continue
                path = os.path.join(root, filename)
                rel = os.path.relpath(path, SEARCH_DIR).replace(os.sep, "/")
                manifest[rel] = _hash_file(path)
    return dict(sorted(manifest.items()))


def main() -> None:
    manifest = build_manifest()
    with open(DEST, "w", encoding="utf-8") as fp:
        json.dump(manifest, fp, indent=2)
        fp.write("\n")
    print(f"{len(manifest)} font(s) hashed into {DEST}")


if __name__ == "__main__":
    main()
