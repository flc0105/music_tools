#!/usr/bin/env python3
import os
import json

from mutagen import File
from mutagen.flac import Picture

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]

for file in files:
    flac = File(file)

    filename_without_extension = os.path.splitext(file)[0]

    data = flac.tags
    if not data:
        continue
    json_data = {key.lower(): value for key, value in data}
    json_filename = f"{filename_without_extension}.json"
    if not os.path.isfile(json_filename):
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=2)
        print(f"JSON metadata saved: {json_filename}")

    album = json_data.get('album')
    cover_filename = f'{album}.jpg'
    if not os.path.isfile(cover_filename):
        pictures = flac.pictures
        if not pictures:
            continue
        for p in pictures:
            if p.type == 3:
                with open(cover_filename, 'wb') as cover_file:
                    cover_file.write(p.data)
                print(f"Cover image saved: {cover_filename}")
                break
