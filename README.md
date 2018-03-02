# AWS tools
---
Set of utilitary scripts to work with AWS services.
Credentials to access your AWS resources can be configured by using:

* Environment variables
* Shared credential file (~/.aws/credentials)
* AWS config file (~/.aws/config)

For more details on how to configure credentials please refer to the Boto3 documentation:
http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials

**sqs-download**
Utility script to consume messages from an SQS queue
