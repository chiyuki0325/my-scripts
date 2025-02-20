#!/bin/bash
#$1 json $2 exported assets folder $3 output path
#use catalog.py in phisap to get a decrypted catalog.json
JSON="`cat "$1"`"
printf "$JSON" | jq -r 'keys[]' | while read item;do
outpath="`printf "$JSON" |jq -rc ".\\"${item}\\""`"
if [[ "$outpath" =~ "Assets" ]];then
    echo "Exporting $outpath"
    pushd "$2/${item}_export/CAB-"* 1>/dev/null
        if [ -f "illustration.png" ];then
            install -D "illustration.png" "$3/$outpath"
        elif [ -f "illustrationBlur.png" ];then
            install -D "illustrationBlur.png" "$3/$outpath"
        elif [ -f "Illustration~1.png" ];then
            install -D "Illustration~1.png" "$3/$outpath"
        elif [ -f "IllustrationBlur~1.png" ];then
            install -D "IllustrationBlur~1.png" "$3/$outpath"
        else
            filename="`basename "$outpath" | sed "s/.json//g"`"
            if [ "$filename" = "IllustrationBlur.png" ];then
                if [ -f "Illustration.png" ];then #fix assetstudio error
                    install -D "Illustration.png"  "$3/$outpath"
                fi
            else
                install -D "$filename"  "$3/$outpath"
            fi
        fi
    popd 1>/dev/null
fi
done
