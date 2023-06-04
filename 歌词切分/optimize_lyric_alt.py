#!/usr/bin/env python3
import sys
import math

# copilot 写的，无脑 tab，一大坨 split，能跑就行

MAX_LENGTH_PER_LINE = 48  # 一行的最大字节长度

lyric_orig = open(sys.argv[1], 'r').read()

# 第一阶段优化：去除空行

lyric = ''

for line in lyric_orig.splitlines():
    time, content = line.split(']')
    sec = time[1:].split(':')[0]
    if content != '':
        lyric += line + '\n'

# 第三阶段优化：拆分超出长度的行

lines = lyric.splitlines()

new_lyric = ''

for i in range(0, len(lines)):
    line = lines[i]
    time = line.split(']')[0][1:]
    content = line.split(']')[1]
    if len(content.encode()) > MAX_LENGTH_PER_LINE:
        # 拆分超出长度的行
        try:
            next_line_time: str = lines[i+1].split(']')[0][1:]
            min = time.split(':')[0]
            this_sec, next_sec = int(time.split(':')[1].split('.')[0]), int(next_line_time.split(':')[1].split('.')[0])
            this_millisec, next_millisec = int(time.split(':')[1].split('.')[1]), int(next_line_time.split(':')[1].split('.')[1])
            millisec_zfill_length = len(time.split(':')[1].split('.')[1])
            if next_sec > this_sec:
                new_sec = str(math.floor((next_sec - this_sec) / 2) + this_sec).zfill(2)
                new_millisec = str(math.floor((next_millisec - this_millisec) / 2) + this_millisec).zfill(millisec_zfill_length)
                new_time = f'[{min}:{new_sec}.{new_millisec}]'
            else:
                new_sec = str(math.floor((60 - this_sec + next_sec) / 2) + this_sec).zfill(2)
                new_millisec = str(math.floor((next_millisec - this_millisec) / 2) + this_millisec).zfill(millisec_zfill_length)
                new_time = f'[{min}:{new_sec}.{new_millisec}]'

            this_line_content = content[:len(content) // 2]
            next_line_content = content[len(content) // 2:]

            new_line_0 = '[' + time + ']' + this_line_content
            new_line_1 = new_time + next_line_content
            new_lyric += new_line_0 + '\n' + new_line_1 + '\n'
        except IndexError:
            this_sec = int(time.split(':')[1].split('.')[0])
            min = time.split(':')[0]
            this_millisec = int(time.split(':')[1].split('.')[1])
            new_time = f'[{min}:{str(this_sec + 1).zfill(2)}.{this_millisec}]'

            this_line_content = content[:len(content) // 2]
            next_line_content = content[len(content) // 2:]

            new_line_0 = '[' + time + ']' + this_line_content
            new_line_1 = new_time + next_line_content
            new_lyric += new_line_0 + '\n' + new_line_1 + '\n'

    else:
        new_lyric += line + '\n'


# 覆盖
open(sys.argv[1], 'w').write(new_lyric)