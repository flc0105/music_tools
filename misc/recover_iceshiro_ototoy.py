import json
import os
import sys

from mutagen.flac import FLAC

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]
for file in files:
    flac = FLAC(file)
    tags = flac.tags
    tags['tracknumber'] = '5/5'
    tags['totaltracks'] = '5'
    tags['discnumber'] = '1/1'
    tags['totaldiscs'] = '1'
    tags['year'] = '2018'
    tags['Album Artist'] = tags['AlbumArtist']
    tags['title'] = '約束 (feat. 花咲なつみ)'
    tags['artist'] = '瀬名航'

    flac.pop('date')
    flac.pop('genre')
    flac.pop('tracktotal')
    
    flac.save()
    print(f'Success: {file}')
