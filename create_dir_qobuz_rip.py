import json
import os

import requests
from mutagen.flac import FLAC

years = {}


def get_spec(audio):
    sample_rate = audio.info.sample_rate / 1000
    bits_per_sample = audio.info.bits_per_sample
    if sample_rate.is_integer():
        sample_rate = int(sample_rate)
    return '{}-{}'.format(bits_per_sample, sample_rate)


def get_year(audio, key):
    if years.get(key):
        return years.get(key)
    year = audio.get('date')[0][:4]
    return year


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
        artist = audio.get('albumartist', ['Unknown Artist'])[0]
        album = audio.get('album', ['Unknown Album'])[0]
        key = secure_filename(f'{artist} - {album}')
        year = get_year(audio, key)
        fmt = 'FLAC'
        spec = get_spec(audio)
        info = secure_filename(f' ({year}) [Qobuz Rip] [{fmt} {spec}]')
        dest_dir = f'{key}{info}'
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        cover_dest = os.path.join(dest_dir, 'cover.jpg')
        if not os.path.exists(cover_dest):
            os.rename(os.path.join(root, 'cover.jpg'), cover_dest)
        dest_file = os.path.join(dest_dir, flac_file)
        if not os.path.exists(dest_file):
            os.rename(os.path.join(root, flac_file), dest_file)
