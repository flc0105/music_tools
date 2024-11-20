import json
import os

from mutagen.flac import FLAC

def secure_filename(filename):
    for char in filename:
        if char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            filename = filename.replace(char, '_')
    return filename


for root, dirs, files in os.walk('.'):
    flac_files = [f for f in files if f.endswith('.flac')]
    for flac_file in flac_files:
        flac_path = os.path.join(root, flac_file)
        audio = FLAC(flac_path)
        date = audio.get('date', ['Unknown Date'])[0]
        date = date.replace('-', '.')
        album = audio.get('album', ['Unknown Album'])[0]
        dest_dir = secure_filename(f'{date} - {album}')
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, flac_file)
        if not os.path.exists(dest_file):
            os.rename(os.path.join(root, flac_file), dest_file)
