#!/bin/bash

if [ $# -eq 0 ]; then
    echo -e "\033[1;31mNo argument. Use bili --help to view usage.\033[0m"
    exit
fi

if [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
    echo "Bilibili mpv wrapper by YidaozhanYa"
    echo "Usage: bili [video url] [options]"
    echo ""
    echo "--browser=(brave, chrome, chromium, edge, firefox, opera, safari, vivaldi)"
    echo "(Default: firefox)"
    echo ""
    echo "--codec=(avc, hevc, av1)"
    echo "(Default: hevc)"
    echo ""
    echo "--size=(360p, 480p, 720p, 1080p, 4k or resolution like 1920x1080)"
    echo "(Default: 1080p)"
    echo ""
    echo "--danmaku_resolution=(resolution like 1920x1080)"
    echo "(Default: 2000x900, smaller danmaku resolution can increase font size)"
    echo ""
    echo "--driver=(iHD, nvidia, i965, radeonsi, etc.) (optional, available drivers are in /usr/lib/dri)"
    echo "(Default: same as global settings)"
    echo ""
    echo "--mpv-args=(arguments to pass to mpv) (optional)"
    echo ""
    echo "-h, --help (show this message)"
    echo ""
    echo "-v, --verbose (show all outputs)"
    echo ""
    echo "Requirements: yt-dlp, jq, python-biliass, mpv or mplayer, any browser with bilibili account logged"
    exit
fi

for arg in ${@}; do
    YTDLP_ARGS="--cookies-from-browser firefox"
    if [ "$arg" = "--verbose" ] || [ "$arg" = "-v" ]; then
        VERBOSE='true'
    fi
    if echo "$arg" | grep -w "\-\-browser" &>/dev/null; then
        YTDLP_ARGS="--cookies-from-browser $(echo $arg | sed "s/--browser=//")"
    fi
    if echo "$arg" | grep -w "\-\-driver" &>/dev/null; then
        export LIBVA_DRIVER_NAME="$(echo $arg | sed "s/--driver=//")"
        echo -e "\033[1;34m::\033[1;0m Using ${LIBVA_DRIVER_NAME} VA-API driver\033[0m"
    fi
    if echo "$arg" | grep -w "\-\-mpv\-args" &>/dev/null; then
        MPV_ARGS="$(echo $arg | sed "s/--mpv-args=//")"
    fi
    FORMAT_FILTER='"mp4/bestvideo[vcodec^=hev1]"'
    if echo "$arg" | grep -w "\-\-codec" &>/dev/null; then
        if [ "$arg" = "--codec=hevc" ]; then
            FORMAT_FILTER='"mp4/bestvideo[vcodec^=hev1]"'
        elif [ "$arg" = "--codec=avc" ]; then
            FORMAT_FILTER='"mp4/bestvideo[vcodec^=avc1]"'
        elif [ "$arg" = "--codec=avc" ]; then
            FORMAT_FILTER='"mp4/bestvideo[vcodec^=av01]"'
        else
            echo -e "\033[1;31mUnknown codec $arg!\033[0m"
            exit
        fi
    fi
    SIZE='x1080'
    RESOLUTION='2000x900'
    if echo "$arg" | grep -w "\-\-size" &>/dev/null; then
        if [ "$arg" = "--size=360p" ]; then
            SIZE='x360'
        elif [ "$arg" = "--size=480p" ]; then
            SIZE='x480'
        elif [ "$arg" = "--size=720p" ]; then
            SIZE='x720'
        elif [ "$arg" = "--size=1080p" ]; then
            SIZE='x1080'
        elif [ "$arg" = "--size=4k" ]; then
            SIZE='4096x'
        else
            if echo "$arg" | grep -w "x" &>/dev/null; then
                SIZE="$(echo $arg | sed "s/--size=//")"
            else
                echo -e "\033[1;31mUnknown video size $arg!\033[0m"
                exit
            fi
        fi
    fi
    if echo "$arg" | grep -w "danmaku_resolution" &>/dev/null; then
        RESOLUTION="$(echo $arg | sed "s/--danmaku_resolution=//")"
    fi
done

URL="$(echo "$1" | awk -F'?' '{print $1}')"
BVID="$(echo "$URL" | awk -F'/video/' '{print $2}' | awk -F'/' '{print $1}')"

echo -e "\033[1;34m::\033[1;0m Creating cache folder...\033[0m"
mkdir -p "/tmp/$BVID"

echo -e "\033[1;34m::\033[1;0m Downloading audio offline cache...\033[0m"
if [ "$VERBOSE" = "true" ]; then
    CMD="yt-dlp ${YTDLP_ARGS} --verbose --no-playlist -f m4a/bestaudio -o /tmp/${BVID}/audio.m4s ${URL}"
else
    CMD="yt-dlp ${YTDLP_ARGS} --quiet --no-playlist -f m4a/bestaudio -o /tmp/${BVID}/audio.m4s ${URL}"
fi
eval "${CMD}"

echo -e "\033[1;34m::\033[1;0m Parsing danmaku ${BVID}...\033[0m"
CID="$(curl -s "https://api.bilibili.com/x/player/pagelist?bvid=${BVID}&jsonp=jsonp" | jq '.data[0].cid')"
echo -e "\033[1;34m::\033[1;0m Downloading danmaku ${CID}...\033[0m"
DANMAKU_POOL="https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=${CID}&segment_index=1"
curl -s "$DANMAKU_POOL" -o "/tmp/${BVID}/seg.so"

echo -e "\033[1;34m::\033[1;0m Converting danmaku to ASS format...\033[0m"
biliass "/tmp/${BVID}/seg.so" -f protobuf -s "$RESOLUTION" -o "/tmp/${BVID}/danmaku.ass"

echo -e "\033[1;34m::\033[1;0m Playing streamed video...\033[0m"
if [ "$VERBOSE" = "true" ]; then
    CMD="yt-dlp ${YTDLP_ARGS} --no-playlist -f ${FORMAT_FILTER} --verbose -o - ${URL} | mpv - --audio-file=/tmp/${BVID}/audio.m4s --sub-file=/tmp/${BVID}/danmaku.ass --hwdec=auto ${MPV_ARGS}"
else
    CMD="yt-dlp ${YTDLP_ARGS} --no-playlist -f ${FORMAT_FILTER} --quiet -o - ${URL} | mpv - --audio-file=/tmp/${BVID}/audio.m4s --sub-file=/tmp/${BVID}/danmaku.ass --hwdec=auto ${MPV_ARGS} 1>/dev/null"
fi
eval "${CMD}"

echo -e "\033[1;34m::\033[1;0m Cleaning up...\033[0m"
rm -rf "/tmp/${BVID}"
