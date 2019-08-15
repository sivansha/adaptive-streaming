#!/bin/bash

#welcome message
printf "  [*] This script measures SSIM for different segment duration video\n"

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
for SEG_DUR in 0.5 2 4 8 12
do
    echo "  [*] Calculating SSIM for segment duration = $SEG_DUR"

	# 18
	# 23
	# 28

	ffmpeg -threads 1 -i ../q2/$SEG_DUR/vs0/big_buck_bunny.m3u8 -i ../images/big_buck_bunny_480p24.y4m  -lavfi  ssim=../q2/SSIM/ssim_18_$SEG_DUR.log -f null -
	ffmpeg -threads 1 -i ../q2/$SEG_DUR/vs1/big_buck_bunny.m3u8 -i ../images/big_buck_bunny_480p24.y4m  -lavfi  ssim=../q2/SSIM/ssim_23_$SEG_DUR.log -f null -
	ffmpeg -threads 1 -i ../q2/$SEG_DUR/vs2/big_buck_bunny.m3u8 -i ../images/big_buck_bunny_480p24.y4m  -lavfi  ssim=../q2/SSIM/ssim_28_$SEG_DUR.log -f null -

done

echo "  [*] Calculating done."
