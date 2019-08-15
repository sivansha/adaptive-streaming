#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

debug = True

array_05 = np.load('../misc/q2_d_frame_contribution_05.npy')
array_2 = np.load('../misc/q2_d_frame_contribution_2.npy')
array_4 = np.load('../misc/q2_d_frame_contribution_4.npy')
array_8 = np.load('../misc/q2_d_frame_contribution_8.npy')
array_12 = np.load('../misc/q2_d_frame_contribution_12.npy')

arr_list = []

arr_list.append(array_05)
arr_list.append(array_2)
arr_list.append(array_4)
arr_list.append(array_8)
arr_list.append(array_12)

# if debug:
#     print(high_array)
#     print(low_array)

N = 5
# menMeans = (20, 35, 30, 35, 27)
# womenMeans = (25, 32, 34, 20, 25)
# menStd = (2, 3, 4, 1, 2)
# womenStd = (3, 5, 2, 3, 3)




iFrames = (array_05[0, 0], array_2[0, 0], array_4[0, 0], array_8[0, 0], array_12[0, 0])
pFrames = (array_05[1, 0], array_2[1, 0], array_4[1, 0], array_8[1, 0], array_12[1, 0])
bFrames = (array_05[2, 0], array_2[2, 0], array_4[2, 0], array_8[2, 0], array_12[2, 0])

ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

print(iFrames)
print(pFrames)
print(bFrames)

p2 = plt.bar(ind, pFrames, width, color="orange")
p3 = plt.bar(ind, bFrames, width, color="red", bottom=pFrames)
p1 = plt.bar(ind, iFrames, width, color="blue", bottom=np.array(pFrames)+np.array(bFrames))

plt.ylabel('Amount of Frames')
plt.title('Amount of Frames by Type')
plt.xlabel('Segment duration')
plt.xticks(ind, ('0.5', '2', '4', '8', '12'))
plt.legend((p1[0], p2[0], p3[0]), ('I Frames', 'P Frames', 'B Frames'))

plt.savefig("../figures/q2_d_amount_of_frames.png")

#
# Pie chart for the highest target bitrate 
#

i = 0
durations = ["0.5","2","4","8","12"]

for arr in arr_list:

    labels = 'I Frames ca. '+str(np.round_(arr[0,1]/(1024*1024), decimals=1))+' MB', 'P Frames ca. '+str(np.round_(arr[1,1]/(1024*1024), decimals=1))+' MB', 'B Frames ca. '+str(np.round_(arr[2,1]/(1024*1024), decimals=1))+' MB'
    total_size = float(arr[:, 1].sum())
    sizes = [arr[0,1]/total_size, arr[1,1]/total_size, arr[2,1]/total_size]
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()

    plt.title('File Size Distribution by Frametype, segment duraton: ' + durations[i])
    pie = ax1.pie(sizes, explode=explode, colors=("blue", "orange", "red") , autopct='%1.1f%%',
            shadow=False, startangle=180)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(pie[0], labels, loc="upper right", bbox_to_anchor = (1,1))

    plt.savefig("../figures/q2_d_size_distribution_" + durations[i] + ".png")
    i+=1

# #
# # Pie chart for the lowest target bitrate 
# #
# labels = 'I Frames ca. '+str(np.round_(low_array[0,1]/(1024), decimals=1))+' KB', 'P Frames ca. '+str(np.round_(low_array[1,1]/(1024), decimals=1))+' KB', 'B Frames ca. '+str(np.round_(low_array[2,1]/(1024), decimals=1))+' KB'
# total_size = float(low_array [:, 1].sum())
# sizes = [low_array[0,1]/total_size, low_array[1,1]/total_size, low_array[2,1]/total_size]
# explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# fig1, ax1 = plt.subplots()

# plt.title('Lowest Target Bitrate File Size Distribution by Frametype')
# pie = ax1.pie(sizes, explode=explode, colors=("blue", "orange", "red") , autopct='%1.1f%%',
#         shadow=False, startangle=180)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.legend(pie[0], labels, loc="upper right", bbox_to_anchor = (1,1))

# plt.savefig("../figures/q4_c_byte_size_distribution_low.png")

plt.show()