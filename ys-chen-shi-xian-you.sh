#!/bin/bash
k(){
    xdotool key $1
}
n(){
    if [ $1 == 1 ]
    then
        if [ $2 == 1 ]
        then
        xdotool key Z
        elif [ $2 == 2 ]
        then
        xdotool key X
        elif [ $2 == 3 ]
        then
        xdotool key C
        elif [ $2 == 4 ]
        then
        xdotool key V
        elif [ $2 == 5 ]
        then
        xdotool key B
        elif [ $2 == 6 ]
        then
        xdotool key N
        elif [ $2 == 7 ]
        then
        xdotool key M
        fi
    elif [ $1 == 2 ]
    then
        if [ $2 == 1 ]
        then
        xdotool key A
        elif [ $2 == 2 ]
        then
        xdotool key S
        elif [ $2 == 3 ]
        then
        xdotool key D
        elif [ $2 == 4 ]
        then
        xdotool key F
        elif [ $2 == 5 ]
        then
        xdotool key G
        elif [ $2 == 6 ]
        then
        xdotool key H
        elif [ $2 == 7 ]
        then
        xdotool key J
        fi
    elif [ $1 == 3 ]
    then
        if [ $2 == 1 ]
        then
        xdotool key Q
        elif [ $2 == 2 ]
        then
        xdotool key W
        elif [ $2 == 3 ]
        then
        xdotool key E
        elif [ $2 == 4 ]
        then
        xdotool key R
        elif [ $2 == 5 ]
        then
        xdotool key T
        elif [ $2 == 6 ]
        then
        xdotool key Y
        elif [ $2 == 7 ]
        then
        xdotool key U
        fi
    fi
}
s(){
    sleep $1s
}
b(){
    sleep $(echo "scale=2; $1*0.27" | bc | awk '{printf "%.2f", $0}')s
}
b2(){
    sleep $(echo "scale=2; $1*0.16" | bc | awk '{printf "%.2f", $0}')s
}
s 0.7
n 2 2
n 1 2
b 2
n 2 3
b 2
n 2 5
n 1 5
b 3
n 2 2
b 1
n 2 3
n 1 3
b 2
n 2 6
b 2
n 2 5
n 1 5
b 1
n 2 6
b 0.5
n 2 5
b 0.5
n 2 3
b 1
n 2 1
b 1
n 2 2
n 1 2
b 2
n 2 3
b 2
n 1 6
n 1 2
b 3
n 2 3
b 1
n 2 2
n 1 2
b 1
n 2 3
b 1
n 2 5
b 1
n 2 2
b 1
n 2 3
n 1 3
b 1
n 2 5
b 0.5
n 2 3
b 0.5
n 2 2
b 1
n 2 1
b 1
n 3 2
n 2 2
b 2
n 3 3
b 2
n 3 5
n 2 5
b 3
n 3 2
b 1
n 3 3
n 2 3
b 2
n 3 6
b 2
n 3 5
n 2 5
b 1
n 3 6
b 0.5
n 3 5
b 0.5
n 3 3
b 1
n 3 1
b 1
n 3 2
n 2 2
b 2
n 3 3
b 2
n 2 6
n 1 6
b 3
n 3 3
b 1
n 3 2
n 2 2
b 1
n 3 3
b 1
n 3 5
b 1
n 3 6
b 1
n 3 3
n 2 3
b 3
n 3 5
b 0.5
n 3 6
b 0.5
n 3 5
b 0.5
n 3 6
n 2 6
b 3
n 3 3
b2 1
n 3 2
n 2 2
b2 1
n 3 3
b2 0.5
n 3 2
b2 0.5
n 3 1
b2 1
n 2 6
b2 1
n 2 5
n 1 5
b2 1
n 2 6
b2 2
n 3 3
b2 1
n 3 2
n 2 2
b2 1
n 3 3
b2 0.5
n 3 2
b2 0.5
n 3 1
b2 1
n 2 6
b2 1
n 2 5
n 1 5
b2 1
n 2 6
b2 2
n 3 1
b2 1
n 3 2
n 2 2
b2 3
n 3 2
b2 1
n 3 2
n 2 2
b2 1
n 3 3
b2 0.5
n 3 2
b2 0.5
n 3 1
b2 1
n 2 6
b2 1
n 3 1
n 2 1
b2 2
n 2 3
b2 2
n 2 5
b2 2
n 3 3
b2 2
n 3 2
n 2 2
b2 1
n 3 3
b2 0.5
n 3 2
b2 0.5
n 3 1
b2 1
n 2 6
b2 1
n 2 5
n 1 5
b2 1
n 2 6
b2 2
n 3 3
b2 1
n 3 2
n 2 2
b2 1
n 3 3
b2 0.5
n 3 2
b2 0.5
n 3 1
b2 1
n 2 6
b2 1
n 2 5
n 1 5
b2 1
n 2 6
b2 2
n 3 1
b2 1
n 3 2
b2 1.3
n 3 2
b2 1.3
n 3 2
b2 1.3
n 3 3
b2 1.3
n 3 3
b2 1.3
n 3 3
b2 1.3

