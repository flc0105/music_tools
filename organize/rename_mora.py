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
    filename = f'{trackno:03d}-{title}.flac'
    os.rename(file, filename)
    print(f'{os.path.basename(file)} -> {filename}')

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.m4a')]
for file in files:
    m4a = File(file)
    title = m4a.tags.get("©nam")[0]
    trackno = int(m4a.tags.get("trkn")[0][0])
    for char in title:
        if char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            title = title.replace(char, '_')
    filename = f'{trackno:03d}-{title}.m4a'
    os.rename(file, filename)
    print(f'{os.path.basename(file)} -> {filename}')
