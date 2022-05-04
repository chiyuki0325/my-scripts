#!/bin/bash
# 通过某种“奇怪”方式勉强实现 Quick Look
xdotool key  --delay 0 --clearmodifiers Ctrl+c # 复制选中文件
filepath=`xclip -selection clipboard -o | sed 's|^file://||'` # 获取文件名
sushi "$filepath" # 弹出预览窗口
sleep 0.08s # 等待窗口开启
bn="`basename "$filepath"`" # 获取文件名
windowid=`xdotool search --name "$bn"` # 获取窗口 ID
windowid=`echo $windowid | sed "s/\n/ /"` # 没毛用，玄学东西
xdotool windowactivate $windowid # 将窗口置于前台
