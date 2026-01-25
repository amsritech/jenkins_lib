@Library('ci-lib') _

pipeline {
  agent any

  environment {
    IMAGE = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app"
    TAG   = "${BUILD_NUMBER}"
  }

  stages {
    stage('Build') {
      steps { buildApp() }
    }

    stage('Docker Build & Push') {
      steps { dockerBuildPush(IMAGE, TAG) }
    }

    stage('Scan') {
      steps { scanImage("${IMAGE}:${TAG}") }
    }

    stage('Deploy') {
      steps { deployToEks('my-app', "${IMAGE}:${TAG}") }
    }
  }

  post {
    success { notifySlack("SUCCESS") }
    failure { notifySlack("FAILED") }
  }
}
