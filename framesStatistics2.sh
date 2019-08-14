#!/bin/bash

echo "  [*] Creating statistics for crf = 23 and duration = $1"
for file in ./images/$1/vs1/*.ts
do
  ffprobe -show_frames $file >> "./images/$1/vs1/stat.txt"
done
