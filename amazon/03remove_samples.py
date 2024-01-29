#!/usr/bin/env python3
import os
import subprocess
import locale

from mutagen import File

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.flac')]

skip = {
    44.1: '286',
    48.0: '312',
    96.0: '624',
    192.0: '1248'
}

for file in files:
    flac = File(file)
    info = flac.info
    sample_rate = info.sample_rate / 1000
    skip_value = skip.get(sample_rate, 'N/A')
    print("{} 的采样率为 {:.1f} kHz，将去除前 {} 位的空采样".format(file, sample_rate, skip_value))

    command = [
        'flac',
        '-5',
        '--skip',
        skip_value,
        '--no-seektable',
        f'"{file}"',
        '-f'
    ]
    print(f"将执行命令：{' '.join(command)}")

    try:
        p = subprocess.run(' '.join(command), shell=True, check=True)  # capture_output=True
        print(f'{file} 处理成功')
    except subprocess.CalledProcessError as e:  # e.stderr.decode()
        print(f'{file} 处理失败')
