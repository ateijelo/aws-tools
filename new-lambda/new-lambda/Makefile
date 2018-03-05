LAMBDA_NAME := __LAMBDA_NAME__
SOURCES := main.py
UID := $(shell id -u)

zip: lambda.zip

lambda.zip: $(SOURCES) requirements.txt
	mkdir -p zip
	cp $(SOURCES) zip/
	docker run --rm -it -u root --entrypoint=sh \
	       -v "$(PWD)"/requirements.txt:/tmp/requirements.txt \
		   -v "$(PWD)"/zip:/tmp/zip \
		   lambci/lambda:python3.6 \
		   -c "pip install -r /tmp/requirements.txt -t deps && cp -vr deps/* deps/.[^.]* /tmp/zip/ && chown -R $(UID) /tmp/zip"
	cd zip && zip -r ../lambda.zip * .[^.]* -x'*.dist-info/*' -x'*.pyc'
	rm -rf zip

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
		lambci/lambda:python3.6 main.handler

.PHONY: clean run-here
clean:
	rm -f lambda.zip
	rm -f .uploaded_at
	rm -rf env
	rm -rf site-packages
	rm -rf task
	rm -rf zip
