#!/bin/bash

# Check if tmux session already exists
SESSION="gdiff_session"
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  # Create a new tmux session if it doesn't exist
  tmux new-session -d -s $SESSION
fi

# Read file names from stdin
while IFS= read -r file; do
  # Create a new tmux window for each file
  tmux new-window -t $SESSION -n "$(basename "$file")"
  
  # Send the command to open Neovim and run Gdiff
  tmux send-keys -t $SESSION "nvim $file -c 'Gdiff master' let g:gitgutter_diff_base = '$REVIEW_BASE'\"" C-m 
done

# Switch to the first window
tmux select-window -t $SESSION:1

# Attach to the tmux session
tmux attach -t $SESSION
