import sys
import qtawesome
from qtawesome.icon_browser import IconBrowser
from qtpy import QtWidgets

from qtmdi import load


def run():
    """
    Start the IconBrowser and block until the process exits.
    """
    app = QtWidgets.QApplication(sys.argv)
    load(app, lazy=False)  # the browser lists every icon, so nothing can stay lazy here
    qtawesome.dark(app)

    browser = IconBrowser()
    browser.setWindowTitle("QtMDi Icon Browser")
    browser._comboFont.setCurrentText("mdf")
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
