"""Creates a *-charmap.json files for built-in fonts"""

import os
import re
import json
from qtmdi import FONT_DIR  # pylint: disable=import-error


REGEX_SEARCH = r'(\w+) ([a-f\d]+)'

codepoints_files = [file for file in os.listdir(FONT_DIR) if file.endswith('.codepoints')]
for filename in codepoints_files:
    filepath = os.path.join(FONT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as fp:
        content = fp.read()

    output = dict((key, f"0x{value}") for key, value in re.findall(REGEX_SEARCH, content))
    dst = os.path.join(FONT_DIR, os.path.splitext(filename)[0]) + '-charmap.json'
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(output, fp)
