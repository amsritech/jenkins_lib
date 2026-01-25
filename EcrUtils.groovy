package org.company.aws

class EcrUtils {
    static def login(String region) {
        sh """
          aws ecr get-login-password --region ${region} |
          docker login --username AWS --password-stdin \
          ${env.AWS_ACCOUNT_ID}.dkr.ecr.${region}.amazonaws.com
        """
    }
}
