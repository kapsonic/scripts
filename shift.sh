#!/bin/bash

function show_time () {
    num=$1
    min=0
    hour=0
    day=0
    if((num>59));then
        ((sec=num%60))
        ((num=num/60))
        if((num>59));then
            ((min=num%60))
            ((num=num/60))
            if((num>23));then
                ((hour=num%24))
                ((day=num/24))
            else
                ((hour=num))
            fi
        else
            ((min=num))
        fi
    else
        ((sec=num))
    fi
    echo "$hour":"$min":"$sec"
}

upTimeSec=$(cut -d '.' -f 1 </proc/uptime)
a=$((10#$upTimeSec))
NHRS=32400
time=`expr $NHRS - $a`

outTime=$(date +%H:%M:%S --date "+$time seconds")
inTime=$(date +%H:%M:%S --date "-$upTimeSec seconds")
echo "$(date +%d-%m-%Y)"
echo "============================"
echo "IN TIME: $inTime"
echo "OUT TIME: $outTime"
echo "TIME LEFT: $(show_time $time)"
