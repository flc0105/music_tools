import os, sys

from mutagen.flac import FLAC

if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
flac = FLAC(filename)

block_types = {
    0: 'STREAMINFO',
    1: 'PADDING',
    2: 'APPLICATION',
    3: 'SEEKTABLE',
    4: 'VORBIS COMMENT',
    6: 'PICTURE'
}

for i, block in enumerate(flac.metadata_blocks):
    print(f'{i} ({block_types.get(block.code)})')
    print('-' * 20)
    if block.code == 6:
        print(block)
    else:
        print(vars(block))
    print()

os.system('pause')
