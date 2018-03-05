#!/bin/bash

BINPATH=$(realpath "$0")
BINDIR=$(dirname "$BINPATH")
TEMPLATE="$BINDIR/new-lambda"

DIR="$1"
LAMBDA_NAME=$(basename "$DIR")

cp -r "$TEMPLATE" "$DIR"

sed -i "s/__LAMBDA_NAME__/$LAMBDA_NAME/" "$DIR/Makefile"
