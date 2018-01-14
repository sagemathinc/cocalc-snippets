#!/usr/bin/env python3
# Import from the BSD licensed jupyter_boilerplate project

# The idea is to extract the data, but it is often incomplete, only parts are useful, different layout (too many subcategories) etc.

import os
import sys
import json
import yaml
from glob import iglob
from pprint import pprint

REPO = 'https://github.com/moble/jupyter_boilerplate.git'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(BASE_DIR, 'tmp')
INPUT_FILES = os.path.join(TMP, 'jupyter_boilerplate', 'snippets_submenus_python', '*.js')
OUT_YAML = os.path.join(BASE_DIR, 'src', 'python', 'boilerplate.yaml')

os.chdir(BASE_DIR)

# setup empty tmp directory
os.system('rm -rf {0}; mkdir {0}'.format(TMP))
os.chdir(TMP)

# fresh clone of repo
os.system('git clone --depth=1 --recurse-submodules {}'.format(REPO))
os.chdir(BASE_DIR)

# read files
for fn in iglob(INPUT_FILES):
    print(fn)
    if fn.endswith('scipy_constants.js'):
        data = open(fn).read().strip().splitlines()
        pprint(data)
        data[0] = '{'
        data[-1] = '}'
        data = json.loads('\n'.join(data))
        pprint(data)
        break