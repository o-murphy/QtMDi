"""Fetches the Simple Icons brand-logo font into src/qtmdi/brands.

simple-icons-font doesn't commit its built font to git - it's only
published via npm and GitHub Releases at release time - so this pulls the
release zip straight from GitHub (no npm/node required) and extracts the
font plus its slug/codepoint metadata, from which the charmap is built.
"""

import io
import json
import os
import urllib.request
import zipfile

from qtmdi import BRANDS_DIR

RELEASES_API = "https://api.github.com/repos/simple-icons/simple-icons-font/releases/latest"
REQUEST_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "QtMDi-fetch-brand-icons",
}


def _get(url: str) -> bytes:
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    with urllib.request.urlopen(request) as response:
        return response.read()


def _latest_release() -> dict:
    return json.loads(_get(RELEASES_API))


def _asset_url(release: dict, name: str) -> str:
    for asset in release["assets"]:
        if asset["name"] == name:
            return asset["browser_download_url"]
    raise RuntimeError(f"asset {name!r} not found in release {release['tag_name']}")


def main() -> None:
    release = _latest_release()
    version = release["tag_name"]
    zip_url = _asset_url(release, f"simple-icons-font-{version}.zip")
    archive = zipfile.ZipFile(io.BytesIO(_get(zip_url)))

    os.makedirs(BRANDS_DIR, exist_ok=True)

    with archive.open("font/SimpleIcons.ttf") as src:
        with open(os.path.join(BRANDS_DIR, "simple-icons.ttf"), "wb") as dst:
            dst.write(src.read())

    with archive.open("font/simple-icons.json") as fp:
        icons = json.load(fp)
    charmap = {icon["slug"]: f"0x{icon['code']}" for icon in icons}
    with open(os.path.join(BRANDS_DIR, "simple-icons-charmap.json"), "w", encoding="utf-8") as fp:
        json.dump(charmap, fp)

    print(f"Simple Icons {version}: {len(charmap)} icons written to {BRANDS_DIR}")


if __name__ == "__main__":
    main()
