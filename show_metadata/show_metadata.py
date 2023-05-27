import datetime
import hashlib
import os
import sys

from mutagen.flac import FLAC


def get_hash(filename):
    with open(filename, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()


def format_seconds(seconds):
    td = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str = f'{hours:02}:{minutes:02}:{seconds:02}'
    return time_str


if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
file_hash = get_hash(filename)
flac = FLAC(filename)
info = flac.info
md5 = hex(info.md5_signature).split('x')[-1]
sample_rate = info.sample_rate / 1000
bits_per_sample = info.bits_per_sample
length = format_seconds(info.length)

tags = {}
for key, value in flac.tags.items():
    if value[0] == '':
        tags[key] = '<empty>'
    elif value[0] == ' ':
        tags[key] = '<space>'
    else:
        tags[key] = value[0]
sorted_dict = {key: tags[key] for key in sorted(tags)}

print('Info')
print('-' * 20)
print(f'{"file_hash":40}{file_hash}')
print(f'{"audio_md5":40}{md5}')
print(f'{"sample_rate":40}{sample_rate} kHz')
print(f'{"bits_per_sample":40}{bits_per_sample}')
print(f'{"length":40}{length}')

padding_length = None
for block in flac.metadata_blocks:
    if block.code == 1:
        padding_length = block.length

try:
    vendor_string = flac.tags.vendor
except:
    vendor_string = '获取失败'

print(f'{"padding_length":40}{padding_length}')
print(f'{"vendor_string":40}{vendor_string}')

print('\nTags')
print('-' * 20)
print('\n'.join(f'{k:40}{v}' for k, v in sorted_dict.items()))
os.system('pause')
