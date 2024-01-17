"""
Organize and classify music files
"""
import json
import os

from mutagen.flac import FLAC

years = {}


def get_spec(audio):
    sample_rate = audio.info.sample_rate / 1000
    bits_per_sample = audio.info.bits_per_sample
    if sample_rate.is_integer():
        sample_rate = int(sample_rate)
    return '{}-{}'.format(bits_per_sample, sample_rate)


def get_source(audio, key):
    try:
        if audio.tags.get('45b1d925-1448-5784-b4da-b89901050a13', [''])[0] == '10006001':
            return 'mora'
        elif audio.tags.get('comment', [''])[0].startswith('Brought to you by OTOTOY.JP'):
            return 'OTOTOY'
        elif audio.tags.get('description', [''])[0].startswith('Interprètes'):
            return 'qobuz'
        else:
            raise
    except:
        source = input(f'{key}：识别【音源】失败，请手动输入：')
        if not source:
            return 'Unknown Source'
        return source


def get_year(audio, key):
    if years.get(key):
        return years.get(key)
    try:
        source = get_source(audio, key)
        if source == 'mora':
            raise
        elif source == 'qobuz':
            year = audio.get('date')[0]
        elif source == 'OTOTOY':
            year = audio.get('year')[0]
        else:
            raise
    except:
        year = input(f'{key}：获取【年份】失败，请手动输入：')
        if not year:
            year = 'Unknown Year'
    years[key] = year
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
        source = get_source(audio, key)
        fmt = 'FLAC'
        spec = get_spec(audio)
        info = secure_filename(f' ({year}) [{source}] [{fmt} {spec}]')
        dest_dir = f'{key}{info}'
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, flac_file)
        if not os.path.exists(dest_file):
            os.rename(os.path.join(root, flac_file), dest_file)
