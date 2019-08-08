## Implementation of server-client for TAPAS based HTTP Adaptive Streaming simulation

HTTP Adaptive Streaming is a methid for video streaming optimization. the video is split into several segments of equal duration, each decoded in several bitrates.<br>
The client apply huristics in order to decide which quality to fetch next.<br><br>

This repository implements a client-server enviroment via virtual machine in order to test and adjust TAPAs based Adaptive Streaming system.<br><br>

The huristic decision should take into considaration:
1. available video segments quality
1. future bandwith astimation
1. current buffer size

<br><br>

assume the video is splitted into durations of 0.5, 2, 4, 8, 12 seconds, with 3 qualities, crf = 18, 23 and 28.
the quality different is:


#### details
- the video is splitted into durations of 0.5, 2, 4, 8, 12 seconds
