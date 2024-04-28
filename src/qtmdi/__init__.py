"""
# QtMDI (Qt Material Design Icons)
qtawesome extension with the latest variable icon fonts for Material Symbols (Python 3)
(C) 2023 Yaroshenko Dmytro (https://github.com/o-murphy)
"""

import os
import sys

import qtawesome
from qtawesome.icon_browser import IconBrowser
from qtpy import QtWidgets


SEARCH_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(SEARCH_DIR, 'fonts')
SYMBOLS_DIR = os.path.join(SEARCH_DIR, 'icons')

_BUILT_IN_FONTS = (
    (
        "mdf",
        "MaterialIcons-Regular.ttf",
        "MaterialIcons-Regular-charmap.json",
    ),
    (
        "mdf-outlined",
        "MaterialIconsOutlined-Regular.otf",
        "MaterialIconsOutlined-Regular-charmap.json",
    ),
    (
        "mdf-round",
        "MaterialIconsRound-Regular.otf",
        "MaterialIconsRound-Regular-charmap.json",
    ),
    (
        "mdf-sharp",
        "MaterialIconsSharp-Regular.otf",
        "MaterialIconsSharp-Regular-charmap.json",
    ),
    (
        "mdf-2tone",
        "MaterialIconsTwoTone-Regular.otf",
        "MaterialIconsTwoTone-Regular-charmap.json",
    ),
)


def _create_symbols_prefix(filename):
    """creates prefix for dynamic loaded symbol fonts"""
    try:
        return f"mds-{os.path.splitext(filename)[0].split('-')[-1]}"
    # pylint: disable=broad-exception-caught
    except Exception as exc:
        print(exc)
        return "mds-other"


def _look_for_fonts():
    fonts = []
    for root, _, files in os.walk(SYMBOLS_DIR):
        path = root.split(os.sep)
        for file in files:
            if os.path.splitext(file)[1] == ".ttf":
                # filepath = os.path.join(root, file)
                prefix = f"{_create_symbols_prefix(file)}-{path[-1]}"
                fonts.append(
                    (prefix, file, "../charmap.json", root)
                )
    return fonts


def load(app: QtWidgets.QApplication):
    """loads fonts and symbols to current QApplication instance"""
    if app == QtWidgets.QApplication.instance():

        for symbols in _look_for_fonts():
            qtawesome.load_font(*symbols)

        for font in _BUILT_IN_FONTS:
            qtawesome.load_font(*font, FONT_DIR)
def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication(sys.argv)
    load(app)
    qtawesome.dark(app)

    browser = IconBrowser()
    browser.setWindowTitle('QtMDi Icon Browser')
    # pylint: disable=protected-access
    browser._comboFont.setCurrentText("mdf")
    browser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
