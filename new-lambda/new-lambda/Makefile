LAMBDA_NAME := __LAMBDA_NAME__
SOURCES := main.py

zip: lambda.zip

lambda.zip: $(SOURCES) site-packages
	zip lambda.zip $(SOURCES)
	cd site-packages && zip -r ../lambda.zip * -x'*.dist-info/*' -x'*.pyc'

site-packages: requirements.txt env/bin/python
	./env/bin/pip install -r requirements.txt -t site-packages && touch site-packages

env/bin/python:
	python3 -m venv env && ./env/bin/pip install wheel

update: .uploaded_at

.uploaded_at: lambda.zip
	aws lambda update-function-code --function-name $(LAMBDA_NAME) --zip-file fileb://lambda.zip && touch .uploaded_at

run-here: zip
	rm -rf task
	unzip -d task lambda.zip
	docker run --rm -it -v "${PWD}"/task:/var/task \
		-e AWS_DEFAULT_REGION \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e SQS_QUEUE_URL \
		-e CELLTRAK_URL \
		-e CELLTRAK_USER \
		-e CELLTRAK_AUTH \
		lambci/lambda:python3.6 main.handler

.PHONY: clean run-here
clean:
	rm -f lambda.zip
	rm -f .uploaded_at
	rm -rf env
	rm -rf site-packages
	rm -rf task
