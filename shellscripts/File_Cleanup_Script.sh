#!/bin/bash
set -euo pipefail

# Usage: ./File_Cleanup_Script.sh /path/to/directory 30
directory="${1:-.}"
days="${2:-30}"

if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' not found!"
    exit 1
fi

echo "Cleaning up .log files in '$directory' older than $days days..."

deleted_files=$(find "$directory" -type f -name "*.log" -mtime +"$days" -print -delete || true)

if [ -z "$deleted_files" ]; then
    echo "No files older than $days days to delete."
else
    echo "Deleted files:"
    echo "$deleted_files"
fi

echo "Cleanup completed."