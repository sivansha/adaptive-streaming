#!/bin/bash

for SEG_DUR in 0.5 2 4 8 12
do
   echo "  [*] Counting total I frames number for duration = $SEG_DUR"

    VAR=$(find -x ../q2/$SEG_DUR/vs1/ -iname '*.ts' -type f -maxdepth 1 -exec ffprobe -loglevel panic -hide_banner -select_streams v -show_frames -show_entries frame=pict_type -of csv {} \; | grep -n I | wc -l | 
   LC_ALL=C awk -v pwd="${PWD}" '
     BEGIN{ sum=0; count=0; }
      { sum+=($1);
   }
   END{ 
        printf ("%d\n", sum); 
   }')  
   echo "    I-frame count = $VAR"
done