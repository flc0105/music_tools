import os
import hashlib
import json

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_flac_files(root_dir):
    flac_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.flac'):
                flac_files.append(os.path.join(dirpath, filename))
    return flac_files

def main():
    root_dir = '.'  # 当前目录
    flac_files = find_flac_files(root_dir)
    file_hashes = []

    for file_path in flac_files:
        file_hashes.append({
            "path": file_path,
            "md5": md5(file_path)
        })

    with open('flac_files_hashes.json', 'w', encoding='utf-8') as f:
        json.dump(file_hashes, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
