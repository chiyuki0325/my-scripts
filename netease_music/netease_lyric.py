#!/usr/bin/env python3
# netease_lyric.py
# Get lyrics from netease music
# 2023-2025 chiyuki0325

import requests
import os
import sys
import re

API_ROOT: str = "http://localhost:3000"


def parse_lyric(lyric_str: str) -> list[tuple[str, str]]:
    """Parse LRC string into list of (timestamp, text) pairs."""
    result = []
    for line in lyric_str.split("\n"):
        if not line.strip():
            continue
        timestamps = re.findall(r"\[(\d+:\d+\.\d+)\]", line)
        text = re.sub(r"\[\d+:\d+\.\d+\]", "", line).strip()
        for ts in timestamps:
            result.append((ts, text))
    return result


def build_dual_lyric(orig_lyric: str, trans_lyric: str) -> str:
    """Build dual-line format: original line followed by translation if exists."""
    orig_lines = parse_lyric(orig_lyric)
    trans_map = {}
    for ts, text in parse_lyric(trans_lyric):
        trans_map[ts] = text

    result = []
    for ts, text in orig_lines:
        result.append(f"[{ts}]{text}")
        if ts in trans_map and trans_map[ts]:
            result.append(f"[{ts}]{trans_map[ts]}")

    return "\n".join(result)


for root, _, files in os.walk(sys.argv[1]):
    for file in files:
        file_name: str = ".".join(file.split(".")[:-1]).strip()
        song_name: str = ""
        if sys.argv[-1] == "a":
            song_name = ".".join(file.split(".")[:-1]).strip()
        else:
            try:
                song_name = ".".join(file.split(".")[:-1]).split(" - ")[1].strip()
            except IndexError:
                song_name = ".".join(file.split(".")[:-1]).strip()
        print(song_name)
        response = requests.get(
            url=f"{API_ROOT}/cloudsearch?keywords={song_name}",
            data={"limit": 1},
        )
        song_id: int = response.json()["result"]["songs"][0]["id"]

        response = requests.get(
            url=f"{API_ROOT}/lyric/?id={song_id}",
        )
        lyric: str = response.json()["lrc"]["lyric"]

        tlyric_str = ""
        if (
            "tlyric" in response.json()
            and response.json()["tlyric"]["lyric"] != ""
        ):
            tlyric_str = response.json()["tlyric"]["lyric"]
            for line in tlyric_str.split("\n"):
                if line == "":
                    continue
                text: str = "]".join(line.split("]")[1:])
                new_text: str = text.strip("(（)）")
                if new_text != text:
                    tlyric_str = tlyric_str.replace(text, new_text)

        output_lyric = build_dual_lyric(lyric, tlyric_str)

        with open(os.path.join(root, f"{file_name}.lrc"), "w") as f:
            f.write(output_lyric)
