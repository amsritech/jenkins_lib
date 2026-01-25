def call(String appName, String image) {
    echo "Deploying to EKS..."

    sh """
      kubectl set image deployment/${appName} \
      ${appName}=${image}

      kubectl rollout status deployment/${appName}
    """
}
