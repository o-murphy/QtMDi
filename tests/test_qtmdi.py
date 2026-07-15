import sys
import unittest

from qtpy import QtWidgets
import qtawesome

from src import qtmdi


class TestIconCreate(unittest.TestCase):
    def test_create(self) -> None:
        app = QtWidgets.QApplication(sys.argv)
        qtmdi.load(app)

        with self.subTest("create gmi"):
            qtawesome.icon("mdf.search")

        with self.subTest("create gms"):
            qtawesome.icon("mds-outlined-base.search")
