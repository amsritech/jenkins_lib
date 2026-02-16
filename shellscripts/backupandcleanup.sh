#!/bin/bash

#########################################
# CONFIGURATION
#########################################

LOG_DIR="/var/log/myapp"
BACKUP_DIR="/backup/logs"
TEMP_DIR="/tmp"
DEPLOY_DIR="/opt/app/releases"

DAYS_TO_KEEP_LOGS=7
DAYS_TO_KEEP_BACKUPS=30
RELEASES_TO_KEEP=5

DATE=$(date +%F)
REPORT="/var/log/cleanup_report_$DATE.log"

mkdir -p $BACKUP_DIR

echo "===== CLEANUP STARTED $DATE =====" >> $REPORT

#########################################
# 1. BACKUP LOG FILES
#########################################

echo "Backing up logs..." >> $REPORT

tar -czf $BACKUP
