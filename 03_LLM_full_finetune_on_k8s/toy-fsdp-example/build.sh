aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 767397933116.dkr.ecr.us-east-1.amazonaws.com

docker build --no-cache -t toy-fsdp . 

docker tag toy-fsdp:latest 767397933116.dkr.ecr.us-east-1.amazonaws.com/luka-exp:toy-fsdp-v0

docker push 767397933116.dkr.ecr.us-east-1.amazonaws.com/luka-exp:toy-fsdp-v0

