# pylint: disable=invalid-name
"""
Hook for PyInstaller
collects package data if PyInstaller packaging requires celpy
"""

# pylint: disable=import-error
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('qtmdi')
