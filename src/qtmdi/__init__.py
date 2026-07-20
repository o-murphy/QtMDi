"""
# QtMDI (Qt Material Design Icons)
qtawesome extension with the latest variable icon fonts for Material Symbols (Python 3)
(C) 2023 Yaroshenko Dmytro (https://github.com/o-murphy)
"""

from __future__ import annotations

import os
import typing

# qtawesome/qtpy are imported lazily (inside the functions that need them),
# not here at module scope: importing qtmdi just for its path constants
# (as the font-fetch scripts under scripts/ do) must not require a Qt
# binding or its native libraries (e.g. libEGL) to be installed.
if typing.TYPE_CHECKING:
    from qtpy import QtWidgets


SEARCH_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(SEARCH_DIR, "fonts")
SYMBOLS_DIR = os.path.join(SEARCH_DIR, "icons")
BRANDS_DIR = os.path.join(SEARCH_DIR, "brands")

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

_BRAND_FONTS = (
    (
        "si",
        "simple-icons.ttf",
        "simple-icons-charmap.json",
        BRANDS_DIR,
    ),
)

# prefix -> (ttf_filename, charmap_filename, directory), populated by _build_registry()
_REGISTRY = {}
_original_icon = None
_original_font = None
_original_charmap = None
# None means "no restriction"; otherwise the only prefixes load() will act on.
_ALLOWED_PREFIXES = None


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
        *_BRAND_FONTS,
    ):
        _REGISTRY[prefix] = (ttf_filename, charmap_filename, directory)


def _ensure_loaded(prefix):
    """Loads a single font on first use. No-op if already loaded, unknown,
    or excluded by a prior load_only restriction."""
    if prefix not in _REGISTRY:
        return
    if _ALLOWED_PREFIXES is not None and prefix not in _ALLOWED_PREFIXES:
        return
    import qtawesome

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


def _lazy_font(prefix, size):
    """Drop-in replacement for qtawesome.font(), see _lazy_icon."""
    _ensure_loaded(prefix)
    return _original_font(prefix, size)


def _lazy_charmap(prefixed_name):
    """Drop-in replacement for qtawesome.charmap(), see _lazy_icon."""
    _ensure_loaded(prefixed_name.split(".", 1)[0])
    return _original_charmap(prefixed_name)


def _install_hooks():
    """Wraps qtawesome's icon/font/charmap lookups so a qtmdi font gets
    registered the first time its prefix is actually referenced, without
    requiring an explicit load() call. Idempotent - safe to call again
    (e.g. from load()) once hooks are already installed."""
    global _original_icon, _original_font, _original_charmap
    import qtawesome

    _build_registry()

    if _original_icon is None:
        _original_icon = qtawesome.icon
        qtawesome.icon = _lazy_icon
    if _original_font is None:
        _original_font = qtawesome.font
        qtawesome.font = _lazy_font
    if _original_charmap is None:
        _original_charmap = qtawesome.charmap
        qtawesome.charmap = _lazy_charmap


def load(app: QtWidgets.QApplication, lazy: bool = True, load_only: set = None):
    """Registers qtmdi fonts on the current QApplication.

    Note that qtawesome.icon()/font()/charmap() already lazily pick up
    qtmdi fonts as soon as qtmdi is imported, with no call to load()
    required. Call load() when you need one of:

    - load_only: restricts which prefixes qtmdi will ever touch (e.g.
      {"mds-rounded-700", "mdf"}), whether loading lazily or eagerly -
      handy when you know upfront exactly which fonts your app uses and
      want to skip registering/loading the rest entirely. Calling load()
      again with load_only=None (the default) lifts any previously set
      restriction.
    - lazy=False: loads every allowed font immediately instead of waiting
      for first use, e.g. for the icon browser, which needs the complete
      charmap upfront.
    """
    global _ALLOWED_PREFIXES
    from qtpy import QtWidgets

    if app != QtWidgets.QApplication.instance():
        return

    _install_hooks()

    if load_only is None:
        _ALLOWED_PREFIXES = None
    elif _ALLOWED_PREFIXES is None:
        _ALLOWED_PREFIXES = set(load_only)
    else:
        _ALLOWED_PREFIXES |= set(load_only)

    if not lazy:
        allowed = _REGISTRY if _ALLOWED_PREFIXES is None else _ALLOWED_PREFIXES
        for prefix in allowed:
            _ensure_loaded(prefix)


try:
    # Best-effort: install the lazy hooks as soon as qtmdi is imported, so
    # qtawesome.icon("mds-...")/font()/charmap() work without an explicit
    # load() call. qtawesome/qtpy are hard dependencies of this package,
    # but the actual Qt binding (PyQt/PySide) is a separate, optional
    # native dependency - scripts that only need qtmdi's path constants
    # (e.g. scripts/fetch_fonts.py) must keep working without one
    # installed, so any failure here (missing/broken binding) is silently
    # ignored; load() remains available to install the hooks explicitly.
    _install_hooks()
except Exception:
    pass
