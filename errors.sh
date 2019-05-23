#!/bin/bash

/bin/echo 'running error script'

if /bin/grep 'Input/output error' /home/pi/fish_stream/logs/twitch_err.log; then
  /bin/echo exists
  sudo /sbin/shutdown -r now
elif  /bin/grep 'Error writing trailer'  /home/pi/fish_stream/logs/twitch_err.log; then
  /bin/echo exists
  sudo /sbin/shutdown -r now
else
  /bin/echo not found
fi
