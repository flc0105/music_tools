#!/usr/bin/env python3
import os
import sys
from mutagen import File
from mutagen.mp4 import MP4, MP4Cover

def no_padding(info):
    # this will remove all padding
    return 0

# List of tags
tags = [
    '----:com.apple.itunes:ISRC',      # ISRC
    '----:com.apple.itunes:UPC',       # UPC
    'aART',                            # Albumartist
    'atID',                            # ArtistID
    'cmID',                            # ComposerId
    'cnID',                            # TrackId
    # 'covr',                            # CoverArt
    'cprt',                            # Copyright
    'desc',                            # Description
    'disk',                            # DiscNumber
    'geID',                            # GenreId
    'plID',                            # AlbumId
    'rtng',                            # ItunesAdvisory
    'sfID',                            # CountryId
    'stik',                            # MediaType
    'trkn',                            # TrackNumber
    'xid ',                            # Xid
    '©ART',                            # Artist
    '©alb',                            # Album
    '©day',                            # Date
    '©gen',                            # GenreName
    '©nam',                            # Title
    '©pub',                            # Publisher
    '©wrt',                            # Composer
]

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.m4a')]
for file in files:
    m4a = File(file)
    
    # Backup all tags
    tags_backup = {tag: m4a.tags[tag] for tag in m4a.tags}

    # Clear all tags
    m4a.delete()
    
    # Restore tags in specified order with explanations
    for tag in tags:
        if tag in tags_backup:
            m4a.tags[tag] = tags_backup[tag]


    # Embed album cover
    if os.path.isfile('cover.jpg'):
        with open("cover.jpg", "rb") as f:
            m4a["covr"] = [
                MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]
    else:
        print('No cover found.')


    # Save the file
    m4a.save(padding=no_padding)
