import os
import hashlib
import json

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    with open('flac_files_hashes.json', 'r', encoding='utf-8') as f:
        recorded_hashes = json.load(f)

    for entry in recorded_hashes:
        file_path = entry["path"]
        recorded_md5 = entry["md5"]
        
        if os.path.exists(file_path):
            current_md5 = md5(file_path)
            if current_md5 != recorded_md5:
                print(f"[MISMATCH] {file_path}: recorded MD5 = {recorded_md5}, current MD5 = {current_md5}")
            else:
                print(f"[MATCH] {file_path}")
        else:
            print(f"[MISSING] {file_path} does not exist")

if __name__ == "__main__":
    main()
