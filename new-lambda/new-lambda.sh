#!/bin/bash

BINPATH=$(realpath "$0")
BINDIR=$(dirname "$BINPATH")
TEMPLATE="$BINDIR/new-lambda.tar.gz"

DIR="$1"
LAMBDA_NAME=$(basename "$DIR")

mkdir -p "$DIR"
tar -C "$DIR" -xf "$TEMPLATE"

sed -i "s/__LAMBDA_NAME__/$LAMBDA_NAME/" "$DIR/Makefile"
