"""
Rewriting music file metadata with iTunes data (am.json)
"""
import json
import locale
import os
import subprocess
import sys

import requests
from mutagen import File
from mutagen.flac import Picture


def new_padding():
    return 8192


f = open('am.json', 'rt', encoding='utf-8')
data = json.loads(f.read())
f.close()
album = data['data'][0]
tracks = data['data'][0]['relationships']['tracks']['data']

p = subprocess.run('metaflac --remove-all --dont-use-padding *.flac', capture_output=True, check=True)
stdout = str(p.stdout.strip(), locale.getdefaultlocale()[1])
print(stdout)

w = album.get('attributes', {}).get('artwork', {}).get('width')
h = album.get('attributes', {}).get('artwork', {}).get('height')

cover_url = album.get('attributes', {}).get('artwork', {}).get('url')
cover_url = cover_url.replace('{w}', str(w)).replace('{h}', str(h))

cover = 'cover.jpg'

if not os.path.exists(cover):
    response = requests.get(cover_url)
    with open(cover, 'wb') as f:
        f.write(response.content)

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]

if not len(tracks) == len(files):
    print('Error: Inconsistency between the number of files and the number of track info.')
    sys.exit(1)

max_discnumber = 0

for track in tracks:
    discnumber = track.get('attributes').get('discNumber', 0)
    if discnumber > max_discnumber:
        max_discnumber = discnumber

for i, file in enumerate(files, start=1):
    flac = File(file)
    flac.add_tags()
    tags = flac.tags
    info = tracks[i - 1]

    if info.get('attributes', {}).get('trackNumber', '') != i:
        print('Error: Data anomaly, about to be withdrawn')
        sys.exit(1)

    tags['album'] = info.get('attributes', {}).get('albumName', '')
    tags['albumartist'] = album.get('attributes', {}).get('artistName', '')
    tags['albumid'] = album.get('id', '')
    tags['artist'] = info.get('attributes', {}).get('artistName', '')
    tags['audiolocale'] = info.get('attributes', {}).get('audioLocale', '')
    tags['comment'] = album.get('attributes', {}).get('url', '')
    tags['composer'] = info.get('attributes', {}).get('composerName', '')
    tags['copyright'] = album.get('attributes', {}).get('copyright', '')
    tags['date'] = info.get('attributes', {}).get('releaseDate', '')
    tags['discnumber'] = str(info.get('attributes').get('discNumber', ''))
    tags['disctotal'] = '1'
    tags['genre'] = info.get('attributes', {}).get('genreNames', [''])[0]
    tags['isrc'] = info.get('attributes', {}).get('isrc', '')
    tags['label'] = album.get('attributes', {}).get('recordLabel', '')
    tags['title'] = info.get('attributes', {}).get('name', '')
    tags['trackid'] = info.get('id', '')
    tags['tracknumber'] = str(info.get('attributes', {}).get('trackNumber', ''))
    tags['tracktotal'] = str(album.get('attributes', {}).get('trackCount', ''))
    tags['upc'] = album.get('attributes', {}).get('upc', '')

    picture = Picture()
    picture.type = 3
    picture.mime = 'image/jpeg'
    picture.data = open(cover, 'rb').read()
    flac.clear_pictures()
    flac.add_picture(picture)
    flac.save(padding=new_padding)
