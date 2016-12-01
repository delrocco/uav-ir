#!/bin/bash

numfiles=0
numfilesnew=0

# wait 1 minute to give user the chance to cancel this script
echo "Countdown to capture: "
for i in {10..1}
do
	echo -n $i " "
	sleep 1
done

# capture some IR images
for i in {1..5000}
do
	# 
	if [ -d ../rpi_lepton/capture/frames ]
	then
		numfiles=$(ls -l ../rpi_lepton/capture/frames | wc -l)
	fi
	
	echo 1 | sudo tee /sys/class/leds/led1/brightness
	sudo ../rpi_lepton/capture/capture
	echo 0 | sudo tee /sys/class/leds/led1/brightness
	
	numfilesnew=$(ls -l ../rpi_lepton/capture/frames | wc -l)
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
