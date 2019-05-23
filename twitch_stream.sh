#!/bin/bash
cmd=$(raspivid -t 0 -fps 15 -b 2000000 -o - | avconv -v error -i - -vcodec copy -an -r 30 -g 30 -bufsize 2000000 -pix_fmt yuv420p -f flv rtmp://live.justin.tv/app/live_425990991_XDBw1sG55SByo9a262At43ELkWeHo0 2> /home/pi/fish_stream/logs/twitch_err.log)

until $cmd ; do
        echo "restarting ffmpeg command..."
        sleep 2
done
