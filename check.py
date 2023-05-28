import os
import re

ignore_folders = ['Lyrics', 'Album', 'EP', 'Single', 'Live', 'Compilation', 'SPs', 'Digital Booklet']
recursive_ignore_dirs = ['_qobuz']
non_recursive_ignore_dirs = ['_more']
pattern_folder = r'.* - .* \(\d{4}\) \[(mora|OTOTOY|e-onkyo|qobuz||Bugs!|7digital)\] (\[.* .*\]|\[DSD.*\])$'
patterns = [
    r'\b\d{3}-.*\.(flac|m4a)\b',
    r'\b\d{2}_\d{2}_.*\.flac\b',
    r'\b\d{2}-\d{2}-.*-.*\.flac\b',
    r'\b\d{1,2}_\d+_.*_\d{1}\.flac\b',
    r'\b.*_\d{2}_.*\.flac\b'
]


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


def check_folder(root):
    for subdir, dirs, files in os.walk(root):
        if subdir == root or any(subdir == os.path.join(root, prefix) for prefix in non_recursive_ignore_dirs) or any(
                subdir.startswith(os.path.join(root, prefix)) for prefix in recursive_ignore_dirs):
            continue
        for dir_name in dirs:
            if dir_name in ignore_folders:
                continue
            if not re.match(pattern_folder, dir_name):
                print(dir_name)
            check_folder(os.path.join(subdir, dir_name))


def check_filenames(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if any(root.startswith(os.path.join(folder_path, prefix)) for prefix in recursive_ignore_dirs):
            continue
        for file in files:
            if file.endswith('.flac') or file.endswith('.m4a') or file.endswith('.wav'):
                if not is_valid_file_name(file):
                    print(os.path.basename(root))
                    break


def is_valid_file_name(file_name):
    for pattern in patterns:
        if re.match(pattern, file_name):
            return True
    return False


print(f'Covers\n{"-" * 20}')
check_cover(os.getcwd())
print(f'\nFolders\n{"-" * 20}')
check_folder(os.getcwd())
print(f'\nFilenames\n{"-" * 20}')
check_filenames(os.getcwd())
