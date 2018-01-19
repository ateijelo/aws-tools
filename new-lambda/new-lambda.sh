#!/bin/bash

BINPATH=$(realpath "$0")
BINDIR=$(dirname "$BINPATH")
TEMPLATE="$BINDIR/new-lambda.tar.gz"

LAMBDA_NAME="$1"
DIR="$LAMBDA_NAME"

mkdir -p "$DIR"
tar -C "$DIR" -xf "$TEMPLATE"

sed -i "s/__LAMBDA_NAME__/$LAMBDA_NAME/" "$DIR/Makefile"
