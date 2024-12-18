import os
from mutagen.flac import FLAC
from pathlib import Path



def process_folder(folder_path):
    folder = Path(folder_path)
    flac_files = list(folder.glob('*.flac'))

   for flac_file in flac_files:
        try:
            audio = FLAC(flac_file)
            pictures = audio.pictures
            if len(pictures) == 0:
                os.remove(flac_file)
            print(f"已删除: {flac_file}")
        except Exception as e:
            print(f"删除失败 {flac_file}: {e}")

    for subfolder in folder.iterdir():
        if subfolder.is_dir():
            process_folder(subfolder)

if __name__ == "__main__":
    current_directory = Path.cwd()
    process_folder(current_directory)
