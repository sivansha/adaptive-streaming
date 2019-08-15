# For the spatial perceptual information (SI), Sobel filter is applied to a video frame.
# Then, the standard deviation of each pixel in the filtered image is computed.
# To compute the SI of a video scene, this procedure is repeated for all frames,
# and the maximum is chosen as SI for the scene.

# for each frame:
# -> apply Sobel filter to a frame
# -> calculates standard deviation of each pixel
# -> highest = SI

# The TI value between two frames is the standard deviation of its difference.
# If you want to compute the TI for a complete scene, the TI is computed for all consecutive video frames and the maximum
# is chosen as TI for the scene.

# for each 2 consecutive frames:
# -> calculates the difference between the frames
# -> calculates standard deviation of the difference
# -> highest = SI

# ffmpeg -video_size 854x480 -r 24 -pixel_format yuv420p -i sintel.yuv output-%d.png

import os
import shutil
import subprocess
import pexpect
from PIL import Image
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt

Y, Cb, Cr = 0, 1, 2
path = "..\images\\frames\\"


def video2frames(command):
    """
    extracts the frames from the video
    :param ffmpeg_command: ffmpeg command to execute
    :return: void
    """

    # delete folder if exists
    # create folder
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

    print(command)
    print("FFMpeg running...")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    output, _ = process.communicate()
    print(output)
    process.kill()

###############################################################################

def computeSI(raw_video, video_size, bitrate, pixel_format):

    """
    calculates SI on a raw .yuv video
    :param raw_video: path to the .yuv video
    :param video_size: the video resolution
    :param bitrate: the video bitrate
    :param pixel_format: the video pixel format
    :return: array with SI values for all frames
    """

    command = "ffmpeg -y -video_size " + str(video_size) + " -r " + str(bitrate) + " -pixel_format " + str(pixel_format) + " -i " + str(raw_video) + " " + str(path) + "frame-%04d.png"
    video2frames(command)

    # for holding the standard deviation of the frames
    frames_sd = []

    # get standard deviation for each frame
    for filename in os.listdir(path):
        print("computing SI for " + filename)
        # open and convert the frame
        yuv_frame = Image.open(path + filename).convert("YCbCr")
        y_frame_asArray = np.array(yuv_frame)[:, :, Y].astype('int32')
        # apply Sobel filter
        sobel_frame_x = ndimage.sobel(y_frame_asArray, axis=0, mode='constant')
        sobel_frame_y = ndimage.sobel(y_frame_asArray, axis=1, mode='constant')
        sobel_frame = np.hypot(sobel_frame_x, sobel_frame_y)

        frames_sd.append(np.std(sobel_frame))

    return frames_sd
###############################################################################

def computeTI(raw_video, video_size, bitrate, pixel_format):

    """
    calculates SI on a raw .yuv video
    :param raw_video: path to the .yuv video
    :param video_size: the video resolution
    :param bitrate: the video bitrate
    :param pixel_format: the video pixel format
    :return: array with SI values for all frames
    """

    command = "ffmpeg -y -video_size " + str(video_size) + " -r " + str(bitrate) + " -pixel_format " + str(pixel_format) + " -i " + str(raw_video) + " " + str(path) + "frame-%04d.png"
    video2frames(command)

    # for holding the standard deviation of the difference
    frames_sd = []

    dirs = os.listdir(path)
    while len(dirs) > 1:
        print("computing TI for " + dirs[0] + ", " + dirs[1])
        yuv_frame_1 = Image.open(path + dirs[0]).convert("YCbCr")
        yuv_frame_2 = Image.open(path + dirs[1]).convert("YCbCr")

        yuv_frame_1 = np.array(yuv_frame_1)[:, :, Y].astype(np.int32)
        yuv_frame_2 = np.array(yuv_frame_2)[:, :, Y].astype(np.int32)

        frames_diff = yuv_frame_1 - yuv_frame_2
        frames_sd.append(np.std(frames_diff))

        dirs.pop(0)

    return frames_sd
###############################################################################

si = computeSI("../images/big_buck_bunny.yuv", "704x480", '24', "yuv420p")
print(si)
ti = computeTI("../images/big_buck_bunny.yuv", "704x480", '24', "yuv420p")
print(ti)

# visualize the results Spatial and temporal information
ax = plt.subplot()
ax.plot(si, label='Spatial Information')
ax.plot(ti, label='Temporal Information')
ax.legend(loc='upper center')
ax.set(title='Visyalization of the Spatial Information and Temporal Information for the Big buck bunny Clip', ylabel='Standard Deviation values', xlabel='Video Frames')

plt.savefig("../figures/q1_e-bbb.png")
plt.show()

