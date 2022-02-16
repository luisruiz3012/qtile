#!/bin/sh

# System icons
picom &
udiskie -t &
nm-applet &
volumeicon &
cbatticon -u 5 &
nitrogen --restore &
xrandr --output HDMI1 --auto

