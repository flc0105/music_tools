#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime, timezone, timedelta

from mutagen import File
from mutagen.flac import Picture

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]


def new_padding(padding):
    return 8192


def process_date(input_string):
    if not input_string:
        return ''
    original_datetime = datetime.fromisoformat(input_string.replace("Z", "+00:00"))
    japan_timezone = timezone(timedelta(hours=9))
    japan_datetime = original_datetime.astimezone(japan_timezone)
    japan_formatted = japan_datetime.strftime("%Y-%m-%d")
    print(f"{input_string} -> {japan_formatted}")
    return japan_formatted


for file in files:
    flac = File(file)

    filename_without_extension = os.path.splitext(file)[0]

    json_filename = f"{filename_without_extension}.json"
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            tags = flac.tags

            comment = json_data.get('comment', '')
            match = re.search(r'albums/([A-Z0-9]+)\?trackAsin=([A-Z0-9]+)', comment)
            if match:
                albumid = match.group(1)
                trackid = match.group(2)
            else:
                albumid = ''
                trackid = ''

            tags['album'] = json_data.get('album', '')
            tags['albumartist'] = json_data.get('albumartist', '')
            tags['albumid'] = albumid
            tags['artist'] = json_data.get('artist', '')
            tags['comment'] = json_data.get('comment', '')
            tags['composer'] = json_data.get('composer', '')
            tags['copyright'] = json_data.get('copyright', '')
            tags['date'] = process_date(json_data.get('date', ''))
            tags['discnumber'] = json_data.get('discnumber', '')
            tags['disctotal'] = json_data.get('disctotal', '')
            tags['genre'] = json_data.get('genre', '')
            tags['isrc'] = json_data.get('isrc', '')
            tags['label'] = json_data.get('label', '')
            tags['title'] = json_data.get('title', '')
            tags['trackid'] = trackid
            tags['tracknumber'] = json_data.get('tracknumber', '')
            tags['tracktotal'] = json_data.get('tracktotal', '')

    # cover_filename = f"{json_data.get('album')}.jpg"
    # if os.path.exists(cover_filename):
    #     flac.clear_pictures()
    #     picture = Picture()
    #     picture.type = 3
    #     picture.mime = 'image/jpeg'
    #     picture.data = open(cover_filename, 'rb').read()
    #     flac.add_picture(picture)
    #     print(f"Cover image imported: {cover_filename}")

    flac.save(padding=new_padding)
    print(f"Processed: {file}")
