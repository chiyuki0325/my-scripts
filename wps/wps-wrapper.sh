#!/bin/bash
export QT_IM_MODULE=fcitx
bwrap --dev-bind / / --tmpfs ~/.fonts/ms-tmp /bin/bash -c "for file in \$(find /usr/share/fonts/ms -name '.*' | grep tt | sed -s 's#/usr/share/fonts/ms/.##');do cp /usr/share/fonts/ms/.\$file ~/.fonts/ms-tmp/\$file;done;ls ~/.fonts/ms-tmp;/usr/bin/wps.bak \"$@\""%
