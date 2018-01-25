#!/usr/bin/env python3

import argparse
import boto3
import json
import os
import time

from pprint import pprint

parser = argparse.ArgumentParser(
    description="Utility script to consume messages from an SQS queue")
parser.add_argument('--queue-url', required=True, 
    help="SQS queue url.")
parser.add_argument('--profile', default="default", 
    help="Profile configured in ~/.aws/config file.")
parser.add_argument('--keep', action="store_true", 
    help="Do not delete messages from the queue.")
parser.add_argument('--until-empty', action="store_true", 
    help="Keep reading while there are messages on the queue.")
parser.add_argument('--yes-i-know-what-im-doing', action="store_true", 
    help="Override when using --until-empty and --keep")
parser.add_argument('--daemon', action="store_true", 
    help="Run on foreground until interrupted.")
parser.add_argument('--verbose', action="store_true", 
    help="Print message to standard output.")
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

        msg = {
            "message_id": message.message_id,
            "body": message.body,
            "message_attributes": message.message_attributes,
            "attributes": message.attributes,
        }

        filename = "{:.03f}-{}.json".format(ts, message.message_id)
        f = open(filename, "w")
        f.write(json.dumps(msg))
        f.close()

        if args.verbose:
            pprint(msg)
            print()

        if not keep:
            message.delete()

        count += 1

    return count

if __name__ == "__main__":
    print("{}: listeing for messages...".format(args.queue_url))
    empty_responses = 0
    exit = False
    while not exit:
        try:
            count = download_once(args.keep)
            if count == 0:
                empty_responses += 1

            if args.daemon:
                time.sleep(1)
                continue

            if not args.until_empty: # just run once
                break

            if empty_responses >= 2:
                print("Two empty long-polled responses, assuming empty.")
                break
        except KeyboardInterrupt:
            exit = True
