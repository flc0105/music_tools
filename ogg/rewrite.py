import os
import glob
from mutagen.oggvorbis import OggVorbis

# 获取当前目录下所有ogg文件
ogg_files = glob.glob("*.ogg")

# 按照修改时间排序
ogg_files.sort(key=os.path.getmtime, reverse=True)

print(ogg_files)


def new_padding(padding):
    return 0


# 遍历列表，修改文件标签
for index, file in enumerate(ogg_files, start=1):
    audio = OggVorbis(file)

    # 获取原始title
    original_title = audio.get('TITLE', ['Unknown Title'])[0]

    original_album = audio.get('ALBUM', ['Unknown Album'])[0]

    audio.delete()
    
    audio['album'] = original_album

    audio['albumartist'] = ""

    audio['artist'] = ""

    audio['date'] = ''

  
    audio['title'] = original_title
    
    audio['tracknumber'] = str(index)

    audio['tracktotal'] = str(len(ogg_files))
    

    
    # 保存修改
    audio.save(padding=new_padding)


print("标签修改完成。")
