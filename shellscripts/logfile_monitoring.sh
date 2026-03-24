#!/usr/bin/env bash

# ---------- Configuration ----------
# List of log files to monitor (space‑separated)
LOG_FILES=(
 "/var/log/syslog"
 "/var/log/nginx/error.log"
 # add more paths as needed
)

# Error pattern(s) to watch for (extended regex)
# Example: match "ERROR", "FAIL", or any line containing "exception"
ERROR_PATTERN="ERROR|FAIL|exception"

# Action to take when a match is found
# Here we just echo with a timestamp; replace with mail, Slack, etc.
alert() {
 local file="$1"
 local line="$2"
 echo "$(date '+%Y-%m-%d %H:%M:%S') $file: $line"
 # Example: send to Slack
 # curl -X POST -H 'Content-type: application/json' \
 # --data "{\"text\":\"$file: $line\"}" https://hooks.slack.com/services/...
}

# ---------- Main logic ----------
# Build the tail command to follow all files
tail_cmd="tail -F"
for f in "${LOG_FILES}"; do
 tail_cmd+=" \"$f\""
done

# Run tail and pipe each line through while loop
eval $tail_cmd | while IFS= read -r line; do
 if echo "$line" | grep -Eiq "$ERROR_PATTERN"; then
 # Extract the source file name from tail's output (if multiple files)
 # tail prefixes each line with "filename: " when following >1 file
 if [[ "$line" =~ ^(+):\ (.*) ]]; then
 src="${BASH_REMATCH}"
 msg="${BASH_REMATCH}"
 else
 src="unknown"
 msg="$line"
 fi
 alert "$src" "$msg"
 fi
done
