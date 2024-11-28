. .env

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REGISTRY}

docker build --no-cache -t ${DOCKER_IMAGE_NAME} . 

docker tag ${DOCKER_IMAGE_NAME}:latest ${REGISTRY}/${ECR_REPO_FOLDER}:${DOCKER_IMAGE_NAME}

docker push ${REGISTRY}/${ECR_REPO_FOLDER}:${DOCKER_IMAGE_NAME}

envsubst < training_worker1.yaml.template > training_worker1.yaml
envsubst < training_worker2.yaml.template > training_worker2.yaml