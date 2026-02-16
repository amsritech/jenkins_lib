#!/bin/bash

# Script to automate environment setup and configuration

# Check if environment argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 {dev|test|prod}"
  exit 1
fi

ENV=$1

echo "Starting setup for $ENV environment..."

# Update package list and install common packages
sudo apt-get update
sudo apt-get install -y curl git jq

# Set environment-specific variables and configurations
case $ENV in
  dev)
    export APP_DEBUG=true
    export DB_HOST=dev-db.example.com
    export LOG_LEVEL=debug
    echo "Configured development environment variables."
    ;;
  test)
    export APP_DEBUG=false
    export DB_HOST=test-db.example.com
    export LOG_LEVEL=info
    echo "Configured testing environment variables."
    ;;
  prod)
    export APP_DEBUG=false
    export DB_HOST=prod-db.example.com
    export LOG_LEVEL=error
    echo "Configured production environment variables."
    ;;
  *)
    echo "Invalid environment: $ENV"
    exit 1
    ;;
esac

# Create necessary directories
mkdir -p /var/myapp/logs
mkdir -p /var/myapp/data

echo "Directories created."

# Set permissions
sudo chown -R $USER:$USER /var/myapp

echo "Permissions set."

# Additional setup steps can be added here, like starting services or configuring files

echo "$ENV environment setup completed successfully."