#!/usr/bin/env python3

import os
import sys
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, USLT, SYLT, Encoding
from pathlib import Path

for root, _, files in os.walk(sys.argv[1]):
    for file in files:
        path = sys.argv[1] + '/' + file
        if file.endswith(".flac") or file.endswith(".mp3"):
            if file.endswith(".flac"):
                music = FLAC(path)
                lyric_path = Path(sys.argv[1] + '/' + file[:-5] + '.lrc')
                if not 'lyrics' in music:
                    if lyric_path.exists():
                        music['lyrics'] = str(lyric_path.open('r').read())
                        music.save()
                if 'description' in music:
                    desc = music['description'][0]
                    if desc.startswith('163') or desc.startswith('kuwo'):
                        music['description'] = []
                        music.save()
            elif file.endswith(".mp3"):
                music_id3 = ID3(path)
                lyric_path = Path(sys.argv[1] + '/' + file[:-4] + '.lrc')
                comm = music_id3.getall('COMM')
                sylt = music_id3.getall('SYLT')
                uslt = music_id3.getall('USLT')
                if comm != []:
                    desc = comm[0].text[0]
                    if desc.startswith('163') or desc.startswith('kuwo'):
                        music_id3.setall('COMM', [])
                        music_id3.save(v2_version=3)
                if sylt == []:
                    if lyric_path.exists():
                        sync_lrc: list[tuple[str, int] | None] = []
                        lrc_text = lyric_path.open('r').readlines()
                        for line in lrc_text:
                            line = line.strip()
                            if line.startswith('['):
                                line_splits = line[1:].split(']')
                                time = line_splits[0].replace('-', '')
                                time_split = time.split(':')
                                time_split_2 = time_split[1].split('.')
                                if time_split_2.__len__() < 2:
                                    continue
                                milliseconds = int(time_split[0]) * 60 * 1000 + int(time_split_2[0]) * 1000 + int(
                                    time_split_2[1].ljust(3, '0'))
                                text = ']'.join(line_splits[1:])
                                sync_lrc.append((text, milliseconds))
                        print(sync_lrc)
                        music_id3.setall("SYLT", [
                            SYLT(encoding=Encoding.UTF8, lang='chi', format=2, type=1, text=sync_lrc)])
                        # music['lyrics'] =
                        music_id3.save(v2_version=3)
                if uslt == []:
                    if lyric_path.exists():
                        lrc_text = lyric_path.open('r').read()
                        music_id3.setall("USLT", [
                            USLT(encoding=Encoding.UTF8, lang='chi', text=lrc_text)])
                        # music['lyrics'] =
                        music_id3.save(v2_version=3)
