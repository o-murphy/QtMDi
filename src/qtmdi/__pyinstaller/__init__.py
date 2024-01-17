"""
Entry points for PyInstaller
"""

import os


def get_hook_dirs():
    """returns hook dir"""
    return [os.path.dirname(__file__)]
