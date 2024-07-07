#!/usr/bin/env python3
import os
import sys
from mutagen import File

if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
aac = File(filename)

for key, value in aac.tags.items():
    if key == 'covr':
        value = 'Image'
    print(f"{key}={value}")

sorted_dict = {key: ('Image' if key == 'covr' else aac.tags[key]) for key in sorted(aac.tags)}


for key, value in sorted_dict.items():
    print(f"{key}={value}")

os.system('pause')
