#!/bin/bash
mkdir ${1}_out
for file in $1/*.ts
do
dd if="$file" of="${file/${1}/${1}_out}" bs=4 skip=53
done
