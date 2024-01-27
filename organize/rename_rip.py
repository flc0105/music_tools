"""
Rename music files to track number and title
"""
import os

from mutagen import File

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]
for file in files:
    flac = File(file)
    title = flac.tags['title'][0]
    for char in title:
        if char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            title = title.replace(char, '_')
    trackno = int(flac.tags['tracknumber'][0])
    filename = f'{trackno:02d}-{title}.flac'
    os.rename(file, filename)
    print(f'{os.path.basename(file)} -> {filename}')
