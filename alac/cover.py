#!/usr/bin/env python3
import json
import logging
import os
import re
import sys
import time
import subprocess

import requests
from mutagen import File
from mutagen.flac import Picture


json_file = next((f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')), None)
if not json_file:
    logger.error('Error: JSON file not found.')
    sys.exit(1)


f = open(json_file, 'rt', encoding='utf-8')
data = json.loads(f.read())
f.close()

album = data['data'][0]
tracks = data['data'][0]['relationships']['tracks']['data']

album_attributes = album.get('attributes', {})

w = album_attributes.get('artwork', {}).get('width')
h = album_attributes.get('artwork', {}).get('height')

cover_url = album_attributes.get('artwork', {}).get('url')
cover_url = cover_url.replace('{w}', str(w)).replace('{h}', str(h))

print(cover_url)

cover = 'cover.jpg'
if not os.path.exists(cover):
    response = requests.get(cover_url)
    with open(cover, 'wb') as f:
        f.write(response.content)