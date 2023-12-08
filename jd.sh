#!/bin/sh
# Jump Directory
path=$(find ~ ~/Desktop/work ~/.config ~/scripts ~/Desktop -mindepth 1 -maxdepth 1 | fzf)
echo "$path"
cd "$path"
echo "Yay or nay"
