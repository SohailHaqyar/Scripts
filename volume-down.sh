#!/bin/bash

# Get the current volume
current_volume=$(playerctl volume)

# Increase the volume by 0.1
new_volume=$(echo "$current_volume - 0.1" | bc)

# Set the new volume
playerctl volume "$new_volume"

echo "Volume decreased to $new_volume"
