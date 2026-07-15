[![SWUbanner]][SWUdocs]

[SWUbanner]:
https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg
[SWUdocs]:
https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md

# QtMDi (Qt Material Design icons)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)
[![pypi version](https://img.shields.io/pypi/v/QtMDi)](https://pypi.org/project/QtMDi/)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/qtmdi)](https://pypi.org/project/QtMDi/)


*Copyright 2023 Yaroshenko Dmytro (https://github.com/o-murphy)*

### The extension for [QtAwesome](https://github.com/spyder-ide/qtawesome) with the latest variable icon fonts for Material Symbols
#### (Python 3, PySide, PyQt)

> [!NOTE]
> Fonts in this package automatically updated, so it will always have the latest icons from Google

> [!NOTE]
> The package is publishing to PyPi automatically, so it can have issues in some releases

> [!NOTE]
> The package uses [QtAwesome](https://github.com/spyder-ide/qtawesome) as it's backend,
> so it support all the feature provided by QtAwesome, for more [see the docs](https://github.com/spyder-ide/qtawesome/blob/master/README.md)

- [Installation](#installation)
- [Usage](#usage)
- [Supported Fonts](#supported-fonts)
- [Available Icons](#available-icons)
- [Development](#development)
- [Known issues](#known-issues)

## Installation

QtMDi is built on [QtAwesome](https://github.com/spyder-ide/qtawesome) and
[qtpy](https://github.com/spyder-industries/qtpy), which is just an
abstraction layer over Qt bindings - it doesn't ship a Qt binding itself,
so you need to install one (`PyQt5`, `PySide2`, `PyQt6` or `PySide6`)
alongside it:

```sh
pip install QtMDi PyQt6
```

Install the latest release from PyPi:
```sh
pip install QtMDi
```

Install the latest updated version from github:
```sh
pip install https://github.com/o-murphy/QtMDi
```

### Using `qtmdi-browser` as a standalone tool

If you just want to run the icon browser (see [Available Icons](#available-icons))
without installing QtMDi into a project, use `uv tool install` (or `pipx`)
with a Qt binding as an extra dependency:

```sh
uv tool install qtmdi --with pyqt6
# or
uv tool install qtmdi --with pyside6

qtmdi-browser
```

## Usage

### Supported Fonts
QtAwesome identifies icons by their prefix and their icon name, separated by a period (.) character.

The following prefixes are currently available to use:
* `mds` prefix has [Google material design icons](https://github.com/google/material-design-icons) symbols style
* `mdf` prefix has [Google material design icons](https://github.com/google/material-design-icons) variablefont style
* `si` prefix has [Simple Icons](https://github.com/simple-icons/simple-icons-font) brand/logo icons, e.g. `qtawesome.icon("si.github")`

### Example

#### Import qtawesome and qtmdi in your python file:

```python
import qtawesome
import qtmdi
```

#### Icon creation example
```python
# basic rounded
qtawesome.icon("mds-rounded-base.home")

# rounded with 700 width
qtawesome.icon("mds-rounded-700.home")

# rounded with 400 width
qtawesome.icon("mds-sharp-400.home")

# basic variablefont ttf based icon
qtawesome.icon("mdf-sharp.home")
```

#### Create an app

```python
from qtpy import QtWidgets

class Example(QtWidgets.QMainWindow):
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
```

#### Load extension on your app instance
```python
import sys
from qtpy import QtWidgets
import qtawesome
import qtmdi


# Create an app
class Example(QtWidgets.QMainWindow):
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
    app = QtWidgets.QApplication()
    
    # Load extension on your app instance
    qtmdi.load(app)
    
    qtawesome.dark(app)
    w = Example()
    w.show()
    sys.exit(app.exec_())
        
if __name__ == '__main__':    
    run()
```

> [!NOTE]
> `qtmdi.load(app)` is lazy by default: it only registers *which* fonts are
> available, and reads/loads the actual font file the first time one of its
> icons is requested through `qtawesome.icon(...)`. This keeps memory usage
> and startup time low when your app only ever uses a few styles/weights out
> of everything QtMDi ships.
>
> Pass `qtmdi.load(app, lazy=False)` to load every shipped font immediately
> instead (this is what `qtmdi-browser` does, since it needs to list every
> icon right away).
>
> If you know upfront exactly which fonts your app uses, restrict qtmdi to
> just those with `load_only`, e.g.
> `qtmdi.load(app, load_only={"mds-rounded-700", "mdf"})`. This works with
> both lazy (only those prefixes become loadable on demand) and
> `lazy=False` (only those prefixes get loaded immediately).

## Available Icons
To see available icons run qtmdi-browser in your terminal

```sh
qtmdi-browser
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and packaging.

Font binaries under `src/qtmdi/icons` and `src/qtmdi/brands` aren't
committed to git (they're fetched fresh at build/CI time to keep the repo
small) - after cloning, run the fetch scripts once to populate them
locally. `fetch_fonts.py` downloads the Material Symbols variable fonts
straight from Google's
[material-design-icons](https://github.com/google/material-design-icons)
repository and generates the per-weight static files with `fonttools`;
`fetch_brand_icons.py` downloads the Simple Icons font + metadata from its
[GitHub Releases](https://github.com/simple-icons/simple-icons-font/releases).
Neither needs `npm`/`node`/`woff2`:

```sh
# install dependencies (including dev tools)
uv sync

# fetch the fonts (one-time, or whenever you want the latest icons)
uv run python scripts/fetch_fonts.py
uv run python scripts/fetch_brand_icons.py
uv run python scripts/fix_font_families.py
uv run python scripts/create_symbols_charmap.py

# run the test suite
uv run pytest

# lint
uv run ruff check
uv run flake8 .

# launch the icon browser against your local checkout
uv run qtmdi-browser
```

Font binaries are refreshed automatically by the
[`symbols-update`](.github/workflows/symbols-update.yml) workflow (via
`scripts/fetch_fonts.py` and `scripts/fetch_brand_icons.py`), which also
fixes the Material Symbols fonts' internal family names so weight/style
selection resolves correctly in Qt (`scripts/fix_font_families.py`),
regenerates `icons/charmap.json` (`scripts/create_symbols_charmap.py`), and
writes `manifest.json` - a checksum of every font file, committed instead
of the binaries themselves, so the workflow can tell whether the fonts
actually changed and only cut a release when they did
(`scripts/write_font_manifest.py`). You normally shouldn't need to touch
any of these by hand.

## Known issues
* Filled icons not shown as expected
* `Grade` property currently unsupported
* `Optical size` property currently unsupported

## License
* MIT License. Copyright 2023 Yaroshenko Dmytro (https://github.com/o-murphy)
See the [LICENSE](LICENSE) file for details.

### Fonts bundled by QtMDi itself (`mdf`, `mds`, `si`)

- The [Google material design icons](https://github.com/google/material-design-icons) fonts (`mdf`, `mds`) are licensed under the [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). A copy of the license, and a notice describing the modifications QtMDi makes to the shipped font files, are included at [`src/qtmdi/licenses/Apache-2.0-material-design-icons.txt`](src/qtmdi/licenses/Apache-2.0-material-design-icons.txt) and [`src/qtmdi/licenses/NOTICE-material-design-icons.txt`](src/qtmdi/licenses/NOTICE-material-design-icons.txt) - both are packaged with every install.

- The [Simple Icons](https://github.com/simple-icons/simple-icons-font) font (`si`) and its icon data are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/); a copy is included at [`src/qtmdi/licenses/CC0-1.0-simple-icons.md`](src/qtmdi/licenses/CC0-1.0-simple-icons.md).

### Fonts available transitively through the QtAwesome dependency

QtMDi doesn't bundle the fonts below itself - they ship as part of the `qtawesome` package (a QtMDi dependency), which carries its own licensing for them; they're listed here only because QtMDi's `load()`/`qtawesome.icon()` gives you access to their prefixes too.

- The [QtAwesome](https://github.com/spyder-ide/qtawesome) licensed under the MIT License. Copyright 2015 - The Spyder development team.
See the [LICENSE](https://github.com/spyder-ide/qtawesome/blob/master/LICENSE.txt) file for details.

- The [Font Awesome](https://github.com/FortAwesome/Font-Awesome/blob/master/LICENSE.txt) and [Elusive Icons](http://elusiveicons.com/license/) fonts are licensed under the [SIL Open Font License](http://scripts.sil.org/OFL).

- The Phosphor font is licensed under the [MIT License](https://github.com/phosphor-icons/phosphor-icons/blob/master/LICENSE).

- The [Material Design Icons](https://github.com/Templarian/MaterialDesign/blob/master/LICENSE) font is licensed under the [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

- The Remix Icon font is licensed under the [Apache License Version 2.0](https://github.com/Remix-Design/remixicon/blob/master/License).

- Microsoft's Codicons are licensed under a [Creative Commons Attribution 4.0 International Public License](https://github.com/microsoft/vscode-codicons/blob/master/LICENSE).
