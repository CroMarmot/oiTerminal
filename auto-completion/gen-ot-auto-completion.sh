#!/usr/bin/env sh
cd "$(dirname "$0")"

FILENAME=ot-auto-completion.sh
DEST=/tmp/$FILENAME
INSERTLINE="ABS_PATH=$(pwd)"

cp ./$FILENAME $DEST
sed -i -e '3 d' -e "4 i $INSERTLINE" $DEST
echo "run 'source $DEST'"
