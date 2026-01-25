def call(String image) {
    echo "Scanning Docker image..."
    sh "trivy image --severity HIGH,CRITICAL ${image}"
}
