#!/usr/bin/env python3
# netease_lyric.py
# Get lyrics from netease music
# 2023 YidaozhanYa

import requests
import os
import sys

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
        with open(os.path.join(root, f"{song_name}.lrc"), "w") as f:
            f.write(lyric)