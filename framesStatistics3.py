import numpy as np
import matplotlib.pyplot as plt


def typeSwitch(tmp_type):
    if tmp_type.startswith("I"): return 0
    if tmp_type.startswith("P"): return 1
    if tmp_type.startswith("B"): return 2

#debug switch
debug=False

array_05 = np.array([[0, 0], [0, 0], [0, 0]])
array_2 = np.array([[0, 0], [0, 0], [0, 0]])
array_4 = np.array([[0, 0], [0, 0], [0, 0]])
array_8 = np.array([[0, 0], [0, 0], [0, 0]])
array_12 = np.array([[0, 0], [0, 0], [0, 0]])

round=0

for file_name in ["./images/0.5/vs1/stat.txt","./images/2/vs1/stat.txt","./images/4/vs1/stat.txt","./images/8/vs1/stat.txt","./images/12/vs1/stat.txt", ]:
    with open(file_name, 'r') as file:
        print ("counting "+file_name)
        content = file.readlines()
        if debug:
            print(content)
            print(type(content))

        for line in content:
            #pkt_size=846\n
            #pict_type=I\n
            if line.startswith("pkt_size="):
                tmp_size = float(line.split("=")[1])
            if line.startswith("pict_type="):
                tmp_type = line.split("=")[1]
                i = typeSwitch(tmp_type)

                if round == 0:
                    array_05[i, 0] = array_05[i, 0]+1
                    array_05[i, 1] = array_05[i, 1]+tmp_size

                if round == 1:
                    array_2[i, 0] = array_2[i, 0]+1
                    array_2[i, 1] = array_2[i, 1]+tmp_size

                if round == 2:
                    array_4[i, 0] = array_4[i, 0]+1
                    array_4[i, 1] = array_4[i, 1]+tmp_size

                if round == 3:
                    array_8[i, 0] = array_8[i, 0]+1
                    array_8[i, 1] = array_8[i, 1]+tmp_size

                if round == 4:
                    array_12[i, 0] = array_12[i, 0]+1
                    array_12[i, 1] = array_12[i, 1]+tmp_size

    round +=1

# print(high_array)
# print(low_array)
np.save('./misc/frame_contribution_05', array_05)
np.save('./misc/frame_contribution_2', array_2)
np.save('./misc/frame_contribution_4', array_4)
np.save('./misc/frame_contribution_8', array_8)
np.save('./misc/frame_contribution_12', array_12)
