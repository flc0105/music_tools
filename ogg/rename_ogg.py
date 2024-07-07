import os

from mutagen import File

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.ogg')]
for file in files:
    ogg = File(file)
    title = ogg.get("title")[0]
    trackno = int(ogg.get("tracknumber")[0])
    for char in title:
        if char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            title = title.replace(char, '_')
    filename = f'{trackno:02d}-{title}.ogg'
    os.rename(file, filename)
    print(f'{os.path.basename(file)} -> {filename}')
