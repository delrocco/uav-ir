#!/bin/bash

scriptdir=$(dirname $0)
capturedir=$scriptdir"/../rpi_lepton/capture"
framesdir=$capturedir"/frames"

echo "[Timestamping frames folder]"
if [ -d $framesDir ]
then
	imgfile=$(find $framesdir"/*.pgm" -print -quit)
	if [ -f $imgfile ]
	then
		timestamp=$(find $imgfile -printf "%TY%Tm%Td_%TH%TM\n" -quit)
		echo "Timestamping:" $framesdir "to" $framesdir"_"$timestamp
		mv $framesdir $framesdir"_"$timestamp
	else
		echo "No files matching:" $framesdir"/*.pgm"
	fi
else
	echo "Folder does not exist:" $framesdir
fi

echo "[Searching for frames_* folder]"
if [ -d $(find $capturedir -name "frames_*" -print -quit) ]
then
	dirfound=$(find $capturedir -name "frames_*" -print -quit)
	echo "Uploading:" $dirfound
	scp -r $dirfound delrocco@ps442953.dreamhost.com:/home/delrocco
else
	echo "Could not find timestamped folder to upload"
fi
