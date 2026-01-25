def call(String status) {
    sh """
      curl -X POST -H 'Content-type: application/json' \
      --data '{"text":"Pipeline ${status}: ${env.JOB_NAME} #${env.BUILD_NUMBER}"}' \
      $SLACK_WEBHOOK
    """
}
