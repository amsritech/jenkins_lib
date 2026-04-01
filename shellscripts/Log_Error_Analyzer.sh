#!/bin/bash
set -euo pipefail

log_file="${1:-app.log}"

if [ ! -f "$log_file" ]; then
    echo "Error: Log file '$log_file' not found!"
    exit 1
fi

# Count errors
error_count=$(grep -i -c "ERROR" "$log_file")
echo "Total number of errors: $error_count"

# Top 3 most frequent errors
echo "Top 3 errors:"
top3_errors=$(grep -i "ERROR" "$log_file" | sort | uniq -c | sort -nr | head -n 3)
echo "$top3_errors"