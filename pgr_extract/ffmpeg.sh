#!/bin/bash
#$1 Tracks folder
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
cd "$1"
for song in *;do
cd "$song"
ffmpeg -y -i music.wav music.ogg
cd ..
done
IFS=$SAVEIFS
