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

aac.tags.pop('rtng')
aac.tags['aART'] = '' # album artist
aac.tags['©ART'] = '' # artist
aac.tags['©day'] = '' # date
aac.tags['©nam'] = '' # title
if '©lyr' in aac.tags:
    aac.tags.pop('©lyr')
aac.tags.pop('©gen')
aac.save()
