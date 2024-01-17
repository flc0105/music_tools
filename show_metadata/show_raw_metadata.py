#!/usr/bin/env python3
import json
import os
import sys

from mutagen.flac import FLAC

if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
flac = FLAC(filename)
print(flac.tags.pprint())

os.system('pause')
