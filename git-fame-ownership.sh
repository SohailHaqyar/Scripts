#!/bin/sh
email_file="emails.txt"
> "$email_file"  

declare -A email_count
total_files=0
while IFS= read -r file; do
  echo "Proccessing file: $file"
    git fame -esnwMC --incl "$file" | tr '/' '|' \
      | awk -F '|' '(NR>6 && $6>=30) {print $2}' >> "$email_file"
    ((total_files++))
done

email_counts=$(sort "$email_file" | uniq -c | sort -nr)

echo "Email counts with percentages based on total files ($total_files):"
while read -r count email; do
    percentage=$(echo "scale=2; ($count / $total_files) * 100" | bc)
    echo "$email: $count ($percentage%)"
done <<< "$email_counts"



