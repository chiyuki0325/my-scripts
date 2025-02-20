### bili.sh

用 mpv 带弹幕播放哔哩哔哩长视频。  
由于双显卡笔记本在 Linux 上，浏览器不能使用独显硬件解码，播放长视频很吃力，故诞生此需求。

依赖：yt-dlp, jq, python-biliass, mpv  
需要浏览器中已经登录哔哩哔哩账号。

```bash
cp ./bili ~/.local/bin/bili
bili https://www.bilibili.com/video/BVxxxxxxx
```

