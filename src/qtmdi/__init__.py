"""
# QtMDI (Qt Material Design Icons)
qtawesome extension with the latest variable icon fonts for Material Symbols (Python 3)
(C) 2023 Yaroshenko Dmytro (https://github.com/o-murphy)
"""


import os
import sys

from qtawesome.icon_browser import IconBrowser
from qtpy import QtWidgets

import qtawesome


__author__ = "o-murphy"
__copyright__ = ("(C) 2023 Yaroshenko Dmytro (https://github.com/o-murphy)",)

__credits__ = ["o-murphy"]
# __version__ = "1.0.0"


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
    """creates prefix for dynamic loaded symbol fonts"""
    try:
        return f"gms-{os.path.splitext(filename)[0].split('-')[-1]}"
    # pylint: disable=broad-exception-caught
    except Exception as exc:
        print(exc)
        return "gms-other"


_BUILT_IN_SYMBOLS = [
    (
        create_symbols_prefix(filename),
        filename,
        "charmap.json",
    ) for filename in os.listdir(SYMBOLS_DIR) if filename.endswith(".ttf")
]


def load(app: QtWidgets.QApplication):
    """loads fonts and symbols to current QApplication instance"""
    if app == QtWidgets.QApplication.instance():

        for symbols in _BUILT_IN_SYMBOLS:
            qtawesome.load_font(*symbols, SYMBOLS_DIR)

        for font in _BUILT_IN_FONTS:
            qtawesome.load_font(*font, FONT_DIR)


def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication()
    load(app)
    qtawesome.dark(app)

    browser = IconBrowser()
    browser.setWindowTitle('QtMDi Icon Browser')
    # pylint: disable=protected-access
    browser._comboFont.setCurrentText("gmi")
    browser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
