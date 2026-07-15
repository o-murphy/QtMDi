#!/usr/bin/env bash
# Fetches the latest Material Symbols fonts into src/qtmdi/icons and
# processes them (fixes font-family metadata, regenerates the charmap and
# checksum manifest). Font binaries aren't committed to git (see
# .gitignore) - this script is what CI (symbols-update.yml,
# python-publish.yml) and contributors run to (re)populate them locally.
#
# Requires: npm, sudo apt (for woff2), uv.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

npm init -y >/dev/null
npm install material-symbols@latest
npm install @material-symbols/font-100@latest
npm install @material-symbols/font-200@latest
npm install @material-symbols/font-300@latest
npm install @material-symbols/font-400@latest
npm install @material-symbols/font-500@latest
npm install @material-symbols/font-600@latest
npm install @material-symbols/font-700@latest

if ! command -v woff2_decompress >/dev/null 2>&1; then
  sudo apt-get install -y woff2
fi

find ./node_modules -type f -name "*.woff2" -print0 | while IFS= read -r -d '' file; do
  woff2_decompress "$file"
done

mkdir -p ./src/qtmdi/icons/base
mkdir -p ./src/qtmdi/icons/100
mkdir -p ./src/qtmdi/icons/200
mkdir -p ./src/qtmdi/icons/300
mkdir -p ./src/qtmdi/icons/400
mkdir -p ./src/qtmdi/icons/500
mkdir -p ./src/qtmdi/icons/600
mkdir -p ./src/qtmdi/icons/700
cp ./node_modules/material-symbols/*.ttf ./src/qtmdi/icons/base
cp ./node_modules/@material-symbols/font-100/*.ttf ./src/qtmdi/icons/100
cp ./node_modules/@material-symbols/font-200/*.ttf ./src/qtmdi/icons/200
cp ./node_modules/@material-symbols/font-300/*.ttf ./src/qtmdi/icons/300
cp ./node_modules/@material-symbols/font-400/*.ttf ./src/qtmdi/icons/400
cp ./node_modules/@material-symbols/font-500/*.ttf ./src/qtmdi/icons/500
cp ./node_modules/@material-symbols/font-600/*.ttf ./src/qtmdi/icons/600
cp ./node_modules/@material-symbols/font-700/*.ttf ./src/qtmdi/icons/700

uv run python scripts/fix_font_families.py
uv run python scripts/create_symbols_charmap.py
uv run python scripts/write_font_manifest.py
