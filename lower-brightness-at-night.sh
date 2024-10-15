#!/bin/bash

while true; do
  current_hour=$(date +"%H")
  current_brightness=$(brightnessctl get)

  if [ "$current_hour" -ge 20 ]; then
    if [ "$current_brightness" -gt 20 ]; then
      notify-send "Lowering brightness.."
      brightnessctl set 20
      wlsunset & 
    fi
  else
    if [ "$current_brightness" -lt 255 ]; then
      notify-send "Let there be light..."
      pkill wlsunset
      brightnessctl set 255
    fi
  fi
  sleep 1800
done
