#!/usr/bin/env python3

import re
import time
import argparse
import subprocess

from collections import namedtuple

import boto3
import arrow
import dateparser

from marshmallow import Schema, fields, post_load

class ObjectSchema(Schema):
    @post_load
    def make_obj(self, data):
        return namedtuple(
            re.sub(r'Schema$', '', self.__class__.__name__),
            data.keys()
        )(**data)

class EventSchema(ObjectSchema):
    timestamp = fields.Function(deserialize=lambda x: int(x/1000))
    message = fields.String()
    eventId = fields.String()

class FilterResponseSchema(ObjectSchema):
    events = fields.List(fields.Nested(EventSchema))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-group', required=True)
    parser.add_argument('--profile', default="default")
    parser.add_argument('--start-time', default="now")
    parser.add_argument('--poll-freq', type=int, default=5)

    args = parser.parse_args()

    aws_session = boto3.Session(profile_name=args.profile)
    logs = aws_session.client('logs')

    start_time = int(dateparser.parse(args.start_time).timestamp())

    seen = set()
    while True:
        resp = logs.filter_log_events(
            logGroupName=args.log_group,
            startTime=start_time * 1000,
        )

        schema = FilterResponseSchema()
        resp = schema.load(resp).data
        for event in resp.events:
            if event.eventId in seen:
                continue
            seen.add(event.eventId)
            msg = event.message
            while msg.endswith('\n'):
                msg = msg[:-1]
            print(
                arrow.get(event.timestamp).to('local').isoformat(),
                msg,
            )
            if event.timestamp > start_time:
                start_time = event.timestamp

        start_time -= 1
        time.sleep(args.poll_freq)

if __name__ == "__main__":
    main()
