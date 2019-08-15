#!/bin/bash


echo "  [*] Creating statistics for crf = 23 and duration = $1"
for file in ../q2/$1/vs1/*.ts
do
  ffprobe -show_frames $file >> "../q2/$1/vs1/stat.txt"
done