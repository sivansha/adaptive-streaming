#!/usr/bin/env python3
# -*- coding: utf-8 -*

from PIL import Image
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt

Y, Cb, Cr = 0, 1, 2

# load image
yuv_frame = Image.open("../images/output-161.png").convert("YCbCr")

# creates array from the image
frame_asArray = np.array(yuv_frame)
# extract y chanel:
y_frame_asArray = frame_asArray[:, :, Y]
# creates image from the y chanel for display
y_frame = Image.fromarray(y_frame_asArray, "L")
# convert the array to displayable type
y_frame_asArray = y_frame_asArray.astype('int32')

# apply Sobel filter to the Y channel
# apply sobel for x, y directions
sobel_frame_x = ndimage.sobel(y_frame_asArray, axis=0, mode='constant')
sobel_frame_y = ndimage.sobel(y_frame_asArray, axis=1, mode='constant')
# combine the x, y deriatives
sobel_frame = np.hypot(sobel_frame_x, sobel_frame_y)

# plot the original image, the Y component, and the Sobel filtered Y component
plt.subplot(1, 3, 1), plt.imshow(yuv_frame)
plt.title('Original Frame'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 3, 2), plt.imshow(y_frame)
plt.title('Y channel of Frame'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 3, 3), plt.imshow(sobel_frame, cmap = 'gray')
plt.title('Sobel filtered Y channel of Frame'), plt.xticks([]), plt.yticks([])

plt.savefig("../figures/q1_b-c-scipy.png")
plt.show()
