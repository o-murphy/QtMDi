import sys
import qtawesome
import qtmdi
from qtpy import QtWidgets


class Example(QtWidgets.QMainWindow):
    """
    Example app
    """

    def __init__(self):
        super().__init__()
        self.lt = QtWidgets.QVBoxLayout(self)
        self.btn = QtWidgets.QToolButton(self)
        self.btn.setIcon(
            qtawesome.icon("mds-rounded-700.home"),
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


if __name__ == "__main__":
    run()
