"""
Check for cover art in album folders
"""
import os


def check_cover(directory):
    items = os.listdir(directory)
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            check_cover(item_path)
        elif item == 'cover.jpg':
            break
    else:
        if '-' in directory and directory.endswith(']'):
            print(os.path.basename(directory))


check_cover(os.getcwd())
