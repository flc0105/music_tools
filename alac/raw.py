#!/usr/bin/env python3
import os
import sys
from mutagen import File

if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
aac = File(filename)


print(vars(aac.info))

for key, value in aac.tags.items():
    if key == 'covr':
        value = type(value[0])
    print(f"{key}={value}")

os.system('pause')
