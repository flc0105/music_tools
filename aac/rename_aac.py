import os

from mutagen import File

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.m4a')]
for file in files:
    m4a = File(file)
    title = m4a.tags.get("©nam")[0]
    trackno = int(m4a.tags.get("trkn")[0][0])
    for char in title:
        if char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            title = title.replace(char, '_')
    filename = f'{trackno:02d}-{title}.m4a'
    os.rename(file, filename)
    print(f'{os.path.basename(file)} -> {filename}')
