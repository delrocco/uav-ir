#!/bin/bash

if [ ! -d "$2" ]; then
  mkdir -p $2
fi

for f in $1/*.$3
do
	newfile=$2/$(basename $f)
	convert $f \( ironbow.png -flip \) -clut $newfile
done
