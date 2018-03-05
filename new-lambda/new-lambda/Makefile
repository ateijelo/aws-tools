LAMBDA_NAME := __LAMBDA_NAME__
SOURCES := main.py

zip: lambda.zip

lambda.zip: $(SOURCES) deps.zip
	cp deps.zip lambda.zip
	zip lambda.zip $(SOURCES)

deps.zip: requirements.txt
	docker run --rm -it -u root --entrypoint=sh \
	       -v "$(PWD)":/tmp/src \
		   lambci/lambda:python3.6 \
		   -c "pip install -r /tmp/src/requirements.txt -t deps && \
		       tar -C deps -cvf /tmp/src/.deps.tar . && \
			   chown --reference=/tmp/src/requirements.txt /tmp/src/.deps.tar"
	mkdir -p .deps && cd .deps && \
	    tar -xf ../.deps.tar && \
	    zip -r ../deps.zip * .[^.]* -x'*.dist-info/*' -x'*.pyc'
	rm -rf .deps ; rm -rf .deps.tar

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
	rm -rf .deps
