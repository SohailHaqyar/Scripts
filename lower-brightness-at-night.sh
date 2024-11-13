#!/bin/bash

while true; do
  current_hour=$(date +"%H")
  current_brightness=$(brightnessctl get)

  if [ "$current_hour" -ge 8 ] && [ "$current_hour" -lt 20 ] ; then
        notify-send "Let there be light..."
        killall wlsunset
        brightnessctl set 255
    else
      notify-send "Lowering brightness.."
      brightnessctl set 20
      wlsunset & 
  fi
  sleep 1800
done
