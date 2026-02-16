#!/bin/bash

echo "===== PRE-DEPLOYMENT HEALTH CHECK ====="

FAIL=0

# CPU Usage
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
echo "CPU Usage: $CPU%"
if (( $(echo "$CPU > 85" | bc -l) )); then
  echo "❌ High CPU usage"
  FAIL=1
fi

# Memory
MEM=$(free | awk '/Mem:/ {printf("%.0f"), $3/$2 * 100}')
echo "Memory Usage: $MEM%"
if [ "$MEM" -gt 85 ]; then
  echo "❌ High memory usage"
  FAIL=1
fi

# Disk
DISK=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
echo "Disk Usage: $DISK%"
if [ "$DISK" -gt 90 ]; then
  echo "❌ Disk almost full"
  FAIL=1
fi

# Required Port Check
PORT=8080
if lsof -i:$PORT >/dev/null ; then
  echo "❌ Port $PORT already in use"
  FAIL=1
else
  echo "✅ Port $PORT is free"
fi

# Service Check
SERVICE=nginx
if systemctl is-active --quiet $SERVICE; then
  echo "✅ $SERVICE running"
else
  echo "❌ $SERVICE not running"
  FAIL=1
fi

# Final Decision
if [ $FAIL -eq 1 ]; then
  echo "🚫 Deployment BLOCKED"
  exit 1
else
  echo "✅ System ready for deployment"
fi
