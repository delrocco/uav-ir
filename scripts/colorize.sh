#!/bin/bash

mkdir -p $2

for f in $1/*.jpg
do
	newfile=$2/$(basename $f)
	convert $f \( ironbow.png -flip \) -clut $newfile
done
