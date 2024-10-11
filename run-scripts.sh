#!/bin/sh
name=$(find ~/scripts ~/.local/bin ~/.local/share/bin -executable -type f  | fzf)
echo "Running script $name"
exec $name
