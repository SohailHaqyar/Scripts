#!/bin/sh
movie=$(cat ~/movies.txt | awk 'BEGIN{srand()} {a[NR]=$0} END{print a[int(rand()*NR)+1]}')
cowsay "Now playing $movie"
curl -s "http://artscene.textfiles.com/vt100/$movie" | pv -q -L 9600
