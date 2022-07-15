#!/bin/bash
xclip -t image/png -o -sel clipboard > /tmp/tmp.png
deepin-ocr /tmp/tmp.png
