import unittest

from qtpy import QtWidgets
import qtawesome

from src import qtmdi


class TestIconCreate(unittest.TestCase):

    def test_create(self) -> None:
        app = QtWidgets.QApplication()
        qtmdi.load(app)

        with self.subTest("create gmi"):
            qtawesome.icon("gmi.search")

        with self.subTest("create gms"):
            qtawesome.icon("gmi.search")
