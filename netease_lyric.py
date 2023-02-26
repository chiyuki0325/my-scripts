#!/usr/bin/env python3
# netease_lyric.py
# Get lyrics from netease music
# 2023 YidaozhanYa

import requests
import os
import sys
import re

API_ROOT: str = "http://localhost:3000"

for root, _, files in os.walk(sys.argv[1]):
    for file in files:
        song_name: str = ".".join(file.split(".")[:-1])  # Remove extension
        print(song_name)
        response = requests.get(
            url=f"{API_ROOT}/cloudsearch?keywords={song_name}",
            data={"limit": 1},
        )
        song_id: int = response.json()["result"]["songs"][0]["id"]
        response = requests.get(
            url=f"{API_ROOT}/lyric?id={song_id}",
        )
        lyric: str = response.json()["lrc"]["lyric"]
        if (
            "tlyric" in response.json()
            and response.json()["tlyric"]["lyric"] != ""
            and (
                re.compile("[\u3040-\u309f]+").search(lyric)
                or re.compile("[\u30a0-\u30ff]+").search(lyric)
            )
        ):
            print("tlyric")
            lyric = response.json()["tlyric"]["lyric"]
            for line in lyric.split("\n"):
                if line == "":
                    continue
                text: str = ']'.join(line.split("]")[1:])
                new_text: str = text.strip('(（)）')
                if new_text != text:
                    lyric = lyric.replace(text, new_text)
        with open(os.path.join(root, f"{song_name}.lrc"), "w") as f:
            f.write(lyric)
