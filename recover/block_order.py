import os, sys

from mutagen.flac import FLAC


def print_blocks(flac):
    block_types = {
        0: 'STREAMINFO',
        1: 'PADDING',
        2: 'APPLICATION',
        3: 'SEEKTABLE',
        4: 'VORBIS COMMENT',
        6: 'PICTURE'
    }

    for i, block in enumerate(flac.metadata_blocks): # 遍历所有元数据块
        print(f'{i} ({block_types.get(block.code, block.code)})') # 通过元数据块的编码去字典中对应相应的显示名称
        print('-' * 20)
        if block.code == 6:
            print(block) # 如果是图片元数据块显示该对象
        else:
            print(vars(block)) # 其他块类型以字典形式显示
        print()


if len(sys.argv) < 2:
    os.system('pause')
    sys.exit(1)

filename = ' '.join(sys.argv[1:])
flac = FLAC(filename)

print_blocks(flac)
old_index = input('元数据块的原始索引位置：')
new_index = input('元数据块的新索引位置：')

try:
    if old_index and new_index:
        old_index = int(old_index)
        new_index = int(new_index)
    else:
        raise Exception('索引位置不能为空')
except Exception as e:
    print(e)
    sys.exit(1)


flac.metadata_blocks.insert(new_index, flac.metadata_blocks.pop(old_index))
flac.save()
print('修改完成')
print_blocks(flac)




