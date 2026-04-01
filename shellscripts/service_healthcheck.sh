#!/bin/bash
set -euo pipefail

service_name="${1:-my_service}"

# Check if service exists
if ! systemctl list-unit-files | grep -qw "$service_name.service"; then
    echo "❌ Service '$service_name' does not exist!"
    exit 1
fi

# Check if the service is active
if systemctl is-active --quiet "$service_name"; then
    echo "✅ Service '$service_name' is running."
else
    echo "❌ Service '$service_name' is NOT running! Attempting restart..."
    if systemctl restart "$service_name"; then
        echo "✅ Service '$service_name' restarted successfully."
    else
        echo "❌ Failed to restart service '$service_name'."
        exit 1
    fi
fi