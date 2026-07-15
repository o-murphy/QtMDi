"""
Makes each Material Symbols weight/style variant register as its own,
distinct Qt font family.

All per-weight static instances (100..700, base) of a given style
(outlined/rounded/sharp) ship with the *same* typographic family name
(e.g. "Material Symbols Outlined 48pt"), differing only by subfamily
(Thin/Light/Regular/.../Bold). qtawesome.IconicFont.font() selects a
font by calling QFont.setFamily() alone, never setWeight()/setStyleName(),
so Qt's font matcher collapses all same-named weight variants onto a
single (usually Regular) face - the requested weight is silently ignored.

Appending the containing directory name (the weight bucket QtMDi already
uses to build its prefixes, see qtmdi._look_for_fonts) to the name-table
family fields makes every variant a unique Qt family, so setFamily()
resolves unambiguously to the intended weight.
"""

import os

from fontTools.ttLib import TTFont

from qtmdi import SYMBOLS_DIR

# name IDs that identify the font to the OS/Qt font matcher.
FAMILY_NAME_IDS = (1, 3, 4, 6, 16)


def _suffix_for(weight_dir: str) -> str:
    return weight_dir.capitalize()


def _already_patched(name_table, suffix: str) -> bool:
    record = name_table.getDebugName(16) or name_table.getDebugName(1)
    return bool(record) and record.endswith(suffix)


def fix_font(path: str, weight_dir: str) -> bool:
    suffix = _suffix_for(weight_dir)
    font = TTFont(path)
    name_table = font["name"]

    if _already_patched(name_table, suffix):
        return False

    for record in name_table.names:
        if record.nameID not in FAMILY_NAME_IDS:
            continue
        value = record.toUnicode()
        if record.nameID == 6:
            # PostScript name: no spaces allowed.
            value = f"{value}-{suffix}"
        else:
            value = f"{value} {suffix}"
        name_table.setName(
            value, record.nameID, record.platformID, record.platEncID, record.langID
        )

    font.save(path)
    return True


def main() -> None:
    changed = 0
    for root, _, files in os.walk(SYMBOLS_DIR):
        weight_dir = os.path.basename(root)
        for filename in files:
            if not filename.endswith(".ttf"):
                continue
            path = os.path.join(root, filename)
            if fix_font(path, weight_dir):
                changed += 1
                print(f"patched {path}")

    print(f"{changed} font(s) patched")


if __name__ == "__main__":
    main()
