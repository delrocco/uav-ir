
framesDir="../rpi_lepton/capture/frames"

echo "[Timestamping frames folder]"
if [ -d $framesDir ]
then
	if [ -f $(find ../rpi_lepton/capture/frames/*.pgm -maxdepth 0 -print -quit) ]
	then
		timestamp=$(find ../rpi_lepton/capture/frames/*.pgm -maxdepth 0 -printf "%TY%Tm%Td_%TH%TM\n" -quit)
		echo "Timestamping:" $framesDir "to" $framesDir"_"$timestamp
		mv $framesDir $framesDir"_"$timestamp
	else
		echo "No files matching:" $framesDir"/*.pgm"
	fi
else
	echo "Folder does not exist:" $framesDir
fi

echo "[Searching for frames_* folder]"
if [ -d $(find ../rpi_lepton/capture/ -name "frames*" -print -quit) ]
then
	framesDir=$(find ../rpi_lepton/capture/ -name "frames*" -print -quit)
	echo "Uploading:" $framesDir
	scp -r $framesDir delrocco@ps442953.dreamhost.com:/home/delrocco
else
	echo "Could not find anything to upload"
fi
