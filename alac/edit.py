#!/usr/bin/env python3
import json
import os
import sys

from mutagen import File



def no_padding(info):
    # this will remove all padding
    return 0

# Define the tags to keep
tags_to_keep = {'----:com.apple.itunes:ISRC', '----:com.apple.itunes:UPC'}

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.m4a')]
for file in files:
    m4a = File(file)

    # Collect tags to delete
    tags_to_delete = [tag for tag in m4a.tags if tag.startswith('----:') and tag not in tags_to_keep]

    # Delete the collected tags
    for tag in tags_to_delete:
        m4a.tags.pop(tag)

    m4a.save(padding=no_padding)
