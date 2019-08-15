#!/bin/bash

#welcome message
printf "  [*] This script is going to prepare the big buck bunny movie for adaptive streaming as needed for q2 of the multimedia lab sheet 3\n"

# saving path where the script is saved
MY_PATH="`dirname \"$0\"`"

#checking in relative location from the script if the video is downloaded
if [ ! -f $MY_PATH/../images/big_buck_bunny_480p24.y4m ]; then
	echo "[!!!] File not found!"
	echo "  [*] Please download the 'full big buck bunny' video file."
	echo "  [*] Use the original name: big_buck_bunny_480p24.y4m"
	echo "  [*] Save the file in multimedia/sheet3/images/"
	exit 1
fi
echo "  [*] Video found"

# checking wheter ffmpeg is installed
FFMPEG_PATH="`command -v ffmpeg`"
if [ -z "$FFMPEG_PATH" ];then
	echo "[!!!] ffmpeg not found"
	echo "  [*] Please install ffmpeg before continuing"
	exit 1
fi
echo "  [*] ffmpeg found"

#conversion of the videos

#for different segment durations
for SEG_DUR in 10
do
    echo "  [*] Converting video with duration = $SEG_DUR"

	ffmpeg -i ../images/big_buck_bunny_480p24.y4m -threads 1 -force_key_frames "expr:gte(t,n_forced * $SEG_DUR)" \
	-c:v h264 -profile:v main -crf:v 30 \
	-f hls -hls_time $SEG_DUR -hls_flags independent_segments -hls_list_size 0 \
	../q2/d/big_buck_bunny.m3u8 

done

echo "  [*] Convertion done."
