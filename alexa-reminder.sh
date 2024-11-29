#!/bin/bash
# notify-send "Time for a break." "I'm going to lock your screen. Future Sohail you better not ignore me. I'm watching you." -t 5000
# sleep 2s 
#
# # Lock the screen for a minute without letting the user unlock
#
# paplay /usr/share/sounds/urban-street-thug-life-music-gfx-sounds-1-3-00-11.mp3
# swaylock 
#
#
is_locked() {
    pgrep swaylock > /dev/null
    return $?
}

# Kill any existing swaylock instances
pkill swaylock

# Create a temporary file to store the lock time
LOCK_FILE="/tmp/screen_lock_time"

# Store the current timestamp
date +%s > "$LOCK_FILE"

# Send initial notification
notify-send "Screen Lock" "Screen will be locked for 1 minute. Take a break!"

# Start swaylock in the background
swaylock &

# Start a loop to prevent unlocking
while true; do
    # Check if swaylock is still running
    if ! is_locked; then
        # Get the lock start time
        START_TIME=$(cat "$LOCK_FILE")
        CURRENT_TIME=$(date +%s)
        ELAPSED_TIME=$((CURRENT_TIME - START_TIME))
        
        # If less than 60 seconds have passed, restart swaylock
        if [ $ELAPSED_TIME -lt 60 ]; then
            # Calculate remaining time
            REMAINING=$((60 - ELAPSED_TIME))
            
            # Notify remaining time and restart swaylock
            notify-send "Screen Lock" "$REMAINING seconds remaining"
            swaylock &
        else
            # Clean up and exit if enough time has passed
            rm -f "$LOCK_FILE"
            notify-send "Break Over" "You can now continue working. Next break in 25 minutes."
            exit 0
        fi
    fi
    
    # Sleep for a short interval before checking again
    sleep 1
done
