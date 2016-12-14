#!/usr/bin/env bash

# arguments passed in
path=$1
format=$2
resolution=$3

# make sure path ends in a slash
case "$path" in
*/)
    ;;           # ends with slash; do nothing
*)
    path=$path/  # ends without slash; add it
    ;;
esac

original=$path"original"
scaled=$path"scaled"
visible=$path"visible"
colored=$path"colored"

# move original images into a sub folder, if not already done
if [ ! -d "$original" ]; then
  mkdir -p $original
  mv $path/*.pgm $original
fi

# remove bad data files
./pgmhelper.py $original -b | xargs rm

# get the range of values for this data set
range=$(./pgmhelper.py $original -r)

# scale the images with respect to the data set range
./pgmhelper.py $original -o $scaled -s $range

# convert the images to a visible format
./visualize.sh $scaled $visible $format $resolution

# false-color the images
./colorize.sh $visible $colored $format
