#!/bin/bash
cookie_BDUSS="cookie BDUSS" # BDUSS
cookie_BAIDUID="cookie BAIDUID，引号不转义" # BAIDUID

curl --cookie "BDUSS=${cookie_BDUSS};BAIDUID=${cookie_BAIDUID};" "https://sp0.baidu.com/6_R1fD_bAAd3otqbppnN2DJv/Pic/upload?pid=super&app=skin&logid=2915142959" -F "file=@$1" | jq -r ".data.pic_water" | sed "s/http/https/"
