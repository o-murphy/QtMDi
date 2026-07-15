"""Regenerates icons/charmap.json from the currently shipped Material Symbols font.

Unlike the built-in fonts (see create_charmap.py), the Material Symbols npm
packages ship no *.codepoints file. The glyph names Google assigns (e.g.
"search") are baked into the font's own post table though, so the charmap
can always be rebuilt straight from whichever font is on disk - no external
source needed, and it stays in sync every time the fonts are updated.
"""

import json
import os

from fontTools.ttLib import TTFont

from qtmdi import SYMBOLS_DIR

# Any style/weight has the same icon names as the rest; 400 (Regular) is
# always present and is the smallest file per style.
SOURCE_FONT = os.path.join(SYMBOLS_DIR, "400", "material-symbols-outlined.ttf")
DEST = os.path.join(SYMBOLS_DIR, "charmap.json")


def build_charmap(font_path: str) -> dict:
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    charmap = {}
    for codepoint, name in sorted(cmap.items()):
        if codepoint < 0xE000 or "." in name:
            continue
        # PostScript glyph names can't start with a digit, so Google's build
        # prefixes those with "_" (e.g. "_9k_plus"); the public icon name -
        # the one used in Google's own docs/CSS - drops that prefix ("9k_plus").
        if name.startswith("_") and name[1:2].isdigit():
            name = name[1:]
        if name in charmap:
            continue  # keep the lowest codepoint when a name has aliases
        charmap[name] = f"0x{codepoint:x}"
    return charmap


def main() -> None:
    charmap = build_charmap(SOURCE_FONT)
    with open(DEST, "w", encoding="utf-8") as fp:
        json.dump(charmap, fp)
    print(f"{len(charmap)} icon names written to {DEST}")


if __name__ == "__main__":
    main()
