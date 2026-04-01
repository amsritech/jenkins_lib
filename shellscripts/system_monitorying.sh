#!/bin/bash
# system_monitoring.sh
set -euo pipefail

# Thresholds
DISK_THRESHOLD=80
MOUNT_POINT="${1:-/}"

# Disk usage
Disk_usage=$(df "$MOUNT_POINT" | awk 'NR==2 {print $5}' | sed 's/%//')
echo "Disk Usage: $Disk_usage%"

if [ "${Disk_usage%.*}" -gt "$DISK_THRESHOLD" ]; then
    echo "⚠️ Warning: Disk usage is above ${DISK_THRESHOLD}%!"
fi

# CPU usage
CPU_usage=$(top -bn1 | awk -F',' '/Cpu\(s\)/ {print 100 - $8"%"}')
echo "CPU Usage: $CPU_usage"

# Memory usage
Memory_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
echo "Memory Usage: $Memory_usage"