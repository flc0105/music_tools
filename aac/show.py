#!/usr/bin/env python3
import json
import os
import sys

from mutagen import File

if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
aac = File(filename)
print(aac.tags.pprint())

os.system('pause')
