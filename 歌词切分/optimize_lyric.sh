while true
do
    read -p "文件名：" file
    ./optimize_lyric.py "$file"
done
