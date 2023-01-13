#!/usr/bin/env bash
i=-5
packages=""
for package in $(pip list --user --outdated); do
    i=$(($i+1))
    if [ $i == 4 ]; then
        packages="$packages $package"
        i=0
    fi
done
pip install --upgrade $packages
