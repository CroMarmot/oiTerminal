#!/usr/bin/env sh
cd "$(dirname "$0")"
FILENAME=ot-auto-completion.sh
cp ./$FILENAME $DEST
echo "run 'source $DEST'"
