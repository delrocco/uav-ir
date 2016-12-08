#!/usr/bin/env bash

original=$1/original
scaled=$1/scaled
visible=$1/visible
colored=$1/colored

# move original images into a sub folder
mkdir -p $original
mv $1/*.pgm $original

# remove bad data files
./pgmhelper.py $original -b | xargs rm

# get the range of values for this data set
scale=$(./pgmhelper.py $original -r)

# scale the images with respect to the data set range
./pgmhelper.py $original -o $scaled -s $scale

# convert the images to a visible format
./visualize.sh $scaled $visible $2 $3

# false-color the images
./colorize.sh $visible $colored