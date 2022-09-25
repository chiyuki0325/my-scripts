#!/bin/bash
#$1 Tracks folder
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
cd "$1"
mkdir "../packed"
for song in *;do
pushd "$song"
newname="`printf "$song" | sed "s/\.0//" | sed -E "s/(.*)\./\1 - /"`"
if [ -f music.ogg ];then rm music.wav;fi
7z a "../../packed/${newname}.zip" .
popd
done

IFS=$SAVEIFS
