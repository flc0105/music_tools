import os

def extract_music_name(filename):
    # 提取音乐名
    start_index = filename.find('-') + 1
    end_index = filename.rfind('.')
    if start_index >= 0 and end_index >= 0:
        return filename[start_index:end_index]
    return None

def find_duplicate_music(root_dir='.'):
    music_names = {}
    duplicates = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.flac') or file.endswith('.m4a'):
                file_path = os.path.join(root, file)
                music_name = extract_music_name(file)
                if music_name:
                    if music_name in music_names:
                        duplicates.append((file_path, music_names[music_name]))
                    else:
                        music_names[music_name] = file_path

    return duplicates

def main():
    duplicates = find_duplicate_music()

    if duplicates:
        print("重复的音乐文件:")
        for file1, file2 in duplicates:
            print(f"{file1} 与 {file2} 音乐名重复")

    else:
        print("没有找到重复的音乐文件")

if __name__ == "__main__":
    main()
