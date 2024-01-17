"""
Hook for PyInstaller
collects package data if PyInstaller packaging requires celpy
"""

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('qtmdi')
