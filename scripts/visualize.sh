#!/bin/bash

mkdir -p $2

mogrify -path $2 -format $3 -resize $4 -quality 100 $1/*.pgm
