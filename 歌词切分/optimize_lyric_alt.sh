while true
do
    read -p "文件名 (alt)：" file
    ./optimize_lyric_alt.py "$file"
done
