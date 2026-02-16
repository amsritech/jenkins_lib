#!/bin/bash

# Script to automate rollout and rollback of Kubernetes deployment

DEPLOYMENT_NAME="my-app"
NAMESPACE="default"
IMAGE_REPO="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app"
NEW_IMAGE_TAG=$1  # Pass new image tag as first argument
ACTION=$2         # Pass "rollout" or "rollback" as second argument

if [ -z "$NEW_IMAGE_TAG" ] || [ -z "$ACTION" ]; then
  echo "Usage: $0 <new-image-tag> <rollout|rollback>"
  exit 1
fi

echo "Starting $ACTION process for deployment $DEPLOYMENT_NAME in namespace $NAMESPACE..."

if [ "$ACTION" == "rollout" ]; then
  # Update deployment image to new tag
  kubectl set image deployment/$DEPLOYMENT_NAME $DEPLOYMENT_NAME=$IMAGE_REPO:$NEW_IMAGE_TAG -n $NAMESPACE --record
  # Wait for rollout to complete
  kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE
  if [ $? -eq 0 ]; then
    echo "Rollout successful: Deployment updated to image tag $NEW_IMAGE_TAG"
  else
    echo "Rollout failed"
    exit 1
  fi

elif [ "$ACTION" == "rollback" ]; then
  # Rollback to previous revision
  kubectl rollout undo deployment/$DEPLOYMENT_NAME -n $NAMESPACE
  if [ $? -eq 0 ]; then
    echo "Rollback successful: Deployment reverted to previous version"
  else
    echo "Rollback failed"
    exit 1
  fi

else
  echo "Invalid action: $ACTION. Use 'rollout' or 'rollback'."
  exit 1
fi