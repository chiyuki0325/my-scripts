#!/bin/bash
bwrap --dev-bind / / --tmpfs ~/.fonts/ms-tmp /bin/bash -c "for file in \`find /usr/share/fonts/ms -name '.*' | grep tt | sed -s 's#/usr/share/fonts/ms/.##'\`;do cp /usr/share/fonts/ms/.\$file ~/.fonts/ms-tmp/\$file;done;ls ~/.fonts/ms-tmp;$1"
