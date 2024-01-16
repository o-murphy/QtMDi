import os
import sys

from qtawesome.icon_browser import IconBrowser
from qtpy import QtWidgets

import qtawesome

FONT_DIR = os.path.join(os.path.dirname(__file__), 'font')


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
    )
)


def load(app: QtWidgets.QApplication):
    if app == QtWidgets.QApplication.instance():

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
