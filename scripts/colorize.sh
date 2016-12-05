#!/bin/bash

for f in visible/*.jpg
do
	newfile="colored/"$(basename $f)
	convert $f \( ironbow.png -flip \) -clut $newfile
done
