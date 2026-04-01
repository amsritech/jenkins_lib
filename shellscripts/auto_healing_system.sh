#!/bin/bash
# auto_heal_monitor.sh
# Monitors disk, CPU, memory and cleans old logs if disk usage > threshold
set -euo pipefail

# Configurable parameters
MOUNT_POINT="${1:-/}"                 # Disk mount to monitor
DISK_THRESHOLD="${2:-80}"             # Disk usage threshold %
LOG_DIR="${3:-/var/log/myapp}"        # Directory to cleanup logs from
LOG_AGE="${4:-7}"                      # Days threshold for logs

echo "🔹 System Monitoring & Auto Cleanup Script"
echo "Mount point: $MOUNT_POINT"
echo "Disk threshold: $DISK_THRESHOLD%"
echo "Log directory: $LOG_DIR"
echo "Log age threshold: $LOG_AGE days"
echo "--------------------------------------"

# 1️⃣ Collect system metrics
Disk_usage=$(df "$MOUNT_POINT" | awk 'NR==2 {print $5}' | sed 's/%//')
CPU_usage=$(top -bn1 | awk -F',' '/Cpu\(s\)/ {print 100 - $8"%"}')
Memory_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')

# 2️⃣ Print metrics
echo "Disk Usage: $Disk_usage%"
echo "CPU Usage: $CPU_usage"
echo "Memory Usage: $Memory_usage"

# 3️⃣ Conditional cleanup if disk usage exceeds threshold
deleted_files=""
if [ "${Disk_usage%.*}" -gt "$DISK_THRESHOLD" ]; then
    echo "⚠️ Disk usage is above $DISK_THRESHOLD%, running cleanup of old logs..."

    if [ -d "$LOG_DIR" ]; then
        deleted_files=$(find "$LOG_DIR" -type f -name "*.log" -mtime +"$LOG_AGE" -print -delete || true)
        if [ -z "$deleted_files" ]; then
            echo "No logs older than $LOG_AGE days to delete."
        else
            echo "Deleted files:"
            echo "$deleted_files"
        fi
    else
        echo "⚠️ Log directory '$LOG_DIR' does not exist. Skipping cleanup."
    fi
else
    echo "Disk usage is below threshold. No cleanup needed."
fi

echo "--------------------------------------"
echo "✅ Monitoring & cleanup complete."