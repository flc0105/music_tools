import logging
import os
import sys
from datetime import datetime

from mutagen.flac import FLAC

current_time = datetime.now()
formatted_time = current_time.strftime("%Y%m%d_%H%M%S")

if '--nolog' in sys.argv:
    logging.disable(logging.CRITICAL)
    logging.getLogger().disabled = True
else:
    logging.basicConfig(
        filename=f'{formatted_time}.log',
        format='[%(asctime)s] %(levelname)s: %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

logger = logging.getLogger(__name__)


class Colors:
    BRIGHT_GREEN = '\033[0;92m'
    BRIGHT_RED = '\033[0;91m'
    BRIGHT_YELLOW = '\033[0;93m'
    RESET = '\033[0;39m\033[0m'


def success(flac_path, source, message):
    message = f'[+] [{source}] {flac_path}：{message}'
    logger.info(message)
    print(f'{Colors.BRIGHT_GREEN}{message}{Colors.RESET}')


def error(flac_path, source, message):
    message = f'[-] [{source}] {flac_path}：{message}'
    logger.error(message)
    print(f'{Colors.BRIGHT_RED}{message}{Colors.RESET}')


def warning(flac_path, source, message):
    message = f'[!] [{source}] {flac_path}：{message}'
    logger.warning(message)
    print(f'{Colors.BRIGHT_YELLOW}{message}{Colors.RESET}')


def get_valid_padding_length(base_number, seconds):
    return base_number + (seconds // 10) * 18


def get_padding_length(flac):
    return flac.metadata_blocks[-1].length


def get_source(flac):
    """获取音源"""
    try:
        if flac.tags.get('45b1d925-1448-5784-b4da-b89901050a13', [''])[0] == '10006001':
            return 'mora'
        elif flac.tags.get('comment', [''])[0].startswith('Brought to you by OTOTOY.JP'):
            return 'OTOTOY'
        else:
            raise Exception('未识别的音源')
    except Exception as e:
        raise Exception(f'识别音源失败：{e}')


def validate_mora_padding(flac):
    try:
        actual_padding = get_padding_length(flac)
    except Exception as e:
        return 0, f'获取填充长度失败，{e}'
    base_numbers = [8244, 8258, 8288, 8302]
    for base_number in base_numbers:
        padding = get_valid_padding_length(base_number, flac.info.length)
        if actual_padding == padding:
            return 1, f'填充长度验证成功（{base_number}）'
    return 0, f'填充长度验证失败（{actual_padding}）'


def validate_mora_order(flac):
    keys = list(flac.tags)
    if keys[0][0] == 'ARTIST':
        if keys[-1][0] == '50dbf5a2-f864-5c17-be00-c36dfd3df7b4':
            return 1, '标签顺序验证成功（50d）'
        elif keys[-1][0] == 'ff8ca75f-2d68-52eb-85d6-1580486025a4':
            return 1, '标签顺序验证成功（ff8）'
    return 0, '标签顺序验证失败'


def validate_ototoy_padding(flac):
    try:
        actual_padding = get_padding_length(flac)
    except Exception as e:
        return 0, f'获取填充长度失败，{e}'
    if actual_padding == 8192:
        return 1, f'填充长度验证成功（8192）'
    return 0, f'填充长度验证失败（{actual_padding}）'


def validate_ototoy_order(flac):
    keys = list(flac.tags)
    if keys[0][0] == 'tracknumber':
        if keys[-1][0] == 'comment':
            return 1, '标签顺序验证成功'
        elif keys[-1][0] == 'WAVEFORMATEXTENSIBLE_CHANNEL_MASK':
            return 1, '标签顺序验证成功（Hires）'
    return 0, '标签顺序验证失败'

block_types = {
    0: 'STREAMINFO',
    1: 'PADDING',
    2: 'APPLICATION',
    3: 'SEEKTABLE',
    4: 'VORBIS COMMENT',
    6: 'PICTURE'
}

def validate_mora_blocks(flac):
    try:
        blocks = flac.metadata_blocks
        if blocks[0].code == 0 and blocks[1].code == 4 and blocks[2].code == 6 and blocks[3].code == 1:
            return 1, '块顺序验证成功'
        raise
    except:
        return 0, '块顺序验证失败'


def validate_ototoy_blocks(flac):
    try:
        blocks = flac.metadata_blocks
        if blocks[0].code == 0 and blocks[1].code == 4 and blocks[2].code == 3 and blocks[-2].code == 6 and blocks[-1].code == 1:
            return 1, f'块顺序验证成功（{len(flac.metadata_blocks)}）'
        elif blocks[0].code == 0 and blocks[1].code == 3 and blocks[2].code == 4 and blocks[3].code == 6 and blocks[4].code == 1:
            return 1, f'块顺序验证成功（{len(flac.metadata_blocks)}）'
        raise
    except:
        return 0, '块顺序验证失败'
    

os.system('')
for root, dirs, files in os.walk('.'):
    flac_files = [f for f in files if f.endswith('.flac')]
    for flac_file in flac_files:
        flac_path = os.path.join(root, flac_file)
        flac = FLAC(flac_path)
        try:
            source = get_source(flac)
        except Exception as e:
            warning(flac_path, '未知', e)
            continue
        if source == 'mora':
            code_padding, message_padding = validate_mora_padding(flac)
            code_order, message_order = validate_mora_order(flac)
            code_blocks, message_blocks = validate_mora_blocks(flac)
            if code_padding and code_order and code_blocks:
                success(flac_path, 'mora', f'{message_padding}，{message_order}，{message_blocks}')
            else:
                error(flac_path, 'mora', f'{message_padding}，{message_order}, {message_blocks}')
        elif source == 'OTOTOY':
            code_padding, message_padding = validate_ototoy_padding(flac)
            code_order, message_order = validate_ototoy_order(flac)
            code_blocks, message_blocks = validate_ototoy_blocks(flac)
            if code_padding and code_order and code_blocks:
                success(flac_path, 'OTOTOY', f'{message_padding}，{message_order}，{message_blocks}')
            else:
                error(flac_path, 'OTOTOY', f'{message_padding}，{message_order}, {message_blocks}')

os.system('pause')
