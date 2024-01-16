import os
import sys

from qtawesome.icon_browser import IconBrowser
from qtpy import QtWidgets

import qtawesome


SEARCH_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(SEARCH_DIR, 'font')
SYMBOLS_DIR = os.path.join(SEARCH_DIR, 'symbols')


_BUILT_IN_FONTS = (
    (
        "gmi",
        "MaterialIcons-Regular.ttf",
        "MaterialIcons-Regular-charmap.json",
    ),
    (
        "gmi-outlined",
        "MaterialIconsOutlined-Regular.otf",
        "MaterialIconsOutlined-Regular-charmap.json",
    ),
    (
        "gmi-round",
        "MaterialIconsRound-Regular.otf",
        "MaterialIconsRound-Regular-charmap.json",
    ),
    (
        "gmi-sharp",
        "MaterialIconsSharp-Regular.otf",
        "MaterialIconsSharp-Regular-charmap.json",
    ),
    (
        "gmi-2tone",
        "MaterialIconsTwoTone-Regular.otf",
        "MaterialIconsTwoTone-Regular-charmap.json",
    ),
)


def create_symbols_prefix(filename):
    try:
        return f"gms-{os.path.splitext(filename)[0].split('-')[-1]}"
    except Exception:
        return f"gms-other"


_BUILT_IN_SYMBOLS = [
    (
        create_symbols_prefix(filename),
        filename,
        "charmap.json",
    ) for filename in os.listdir(SYMBOLS_DIR) if filename.endswith(".ttf")
]

print(_BUILT_IN_SYMBOLS)

# _BUILT_IN_SYMBOLS = (
#     (
#         "gms-outlined",
#         "material-symbols-outlined.ttf",
#         "charmap.json",
#     ),
#     (
#         "gms-outlined",
#         "material-symbols-rounded.ttf",
#         "charmap.json",
#     ),
#     (
#         "gms-outlined",
#         "material-symbols-sharp.ttf",
#         "charmap.json",
#     )
# )


def load(app: QtWidgets.QApplication):
    if app == QtWidgets.QApplication.instance():

        for symbols in _BUILT_IN_SYMBOLS:
            qtawesome.load_font(*symbols, SYMBOLS_DIR)

        for font in _BUILT_IN_FONTS:
            qtawesome.load_font(*font, FONT_DIR)


def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication([])
    load(app)
    qtawesome.dark(app)

    browser = IconBrowser()
    browser._comboFont.setCurrentText("gmi")
    browser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
