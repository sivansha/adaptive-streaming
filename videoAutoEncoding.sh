#!/bin/bash

#welcome message
printf "  [*] This script is going to prepare the big buck bunny movie for adaptive streaming

# saving path where the script is saved
MY_PATH="`dirname \"$0\"`"

#checking in relative location from the script if the video is downloaded
if [ ! -f $MY_PATH/images/big_buck_bunny_480p24.y4m ]; then
	echo "[!!!] File not found!"
	echo "  [*] Please download the 'full big buck bunny' video file."
	echo "  [*] Use the original name: big_buck_bunny_480p24.y4m"
	echo "  [*] Save the file in multimedia/images/"
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

# for SEG_DUR in 0.01
# do
#     echo "  [*] Converting video with duration = $SEG_DUR"

# 	ffmpeg -i ./images/big_buck_bunny_480p24.y4m \
# 	-force_key_frames "expr:gte(t,n_forced*10)" \
# 	-threads 1 \
# 	-c:v h264 -profile:v main -crf:v 30 \
# 	-f hls -hls_time 0 -hls_flags independent_segments -hls_list_size 0 \
# 	/a/big_buck_bunny.m3u8

# done

for SEG_DUR in 0.01
do
    echo "  [*] Converting video with duration = $SEG_DUR"

	ffmpeg -i ./images/big_buck_bunny_480p24.y4m \
	-force_key_frames "expr:gte(t,n_forced*10)" \
	-threads 1 \
	-c:v h264 -profile:v main -crf:v 30 \
	-f segment -segment_time 5.0 -segment_time_delta 5.0 \
	-segment_list ./a/big_buck_bunny.m3u8 \
	./a/big_buck_bunny%03d.ts 

done


echo "  [*] Convertion done."
