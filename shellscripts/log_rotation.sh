#!/bin/bash
# log_rotate_ts.sh
set -euo pipefail

# Config
LOG_DIR="${1:-/var/log/myapp}"
LOG_FILE="${2:-app.log}"
BACKUP_COUNT="${3:-5}"

# Ensure log directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "Error: Log directory '$LOG_DIR' does not exist!"
    exit 1
fi

LOG_PATH="$LOG_DIR/$LOG_FILE"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Only rotate if the log file exists
if [ -f "$LOG_PATH" ]; then
    # Compress the current log with timestamp
    gzip -c "$LOG_PATH" > "$LOG_PATH.$TIMESTAMP.gz"
    
    # Empty the current log
    : > "$LOG_PATH"

    echo "✅ Log rotated: $LOG_PATH -> $LOG_PATH.$TIMESTAMP.gz"

    # Cleanup old backups, keep only the latest BACKUP_COUNT files
    old_backups=($(ls -1t "$LOG_DIR/$LOG_FILE."*.gz 2>/dev/null))
    if [ "${#old_backups[@]}" -gt "$BACKUP_COUNT" ]; then
        for file in "${old_backups[@]:$BACKUP_COUNT}"; do
            rm -f "$file"
            echo "🗑️ Deleted old backup: $file"
        done
    fi
else
    echo "Log file '$LOG_PATH' not found. Skipping rotation."
fi