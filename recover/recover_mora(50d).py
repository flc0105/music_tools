import json
import os
import sys

from mutagen.flac import FLAC

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]
for file in files:
    flac = FLAC(file)
    tags = flac.tags
    tags['ARTIST'] = tags['ARTIST']
    tags['TITLE'] = tags['TITLE']
    tags['ALBUM'] = tags['ALBUM']
    tags['ALBUMARTIST'] = tags['ALBUMARTIST']
    tags['GENRE'] = tags['GENRE']
    tags['GENRENUMBER'] = tags['GENRENUMBER']
    tags['DATE'] = tags['DATE']
    tags['COMPOSER'] = tags['COMPOSER']
    tags['DISCNUMBER'] = tags['DISCNUMBER']
    tags['TRACKNUMBER'] = tags['TRACKNUMBER']
    tags['COPYRIGHT'] = tags['COPYRIGHT']
    tags['ORGANIZATION'] = tags['ORGANIZATION']
    tags['COMMENT'] = tags['COMMENT']
    tags['PERFORMER'] = tags['PERFORMER']
    tags['MOOD'] = tags['MOOD']
    tags['45b1d925-1448-5784-b4da-b89901050a13'] = tags['45b1d925-1448-5784-b4da-b89901050a13']
    tags['be242671-3d48-5ac8-b762-7d2db4f584b8'] = tags['be242671-3d48-5ac8-b762-7d2db4f584b8']
    tags['ff8ca75f-2d68-52eb-85d6-1580486025a4'] = tags['ff8ca75f-2d68-52eb-85d6-1580486025a4']
    tags['93a74bea-ce97-5571-a56a-c5084dba9873'] = tags['93a74bea-ce97-5571-a56a-c5084dba9873']
    tags['8e90f26b-372a-5c8c-bb05-1ec0f36ee60c'] = tags['8e90f26b-372a-5c8c-bb05-1ec0f36ee60c']
    tags['07f42305-3c75-529c-ba48-09435e88980d'] = tags['07f42305-3c75-529c-ba48-09435e88980d']
    tags['50dbf5a2-f864-5c17-be00-c36dfd3df7b4'] = tags['50dbf5a2-f864-5c17-be00-c36dfd3df7b4']
    flac.save()
    print(f'Success: {file}')
