"""
# QtMDI (Qt Material Design Icons)
qtawesome extension with the latest variable icon fonts for Material Symbols (Python 3)
(C) 2023 Yaroshenko Dmytro (https://github.com/o-murphy)
"""

import os

import qtawesome
from qtpy import QtWidgets


SEARCH_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(SEARCH_DIR, "fonts")
SYMBOLS_DIR = os.path.join(SEARCH_DIR, "icons")

_BUILT_IN_FONTS = (
    (
        "mdf",
        "MaterialIcons-Regular.ttf",
        "MaterialIcons-Regular-charmap.json",
        FONT_DIR,
    ),
    (
        "mdf-outlined",
        "MaterialIconsOutlined-Regular.otf",
        "MaterialIconsOutlined-Regular-charmap.json",
        FONT_DIR,
    ),
    (
        "mdf-round",
        "MaterialIconsRound-Regular.otf",
        "MaterialIconsRound-Regular-charmap.json",
        FONT_DIR,
    ),
    (
        "mdf-sharp",
        "MaterialIconsSharp-Regular.otf",
        "MaterialIconsSharp-Regular-charmap.json",
        FONT_DIR,
    ),
    (
        "mdf-2tone",
        "MaterialIconsTwoTone-Regular.otf",
        "MaterialIconsTwoTone-Regular-charmap.json",
        FONT_DIR,
    ),
)

# prefix -> (ttf_filename, charmap_filename, directory), populated by _build_registry()
_REGISTRY = {}
_original_icon = None


def _create_symbols_prefix(filename):
    """creates prefix for dynamic loaded symbol fonts"""
    try:
        return f"mds-{os.path.splitext(filename)[0].split('-')[-1]}"
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
                fonts.append((prefix, file, "../charmap.json", root))
    return fonts


def _build_registry():
    """Enumerates every available font and its files without reading them."""
    if _REGISTRY:
        return
    for prefix, ttf_filename, charmap_filename, directory in (
        *_look_for_fonts(),
        *_BUILT_IN_FONTS,
    ):
        _REGISTRY[prefix] = (ttf_filename, charmap_filename, directory)


def _ensure_loaded(prefix):
    """Loads a single font on first use. No-op if already loaded or unknown."""
    if prefix not in _REGISTRY:
        return
    if prefix in qtawesome._instance().fontname:
        return
    qtawesome.load_font(prefix, *_REGISTRY[prefix])


def _iter_strings(value):
    """Recursively yields every string found in icon-name arguments/options,
    covering plain names, 'active'/'disabled'/'selected' kwargs and the
    per-glyph 'options' list used for icon stacks."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_strings(item)


def _lazy_icon(*names, **kwargs):
    """Drop-in replacement for qtawesome.icon() that loads a qtmdi font
    the first time its prefix is actually referenced, instead of eagerly
    loading every shipped font up front."""
    for value in (*names, kwargs):
        for text in _iter_strings(value):
            if "." in text:
                _ensure_loaded(text.split(".", 1)[0])
    return _original_icon(*names, **kwargs)


def load(app: QtWidgets.QApplication, lazy: bool = True):
    """Registers qtmdi fonts on the current QApplication.

    If lazy (the default), a font is only read from disk and registered
    with Qt the first time qtawesome.icon() is called with a matching
    prefix. Pass lazy=False to load every shipped font immediately instead,
    e.g. for the icon browser, which needs the complete charmap upfront.
    """
    global _original_icon
    if app != QtWidgets.QApplication.instance():
        return

    _build_registry()

    if lazy:
        if _original_icon is None:
            _original_icon = qtawesome.icon
            qtawesome.icon = _lazy_icon
    else:
        for prefix in _REGISTRY:
            _ensure_loaded(prefix)
