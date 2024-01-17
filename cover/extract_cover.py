import os
from mutagen.flac import FLAC
from mutagen import File
from pathlib import Path

def extract_cover(flac_path):
    """
    Extracts the cover image from a FLAC file and saves it as 'cover.jpg' in the same directory.

    Parameters:
    - flac_path (Path): The path to the FLAC file.

    Returns:
    - None
    """
    try:
        audio = FLAC(flac_path)
        pictures = audio.pictures
        for p in pictures:
            if p.type == 3:
                cover_path = flac_path.parent / 'cover.jpg'
                with open(cover_path, 'wb') as cover_file:
                    cover_file.write(p.data)
                print(f"Cover extracted and saved: {cover_path}")
                return  # Exit the function after extracting the first cover
        print(f"No cover found in: {flac_path}")
    except Exception as e:
        print(f"Error extracting cover from {flac_path}: {e}")

def extract_m4a_cover(m4a_path):
    """
    Extracts the cover image from an M4A file and saves it as 'cover.jpg' in the same directory.

    Parameters:
    - m4a_path (Path): The path to the M4A file.

    Returns:
    - None
    """
    try:
        audio = File(m4a_path)
        if 'covr' in audio:
            pictures = audio['covr']
            for p in pictures:
                cover_path = m4a_path.parent / 'cover.jpg'
                with open(cover_path, 'wb') as cover_file:
                    cover_file.write(p)
                print(f"Cover extracted and saved: {cover_path}")
                return  # Exit the function after extracting the first cover
        print(f"No cover found in: {m4a_path}")
    except Exception as e:
        print(f"Error extracting cover from {m4a_path}: {e}")

def process_folder(folder_path):
    """
    Recursively processes a folder, checking for FLAC and M4A files and extracting cover images if needed.

    Parameters:
    - folder_path (Path): The path to the folder to be processed.

    Returns:
    - None
    """
    folder = Path(folder_path)
    flac_files = list(folder.glob('*.flac'))
    m4a_files = list(folder.glob('*.m4a'))
    cover_path = folder / 'cover.jpg'

    if not cover_path.exists():
        if flac_files:
            extract_cover(flac_files[0])
        elif m4a_files:
            extract_m4a_cover(m4a_files[0])

    for subfolder in folder.iterdir():
        if subfolder.is_dir():
            process_folder(subfolder)

if __name__ == "__main__":
    current_directory = Path.cwd()
    process_folder(current_directory)
