import sys
import qtawesome
import qtmdi
from qtpy import QtWidgets


# pylint: disable=too-few-public-methods
class Example(QtWidgets.QMainWindow):
    """
    Example app
    """
    def __init__(self):
        super().__init__()
        self.lt = QtWidgets.QVBoxLayout(self)
        self.btn = QtWidgets.QToolButton(self)
        self.btn.setIcon(
            qtawesome.icon("mdi-rounded-700.home_filled"),
        )
        self.btn.setFixedSize(48, 48)
        self.btn.setIconSize(32, 32)
        self.lt.addWidget(self.btn)


def run():
    """
    Start the Example app and block until the process exits.
    """
    app = QtWidgets.QApplication()
    qtmdi.load(app)
    qtawesome.dark(app)
    w = Example()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
