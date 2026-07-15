"""Fetches the latest Material Symbols fonts into src/qtmdi/icons.

Downloads the variable fonts directly from Google's own
google/material-design-icons repository - the source the various npm
packages (material-symbols, @material-symbols/font-*) repackage - and
instantiates the per-weight static files locally with fontTools instead of
depending on npm/node/woff2. No non-Python tooling required.
"""

import io
import os
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from qtmdi import SYMBOLS_DIR

STYLES = ("Outlined", "Rounded", "Sharp")
WEIGHTS = (100, 200, 300, 400, 500, 600, 700)
OPTICAL_SIZE = 48
WEIGHT_NAMES = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
}

RAW_URL = (
    "https://raw.githubusercontent.com/google/material-design-icons/master/"
    "variablefont/MaterialSymbols{style}%5BFILL%2CGRAD%2Copsz%2Cwght%5D.ttf"
)


def _download(style: str) -> bytes:
    with urllib.request.urlopen(RAW_URL.format(style=style)) as response:
        return response.read()


def _set_subfamily_name(font: TTFont, weight: int) -> None:
    weight_name = WEIGHT_NAMES[weight]
    name_table = font["name"]
    for name_id in (2, 17):
        for record in name_table.names:
            if record.nameID == name_id:
                name_table.setName(
                    weight_name, name_id, record.platformID, record.platEncID, record.langID
                )


def process_style(style: str) -> None:
    filename = f"material-symbols-{style.lower()}.ttf"
    data = _download(style)

    base_dir = os.path.join(SYMBOLS_DIR, "base")
    os.makedirs(base_dir, exist_ok=True)
    with open(os.path.join(base_dir, filename), "wb") as fp:
        fp.write(data)

    for weight in WEIGHTS:
        font = TTFont(io.BytesIO(data))
        instance = instancer.instantiateVariableFont(
            font, {"wght": weight, "opsz": OPTICAL_SIZE, "GRAD": 0}, inplace=True
        )
        _set_subfamily_name(instance, weight)

        dest_dir = os.path.join(SYMBOLS_DIR, str(weight))
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, filename)
        instance.save(dest)
        print(f"wrote {dest}")


def main() -> None:
    for style in STYLES:
        process_style(style)


if __name__ == "__main__":
    main()
