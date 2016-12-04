#!/bin/bash

numfiles=0
numfilesnew=0
scriptdir=$(dirname $0)
capturedir=$scriptdir"/../rpi_lepton/capture"
framesdir=$capturedir"/frames"

# wait 1 minute to give user the chance to cancel this script
echo "Countdown to capture: "
for i in {30..1}
do
	echo -n $i " "
	sleep 1
done

# capture some IR images
for i in {1..5000}
do
	# 
	if [ -d $framesdir ]
	then
		numfiles=$(ls -l $framesdir | wc -l)
	fi
	
	echo 1 | sudo tee /sys/class/leds/led1/brightness
	sudo $capturedir"/capture"
	echo 0 | sudo tee /sys/class/leds/led1/brightness
	
	numfilesnew=$(ls -l $framesdir | wc -l)
	if (( numfilesnew > numfiles ))
	then
		echo "Total captured: " $numfilesnew
		echo 1 | sudo tee /sys/class/leds/led0/brightness
		echo 0 | sudo tee /sys/class/leds/led0/brightness
	else
		echo "Capture failed :("
	fi
	
	sleep 2
done

echo 0 | sudo tee /sys/class/leds/led0/brightness
echo 0 | sudo tee /sys/class/leds/led1/brightness
