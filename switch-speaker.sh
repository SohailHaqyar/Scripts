#!/bin/bash

# Get list of sinks (outputs)
sinks=$(pactl list short sinks | cut -f2)

# Get current default sink
current=$(pactl get-default-sink)

# Convert to array
mapfile -t sink_array <<< "$sinks"

# Find current sink index
for i in "${!sink_array[@]}"; do
    if [[ "${sink_array[$i]}" == "$current" ]]; then
        current_index=$i
        break
    fi
done

# Calculate next sink index
next_index=$(( (current_index + 1) % ${#sink_array[@]} ))

# Set next sink as default
pactl set-default-sink "${sink_array[$next_index]}"
