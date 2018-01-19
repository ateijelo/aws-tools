#!/usr/bin/env python3

import os
import json
import argparse

import boto3

parser = argparse.ArgumentParser()
parser.add_argument('--queue-url', required=True)
parser.add_argument('--profile', default="default")
parser.add_argument('--keep', action="store_true")
parser.add_argument('--until-empty', action="store_true")
parser.add_argument('--yes-i-know-what-im-doing', action="store_true")

args = parser.parse_args()

aws_session = boto3.Session(profile_name=args.profile)
sqs = aws_session.resource('sqs')
queue = sqs.Queue(args.queue_url)

if args.keep and not args.yes_i_know_what_im_doing:
    # we don't want to attempt to empty the queue
    # if we're not actually deleting anything
    args.until_empty = False

def download_once(keep=False):
    messages = queue.receive_messages(
        WaitTimeSeconds=5,
        MaxNumberOfMessages=10,
        MessageAttributeNames=['All'],
        AttributeNames=['All'],
    )

    count = 0

    for message in messages:
        print("Downloading message: {}".format(message.message_id))
        ts = int(message.attributes.get('SentTimestamp')) / 1000

        filename = "{:.03f}-{}.json".format(ts, message.message_id)
        f = open(filename, "w")
        f.write(json.dumps({
            "message_id": message.message_id,
            "body": message.body,
            "message_attributes": message.message_attributes,
            "attributes": message.attributes,
        }))
        f.close()
        # try:
        #     os.utime(filename, (ts, ts))
        # except (KeyError, ValueError, TypeError):
        #     pass
        if not keep:
            message.delete()
        count += 1
    return count

if __name__ == "__main__":
    empty_responses = 0
    while True:
        count = download_once(args.keep)
        if count == 0:
            empty_responses += 1

        if not args.until_empty: # just run once
            break

        if empty_responses >= 2:
            print("Two empty long-polled responses, assuming empty.")
            break
