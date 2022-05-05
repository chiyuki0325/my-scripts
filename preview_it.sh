#!/bin/bash
# 通过某种奇怪方式实现类 Mac OS 的 「快速预览」
# 依赖：xclip xdotool sushi gloobus-preview hawkeye-quicklook-git (AUR)
# GitHub 已经不支持 git:// 克隆，于是需要修改 hawkeye-quicklook-git 的 PKGBUILD，git:// 改为 git+https:// 。

xclip -selection clipboard -o > /tmp/selection # 备份当前剪贴板
xdotool key  --delay 0 --clearmodifiers Ctrl+c # 复制选中文件

FILE_PATH=`xclip -selection clipboard -o | sed 's|^file://||'`
FILE_NAME="`basename "$FILE_PATH"`"
# 获取文件名

FILE_MIME=`file --mime-type "$FILE_PATH" | awk -F": " '{print $2}'`
FILE_MIME_1=`echo $FILE_MIME | awk -F"/" '{print $1}'`
FILE_MIME_2=`echo $FILE_MIME | awk -F"/" '{print $2}'`
# 获取 mimetype
if [ ${FILE_NAME: -3} == ".md" ]; then
    # markdown 使用 hawkeye 打开
    hawkeye --uri="file://${FILE_PATH}"
elif [ ${FILE_NAME: -4} == ".xml" ]; then
    # xml 使用 gloobus-preview 打开
    gloobus-preview "$FILE_PATH"
else
    if [ $FILE_MIME_1 == "text" ]; then
        if [ $FILE_MIME_2 == "plain" ]; then
            sushi "$FILE_PATH"
        else
            gloobus-preview "$FILE_PATH"
        fi
    else
        if [[ $FILE_MIME_1 == "image" ]] || [[ $FILE_MIME_1 == "audio" ]] || [[ $FILE_MIME_1 == "video" ]] || [[ $FILE_MIME_2 == "pdf" ]]; then
            sushi "$FILE_PATH"
        else
            gloobus-preview "$FILE_PATH"
        fi
    fi
fi
# 根据文件类型弹出不同预览窗口

xdotool keyup Ctrl # 松开 Ctrl
xdotool keyup space # 松开 Space
sleep 0.08s # 等待窗口开启
WINDOW_ID=`xdotool search --name "$FILE_NAME"` # 获取窗口 ID
WINDOW_ID=`echo $WINDOW_ID | sed "s/\n/ /"` # 没毛用，玄学东西，降低出错率
xdotool windowactivate $WINDOW_ID # 将窗口置于前台

xclip -i -selection clipboard < /tmp/selection # 导入备份的剪贴板文件
rm /tmp/selection # 删除备份，清理内存
