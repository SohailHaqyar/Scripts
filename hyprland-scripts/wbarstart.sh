#!/usr/bin/env sh

killall waybar
waybar --config /home/kaka/.config/waybar/config.jsonc --style /home/kaka/.config/waybar/style.css > /dev/null 2>&1 &

