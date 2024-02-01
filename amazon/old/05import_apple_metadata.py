#!/usr/bin/env python3
import json
import locale
import os
import subprocess
import sys

import requests
from mutagen import File
from mutagen.flac import Picture


def new_padding(padding):
    return 8192


json_file = next((f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')), None)
if not json_file:
    raise FileNotFoundError('JSON file not found')

print(f'Loading metadata from {json_file}')
f = open(json_file, 'rt', encoding='utf-8')
data = json.loads(f.read())
f.close()

album = data['data'][0]
tracks = data['data'][0]['relationships']['tracks']['data']

w = album.get('attributes', {}).get('artwork', {}).get('width')
h = album.get('attributes', {}).get('artwork', {}).get('height')

cover_url = album.get('attributes', {}).get('artwork', {}).get('url')
cover_url = cover_url.replace('{w}', str(w)).replace('{h}', str(h))

cover = 'cover.jpg'
if not os.path.exists(cover):
    print(f'Requesting album cover from {cover_url}')
    response = requests.get(cover_url)
    with open(cover, 'wb') as f:
        f.write(response.content)

files = sorted([f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')])
print('Files to process: {}'.format('\n'.join(files)))

if not len(tracks) == len(files):
    print('Error: Inconsistency between the number of files and the number of track info.')
    sys.exit(1)

for i, file in enumerate(files, start=1):
    flac = File(file)
    tags = flac.tags
    info = tracks[i - 1]

    if info.get('attributes', {}).get('trackNumber', '') != i:
        print('Error: Data anomaly, about to be withdrawn')
        sys.exit(1)

    album_attributes = album.get('attributes', {})
    track_attributes = info.get('attributes', {})


    tags['album'] = track_attributes.get('albumName', '')  # album
    tags['albumartist'] = album_attributes.get('artistName', '')  # albumartist
    tags['albumid'] = tags.get('albumid', '')
    tags['artist'] = track_attributes.get('artistName', '')  # artist
    tags['comment'] = tags.get('comment', '')
    tags['composer'] = track_attributes.get('composerName', '')  # composer
    tags['copyright'] = album_attributes.get('copyright', '')  # copyright
    tags['date'] = track_attributes.get('releaseDate', '')  # date
    tags['discnumber'] = tags.get('discnumber', '')
    tags['disctotal'] = tags.get('disctotal', '')
    tags['genre'] = track_attributes.get('genreNames', [''])[0]  # genre
    tags['isrc'] = track_attributes.get('isrc', '')  # isrc
    tags['label'] = album_attributes.get('recordLabel', '')  # label
    tags['title'] = track_attributes.get('name', '')  # title
    tags['trackid'] = tags.get('trackid', '')
    tags['tracknumber'] = tags.get('tracknumber', '')
    tags['tracktotal'] = tags.get('tracktotal', '')
    tags['upc'] = album_attributes.get('upc', '')  # upc

    picture = Picture()
    picture.type = 3
    picture.mime = 'image/jpeg'
    picture.data = open(cover, 'rb').read()
    flac.clear_pictures()
    flac.add_picture(picture)
    flac.save(padding=new_padding)
    print(f'Processed: {file}')

print('Processing complete.')
