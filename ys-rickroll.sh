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
    sleep $(echo "scale=2; $1*0.26" | bc | awk '{printf "%.2f", $0}')s
}
b2(){
    sleep $(echo "scale=2; $1*0.12" | bc | awk '{printf "%.2f", $0}')s
}
alias K="k"
alias B="b"

qianzou(){
k V;k N;k A;k Q;b 3 #1
k B;k M;k S;k W;b 3 #2
k B;b 2 #-5
k C;k B;k M;k W;b 3 #2
k C;k N;k A;k E;b 3 #3
k T;b2 1;k R;b2 1;k E;b2 1;k Q;b2 1 #5431
k V;k N;k A;k Q;b 3 #1
k B;k M;k S;k W;b 3 #2
k B;b 2 #-5
#
k C;k B;k M;b 3
k C;k N;k A;b 2
k G;b2 1;k G;b2 1;k T;b2 1;k R;b2 1;k E;b2 1;k Q;b2 1 #-5 -5 5431
##
k V;k N;k A;k Q;b 3 #1
k B;k M;k S;k W;b 3 #2
k B;b 2 #-5
k C;k B;k M;k W;b 3 #2
k C;k N;k A;k E;b 3 #3
k T;b2 1;k R;b2 1;k E;b2 1;k Q;b2 1 #5431
k V;k N;k A;k Q;b 3 #1
k B;k M;k S;k W;b 3 #2
k B;b 2 #-5
#
k C;k B;k M;b 3
k C;k N;k A;b 3
k C;b 2
}

part1(){
k V ;k N;k A;b 2 #bz
k H; b 1 #6
k V ;k N; k A;k J;b 1 #7
k Q;b 1     ;k Q;b 1; #11
k V ;k N; k A;k W;b 1 #2
k J;b 1    ; #7
k C;k B;k M;b2 3;#伴奏
k H;b2 1;   k G;b2 3
k C;k B;k M;b2 7;#伴奏
k C;k B;k M;b 2;#伴奏

k V ;k N;k A;b 1 #bz
k H; b 1 ;k H; b 1 #6 6
k V ;k N; k A;k J;b 1 #7
k Q;b 1     ;k H;b 1; #1 6
k V ;k N;k A;b 1 #bz
k G; b 1;# 5
k V;k N;k A;k T;b 2; #+5
k T;b 1; #+5
k C;k B;k M;k W;b 2;#伴奏 2
k C;k B;k M;b 3;#伴奏
}
part1_2(){
k V ;k N;k A;b 1 #bz
k H; b 1 ;k H; b 1 #6 6
k V ;k N; k A;k J;b 1 #7
k Q;b 1     ;k H;b 1; #1 6
k V ;k N; k A;k Q;b 1 #1
k W;b 1    ; #2
k C;k B;k M;b 1;#伴奏
k J;b 1; k H;b 1; #76
k C;k B;k M;k J;b 1;#7
b2 1; k H; b2 1;
k G;b 1;
k C;k B;k M;b 2;#伴奏

k V ;k N;k A;b 1 #bz
k H; b 1 ;k H; b 1 #6 6
k V ;k N; k A;k J;b 1 #7
k Q;b 1     ;k H;b 1; #1 6
k V ;k N; k A;k G;b 2 #5
k V;k N;k A;k W;b 1;#2
k W;b 1;k W;b 1; # 22
k C;k B;k M;k E;b 1;#3
k W ;b 2;
k C;k B;k M;b 2;#伴奏
}

part1_3(){
k V;k N ;k A;k Q;b 3; #1 . .
k V ;k N;k A;b 2 #bz
k W;b 1;#2
k V;k N ;k A;k E;b 1; #3
k Q;b 1;#2   ######
k C;k B;k M;k W;b 1;#2
k W;b 1;k W;b 1; # 22
k C;k B;k M;k E;b 1;#3
k W;b 1;k G;b 1; # 2 5
k C;k B;k M;k G;b 2;#5 bz

k V ;k N;k A;b 3 #bz
k V ;k N;k A;b 1 #bz
k H;b 1;k J;b 1;# 67
k V;k N ;k A;k Q;b 1; #1
k H;b 1; #6
k V ;k N;k A;b 1 #bz
k W;b 1;k E;b 1;# 23
k B;k M;k S;k W;b 3 #2
k B;k M;k S;k G;b2 1;#5
k H;b2 1;k Q;b2 1;k H b2 1;#616
}

part2(){
k V;k N;k A;k E;b2 3;#3
k V;k N;k A;k E;b2 3;#3
k B;k M;k S;k W;b2 5; #2
k B ;b2 1;k M;k S;k G;b2 1;#5
k H;b2 1;k Q;b2 1;k H b2 1;#616

k C;k B;k M;k W;b2 3;#2
k C;k B;k M;k W;b2 3;#2
k C;k N;k A;k Q;b2 3;#1
k J;b2 1;k H;b2 1;#76
k C ;k N;k A;k G;b2 1;#5
k H;b2 1;k Q;b2 1;k H ;b2 1;#616
}
part2_2(){
k V;k N;k A;k Q;b2 3; #1
k V;k N;k A;b2 1;#bz
k W;b 1; #2
k B;k M;k S;k J;b 2; #7
k H;b 1; #6
k B;k G;b 1; #6
k G;b 1; #6

k C;k B;k M;k W;b 1;#2
k C;k B;k M;b 1;#bz
k Q;b 2;#1
k C;k N;k A;b 1; #bz
k C;k N;k A;b 1; #bz
k C ;k N;k A;k G;b2 1;#5
k H;b2 1;k Q;b2 1;k H ;b2 1;#616
}

part3(){
k V;k N;k A;k E;b2 3;#3
k V;k N;k A;k E;b2 3;#3
k B;k M;k S;k W;b2 5; #2
k B ;b2 1;k M;k S;k G;b2 1;#5
k H;b2 1;k Q;b2 1;k H b2 1;#616
k C;k B;k M;k T;b 1 #+5
k C;k B;k M;b 1;#bz
k J;b 1;#7
k C;k N;k A;k Q;b 1;#1
b2 1; k J;b2 1;k H;b 1;#76
k C ;k N;k A;k G;b2 1;#5
k H;b2 1;k Q;b2 1;k H ;b2 1;#616



k V;k N;k A;k Q;b2 3; #1
k V;k N;k A;b2 1;#bz
k W;b 1; #2
k B;k M;k S;k J;b 2; #7
k H;b 1; #6
k B;k G;b 1; #6
k G;b 1; #6

k C;k B;k M;k W;b 1;#2
k C;k B;k M;b 1;#bz
k Q;b 2;#1
k C;k N;k A;b 1; #bz
k C;k N;k A;b 1; #bz
b 2;
}

echo "Never Gonna Give You Up - Rick Astley"
echo "Ported to Linux by YidaozhanYa"
s 0.7
qianzou
part1
part1_2
part1_3
part2
part2_2
part3
