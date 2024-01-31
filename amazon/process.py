#!/usr/bin/env python3
import json
import logging
import os
import re
import sys
import time
import subprocess

import requests
from mutagen import File
from mutagen.flac import Picture


def get_logger():
    # 创建日志记录器
    logger = logging.getLogger()
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    # 创建控制台处理器和文件处理器
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('process.log')
    # 配置控制台处理器和文件处理器的日志级别
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)
    # 创建日志记录的格式
    log_format = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # 将格式应用于控制台处理器和文件处理器
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)
    # 将处理器添加到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


# 获取日志记录器
logger = get_logger()

json_file = next((f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')), None)
if not json_file:
    logger.error('JSON file not found.')
    raise FileNotFoundError('JSON file not found.')

logger.info('---------- Step 1: Backup original tags ----------')

files = sorted([f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')])

logger.info('Files to be processed: \n{}'.format('\n'.join(files)))

original_tags = []

for file in files:
    flac = File(file)
    data = flac.tags
    if not data:
        continue
    json_data = {key.lower(): value for key, value in data}
    original_tags.append(json_data)

logger.info('Tags backup complete: \n{}'.format(original_tags))

logger.info('---------- Step 2: Remove metadata ----------')
try:
    p = subprocess.run('metaflac --remove-all --dont-use-padding *.flac', shell=True, check=True)  # capture_output=True
    logger.info('Processing completed.')
except subprocess.CalledProcessError as e:
    logger.error('Processing failure.')
    raise

logger.info('---------- Step 3: Remove empty samples ----------')

skip = {
    44.1: '286',
    48.0: '312',
    96.0: '624',
    192.0: '1248'
}

for file in files:
    flac = File(file)
    info = flac.info
    sample_rate = info.sample_rate / 1000
    skip_value = skip.get(sample_rate, 'N/A')
    logger.info(
        '{} has a sample rate of {:.1f} kHz. Skipping the first {} samples.'.format(file, sample_rate, skip_value))

    command = [
        'flac',
        '-5',
        '--skip',
        skip_value,
        '--no-seektable',
        f'"{file}"',
        '-f'
    ]
    logger.info(f"Executing command: {' '.join(command)}")

    try:
        p = subprocess.run(' '.join(command), shell=True, check=True)  # capture_output=True
        logger.info(f'Processing completed: {file}')
    except subprocess.CalledProcessError as e:  # e.stderr.decode()
        logger.error(f'Processing failed: {file}')
        raise

logger.info('Processing completed.')

logger.info('---------- Step 4: Add tags ----------')


def new_padding(padding):
    return 8192


logger.info(f'Loading metadata from {json_file}')
f = open(json_file, 'rt', encoding='utf-8')
data = json.loads(f.read())
f.close()

album = data['data'][0]
tracks = data['data'][0]['relationships']['tracks']['data']

album_attributes = album.get('attributes', {})

w = album_attributes.get('artwork', {}).get('width')
h = album_attributes.get('artwork', {}).get('height')

cover_url = album_attributes.get('artwork', {}).get('url')
cover_url = cover_url.replace('{w}', str(w)).replace('{h}', str(h))

cover = 'cover.jpg'
if not os.path.exists(cover):
    logger.info(f'Requesting album cover from {cover_url}')
    response = requests.get(cover_url)
    with open(cover, 'wb') as f:
        f.write(response.content)

files = sorted([f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')])
logger.info('Files to process: \n{}'.format('\n'.join(files)))

if not len(tracks) == len(files):
    logger.error('Error: Inconsistency between the number of files and the number of track info.')
    sys.exit(1)

for i, file in enumerate(files, start=1):
    flac = File(file)
    tags = flac.tags
    info = tracks[i - 1]
    track_original_tags = original_tags[i - 1]

    if info.get('attributes', {}).get('trackNumber', '') != i:
        logger.error('Error: Data anomaly, about to be withdrawn')
        sys.exit(1)

    track_attributes = info.get('attributes', {})

    if track_attributes.get('isrc', '') != track_original_tags.get('isrc', ''):
        logger.error('Error: isrc match failed.')
        sys.exit(1)

    album_name = album_attributes.get('name', '')
    if album_name.endswith(" - EP"):
        release_type = "EP"
    elif album_name.endswith(" - Single"):
        release_type = "Single"
    else:
        release_type = "Album"

    tags['album'] = album_attributes.get('name', '').replace(' - Single', '').replace(' - EP', '').strip()
    tags['albumartist'] = album_attributes.get('artistName', '')
    tags['artist'] = track_attributes.get('artistName', '')
    tags['audiolocale'] = track_attributes.get('audioLocale', '')
    tags['comment'] = track_original_tags.get('comment', '')
    tags['composer'] = track_attributes.get('composerName', '')
    tags['copyright'] = album_attributes.get('copyright', '')
    tags['date'] = track_attributes.get('releaseDate', '')
    tags['discnumber'] = track_original_tags.get('discnumber', '')
    tags['disctotal'] = track_original_tags.get('disctotal', '')
    tags['genre'] = track_attributes.get('genreNames', [''])[0]
    tags['isrc'] = track_attributes.get('isrc', '')
    tags['label'] = album_attributes.get('recordLabel', '')
    tags['releasetype'] = release_type
    tags['title'] = track_attributes.get('name', '')
    tags['tracknumber'] = track_original_tags.get('tracknumber', '')
    tags['tracktotal'] = track_original_tags.get('tracktotal', '')
    tags['upc'] = album_attributes.get('upc', '')

    picture = Picture()
    picture.type = 3
    picture.mime = 'image/jpeg'
    picture.data = open(cover, 'rb').read()
    flac.clear_pictures()
    flac.add_picture(picture)
    flac.save(padding=new_padding)
    logger.info(f'Processing completed: {file}')

logger.info('Processing complete.')

logger.info('---------- Step 5: Rename ----------')
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
    logger.info(f'{os.path.basename(file)} -> {filename}')

logger.info('---------- Step 6: Categorization ----------')


def get_spec(audio):
    sample_rate = audio.info.sample_rate / 1000
    bits_per_sample = audio.info.bits_per_sample
    if sample_rate.is_integer():
        sample_rate = int(sample_rate)
    return '{}-{}'.format(bits_per_sample, sample_rate)


def get_year(audio):
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
        audio = File(flac_path)
        artist = audio.get('albumartist', ['Unknown Artist'])[0]
        album_name = audio.get('album', ['Unknown Album'])[0]
        album = secure_filename(f'{artist} - {album_name}')
        year = get_year(audio)
        fmt = 'FLAC'
        spec = get_spec(audio)
        info = secure_filename(f' ({year}) [Amazon Music Rip] [{fmt} {spec}]')
        dest_dir = f'{album}{info}'
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        cover_src = os.path.join(root, 'cover.jpg')
        cover_dest = os.path.join(dest_dir, 'cover.jpg')
        if not os.path.exists(cover_dest) and os.path.exists(cover_src):
            os.rename(cover_src, cover_dest)
        dest_file = os.path.join(dest_dir, flac_file)
        if not os.path.exists(dest_file):
            os.rename(os.path.join(root, flac_file), dest_file)

logger.info('Processing complete.')
