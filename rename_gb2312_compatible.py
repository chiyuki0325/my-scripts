#!/usr/bin/env python3

# rename_gb2312_compatible.py
# Rename files to GB2312 compatible
# 2023 YidaozhanYa

import os
import sys
from opencc import OpenCC
from pykakasi import kakasi
import re


def convert_filename(filename: str) -> str:
    cc = OpenCC("t2s")
    cc_jp = OpenCC("jp2t")
    kks = kakasi()
    new_filename: str = cc.convert(cc_jp.convert(filename))
    result: list[dict[str, str]] = kks.convert(new_filename)
    for kks_item in result:
        if (
            re.compile("[\u3040-\u309f]+").match(kks_item["orig"])
        ) or (
            re.compile("[\u30a0-\u30ff]+").match(kks_item["orig"])
        ):
            new_filename = new_filename.replace(
                kks_item["orig"],kks_item["hepburn"]
            )
    return re.compile(" +").sub(" ", new_filename.replace('　','')).strip()


if len(sys.argv) < 2:
    print("Usage: rename_gb2312_compatible.py <folder to process>")
    sys.exit(1)

for root, _, files in os.walk(sys.argv[1]):
    for file in files:
        old_filename: str = os.path.join(root, file)
        new_filename = os.path.join(root, convert_filename(file))
        if old_filename != new_filename:
            print(tuple([old_filename, new_filename]))
            os.rename(old_filename, new_filename)
