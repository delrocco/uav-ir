#!/bin/bash

if [ ! -d "$2" ]; then
  mkdir -p $2
fi

mogrify -path $2 -format $3 -resize $4 -quality 100 $1/*.pgm
