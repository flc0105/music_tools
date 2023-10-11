import json
import os
import sys

from mutagen.flac import FLAC

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]
for file in files:
    flac = FLAC(file)
    tags = flac.tags
    tags['tracknumber'] = tags['tracknumber']
    tags['totaltracks'] = tags['totaltracks']
    tags['discnumber'] = tags['discnumber']
    tags['totaldiscs'] = tags['totaldiscs']
    tags['artist'] = tags['artist']
    tags['title'] = tags['title']
    tags['album'] = tags['album']
    tags['year'] = tags['year']
    tags['AlbumArtist'] = tags['AlbumArtist']
    tags['Album Artist'] = tags['Album Artist']
    tags['comment'] = tags['comment']
    if 'WAVEFORMATEXTENSIBLE_CHANNEL_MASK' in tags:
        tags['WAVEFORMATEXTENSIBLE_CHANNEL_MASK'] = tags['WAVEFORMATEXTENSIBLE_CHANNEL_MASK']
    flac.save()
    print(f'Success: {file}')
