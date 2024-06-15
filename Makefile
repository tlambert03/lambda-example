include .env

ECR_URL=$(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE_NAME):$(IMAGE_TAG)
PLATFORM=linux/arm64
CONTAINER_NAME=lambda-tester

.PHONY: build push invoke run test

all: build

build:
	docker build --platform $(PLATFORM) -t $(IMAGE_NAME) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(ECR_URL)

push:
	make build
	docker push $(ECR_URL)
	aws lambda update-function-code --no-cli-pager \
		--function-name $(LAMBDA_FUNCTION_NAME) \
		--image-uri $(ECR_URL)

invoke:
	aws lambda invoke --no-cli-pager --function-name $(LAMBDA_FUNCTION_NAME) /dev/stdout

run:
	make build
	docker run --platform $(PLATFORM) --name $(CONTAINER_NAME) -p 9000:8080 $(IMAGE_NAME)

test:
	make run &
	sleep 2  # wait for the container to start
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)