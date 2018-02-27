# Python3

import boto3

def handler(event, context):

    sqs = boto3.resource('sqs')
    print(sqs)
