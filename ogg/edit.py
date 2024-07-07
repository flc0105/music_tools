import os,sys
import glob
from mutagen.oggvorbis import OggVorbis

if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])


def new_padding(padding):
    return 0



audio = OggVorbis(filename)
audio.delete()

audio['album'] = ''

audio['albumartist'] = ''

audio['artist'] = ''

audio['date'] = ''

audio['title'] = ''

audio['tracknumber'] = ''

audio['tracktotal'] = ''



# 保存修改
audio.save(padding=new_padding)


print("标签修改完成。")
