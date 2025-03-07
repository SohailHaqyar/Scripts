#!/bin/bash

# Get the list of connected monitors
monitor_count=$(wlr-randr --json | jq 'keys | length')
if [ "$monitor_count" -eq 2 ]; then
        # Disable eDP-1 and enable the other monitor
        notify-send "Big man detected, switching fast boy off..."
        hyprctl keyword monitor "eDP-1, disable"
fi
