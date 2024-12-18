import os
from mutagen.flac import FLAC
from pathlib import Path

def delete(flac_path):
    try:
        audio = FLAC(flac_path)
        pictures = audio.pictures
        if pictures.length == 0:
            os.remove(flac_path)
        print(f"已删除: {flac_path}")
    except Exception as e:
        print(f"删除失败 {flac_path}: {e}")

def process_folder(folder_path):
    folder = Path(folder_path)
    flac_files = list(folder.glob('*.flac'))

    if flac_files:
        delete(flac_files[0])

    for subfolder in folder.iterdir():
        if subfolder.is_dir():
            process_folder(subfolder)

if __name__ == "__main__":
    current_directory = Path.cwd()
    process_folder(current_directory)
