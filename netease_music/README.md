### netease_lyric.py

批量从网易云音乐下载歌词，并保存到同名 lrc 文件。
我的个人需求：如果歌词中包含日语，则下载翻译歌词，否则下载原始歌词。（35 行开始）

加上 a 是以音乐文件名全名搜索，否则只以歌名搜索。

```bash
python netease_lyric.py FOLDER
python netease_lyric.py FOLDER a
```

### music_tags.py

把之前下载好的 lrc 歌词写到音乐文件头，并去除网易跟踪参数。

用法同上。



依赖：
https://版权保护故去除域名/Binaryify/neteasecloudmusicapi
https://github.com/quodlibet/mutagen