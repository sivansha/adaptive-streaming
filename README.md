## Implementation of server-client for TAPAS based HTTP Adaptive Streaming simulation

HTTP Adaptive Streaming is a methid for video streaming optimization. the video is split into several segments of equal duration, each decoded in several bitrates.<br>
The client apply huristics in order to decide which quality to fetch next.<br><br>

This repository implements a client-server enviroment via virtual machine in order to test and adjust TAPAs based Adaptive Streaming system.<br><br>

Factors that should be taken into considaration:
1. available video segments quality
1. future bandwith astimation
1. current buffer size

#### details
- the video is splitted into durations of 0.5, 2, 4, 8, 12 seconds

### resources
The video used in the code can be found here:
[big buck bunny](https://peach.blender.org/download/)
