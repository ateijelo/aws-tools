LAMBDA_NAME := __LAMBDA_NAME__
SOURCES := main.py
UID := $(shell id -u)

zip: lambda.zip

lambda.zip: $(SOURCES) deps.zip
	zip deps.zip $(SOURCES)
	cp deps.zip lambda.zip

deps.zip: requirements.txt
	mkdir -p deps
	docker run --rm -it -u root --entrypoint=sh \
	       -v "$(PWD)"/requirements.txt:/tmp/requirements.txt \
		   -v "$(PWD)"/deps:/tmp/deps \
		   lambci/lambda:python3.6 \
		   -c "pip install -r /tmp/requirements.txt -t deps && cp -vr deps/* deps/.[^.]* /tmp/deps/ && chown -R $(UID) /tmp/deps"
	rm -f deps.zip
	cd deps ; zip -r ../deps.zip * .[^.]* -x'*.dist-info/*' -x'*.pyc' ; cd ..
	rm -rf deps

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
	rm -f lambda.zip deps.zip
	rm -f .uploaded_at
	rm -rf env
	rm -rf site-packages
	rm -rf task
	rm -rf deps
