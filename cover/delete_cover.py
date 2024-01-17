import os
from pathlib import Path

def delete_cover_files(folder_path):
    """
    Recursively deletes all 'cover.jpg' files in the specified folder and its subfolders.

    Parameters:
    - folder_path (Path): The path to the folder to be processed.
 
    Returns:
    - None
    """
    folder = Path(folder_path)

    for file in folder.glob('**/cover.jpg'):
        try:
            file.unlink()
            print(f"Cover file deleted: {file}")
        except Exception as e:
            print(f"Error deleting cover file {file}: {e}")

if __name__ == "__main__":
    current_directory = Path.cwd()
    delete_cover_files(current_directory)
