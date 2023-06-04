#!/usr/bin/env python3

from pathlib import Path
from xml.dom.minidom import parse as parse_xml
from mutagen.flac import FLAC, Picture
import shutil

# 常量
MUSIC_VERSION_DIR = Path('/mnt/ssd/下载/mai/maimai FESTiVAL (SDEZ 1.30.00)/Package/Sinmai_Data/StreamingAssets/A000/musicVersion/') 
MUSIC_GENRE_DIR = Path('/mnt/ssd/下载/mai/maimai FESTiVAL (SDEZ 1.30.00)/Package/Sinmai_Data/StreamingAssets/A000/musicGenre/') 
MUSIC_DATA_DIR = Path('/mnt/ssd/下载/mai/maimai FESTiVAL (SDEZ 1.30.00)/Package/Sinmai_Data/StreamingAssets/A000/music/')
SOUND_FLAC_DIR = Path('/home/yidaozhan/sound/')
JACKET_PNG_DIR = Path('/home/yidaozhan/jackets/')
OUTPUT_DIR = Path('/home/yidaozhan/output')

# 数据
music_version = {}
music_genre = {}
music_data = {}

for dir in MUSIC_VERSION_DIR.iterdir():
    if dir.is_dir():
        document = parse_xml(open(dir / 'MusicVersion.xml')).documentElement
        music_version[document.getElementsByTagName('version')[0].childNodes[0].data] = document.getElementsByTagName('genreName')[0].childNodes[0].data

for dir in MUSIC_GENRE_DIR.iterdir():
    if dir.is_dir():
        document = parse_xml(open(dir / 'MusicGenre.xml')).documentElement
        music_genre[document.getElementsByTagName('name')[0].getElementsByTagName('id')[0].childNodes[0].data] = document.getElementsByTagName('genreName')[0].childNodes[0].data

for dir in MUSIC_DATA_DIR.iterdir():
    if dir.is_dir():
        if (dir / 'Music.xml').exists():
            document = parse_xml(open(dir / 'Music.xml')).documentElement
            id = (document.getElementsByTagName('name')[0].getElementsByTagName('id')[0].childNodes[0].data).zfill(6)[-4:].zfill(6)
            song_name = document.getElementsByTagName('name')[0].getElementsByTagName('str')[0].childNodes[0].data
            artist_name = document.getElementsByTagName('artistName')[0].getElementsByTagName('str')[0].childNodes[0].data
            if '曲：' in artist_name:
                artist_name = artist_name.replace('曲：', '').replace('／歌：', ' feat. ').split('[')[0]
            genre_id = document.getElementsByTagName('genreName')[0].getElementsByTagName('id')[0].childNodes[0].data
            version = (document.getElementsByTagName('version')[0].childNodes[0].data)[0:3]+'00'
            music_data[id] = {
                'song': song_name,
                'artist': artist_name,
                'album': music_genre[genre_id] + ' (' + music_version[version] + ')',
            }

for music_file_orig in SOUND_FLAC_DIR.iterdir():
    if music_file_orig.is_file():
        id = music_file_orig.stem[-6:]
        music_file = OUTPUT_DIR / ('Music ' + id[2:] + '.flac')
        shutil.copy(
            music_file_orig,
            music_file
        )

        if id in music_data:
            new_filename = music_data[id]['artist'] + ' - ' + music_data[id]['song'] + '.flac'
            # 删除不兼容的字符
            new_filename = new_filename.replace('/', '／').replace('\\', '＼').replace(':', '：').replace('*', '＊').replace('?', '？').replace('"', '＂').replace('<', '＜').replace('>', '＞').replace('|', '｜')
            if 'CV.' in new_filename:
                new_filename = new_filename.split('／CV')[0]
            music_file.rename(
                OUTPUT_DIR / new_filename
                )
            music_file = OUTPUT_DIR / new_filename

        if id in music_data:
            audio_file = FLAC(music_file)
            audio_file['title'] = music_data[id]['song']
            audio_file['artist'] = music_data[id]['artist']
            audio_file['album'] = music_data[id]['album']
            audio_file['albumartist'] = music_data[id]['artist']
            audio_file.save()
        
        jacket_file = JACKET_PNG_DIR / f'UI_Jacket_{id}.png'
        if jacket_file.exists():
            picture = Picture()
            picture.type = 3
            picture.mime = 'image/png'
            if id in music_data:
                picture.desc = music_data[id]['song']
            picture.data = open(jacket_file, 'rb').read()
            audio_file.add_picture(picture)
            audio_file.save()
