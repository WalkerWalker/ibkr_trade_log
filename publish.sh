docker build -t ibkr-trade-log .
docker tag ibkr-trade-log:latest 466255695036.dkr.ecr.eu-central-1.amazonaws.com/ibkr-trade-log:latest
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 466255695036.dkr.ecr.eu-central-1.amazonaws.com
docker push 466255695036.dkr.ecr.eu-central-1.amazonaws.com/ibkr-trade-log:latest
