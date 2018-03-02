#!/usr/bin/env python3

import os
import json
import argparse

import boto3

parser = argparse.ArgumentParser()
parser.add_argument('--queue-url', required=True)
parser.add_argument('--profile', default="default")
parser.add_argument('filenames', nargs='*')

args = parser.parse_args()

aws_session = boto3.Session(profile_name=args.profile)
sqs = aws_session.resource('sqs')
queue = sqs.Queue(args.queue_url)

for filename in args.filenames:
    print("Uploading {}".format(filename))
    result = queue.send_message(
        MessageBody=open(filename).read()
    )
    print(result)
