#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import re


def get_logs_from_folder(folder_path,debug):
    """
    get_logs_from_folder:
    =====================
    Returns all files with full path from given folder.
    """

    files = []
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        files.extend(filenames)
        break
    if debug:
        print(filenames)
    return files


def import_log(file_name, debug, last_column=9):

    result_list =[]
    with open(file_name) as file:
        file.readline() #gets rid of the first line

        for line in file.readlines():
            #if debug: print(line)
            
            line = line.split(" ")
            line = list(map(float,line))
            result_list.append(line[:last_column])
            #print(result_list)

    return np.array(result_list)


def extract_QoE_values(file_name, debug):
    """
    extract_QoE_values:
    ===================
    Reads the data of a given log file for futher analyses.
    Data is returned as a numpy array in the form:
    np.array[inital_delay, average_quality, number_of_switches, number_of_stallings, stalling_duration]
    """
    #TODO archived ouput seems faulty correct that
    result_list = []
    inital_delay = -1
    average_quality = 0

    number_of_switches = -1
    temp_level = -1

    number_of_stallings = -1
    stalling_duration = 0
    temp_stalling_start_entry = -1

    # importing the log data
    log_data = import_log(file_name,debug)
    log_entries = log_data.shape[0]
    
    for i in range(log_entries):

        #checking if inital_delay is over
        if inital_delay == -1 and log_data[i,8] !=0:
            inital_delay = log_data[i,0]-log_data[0,0]
            if debug:
                print (i)
                print (inital_delay)

        # tracking stallings
        # new stalling happens
        if log_data[i,2] == 0 and temp_stalling_start_entry == -1:
                number_of_stallings +=1
                temp_stalling_start_entry = i
                if debug: print(i)
        
        # current stalling ends
        if temp_stalling_start_entry != -1 and log_data[i,2] != 0 and inital_delay!=-1:
            stalling_duration += log_data[i,0]-log_data[temp_stalling_start_entry,0]
            temp_stalling_start_entry = -1
            if debug: print(i)

        # tracking the level/quality        
        current_level = log_data[i,5]
        if  current_level != temp_level:
            number_of_switches += 1
            temp_level = current_level
        average_quality += current_level

    average_quality = average_quality/log_entries

    #subtract inital delay
    stalling_duration-=inital_delay

    #return [inital_delay, average_quality, number_of_switches, number_of_stallings, stalling_duration]
    return np.array([inital_delay, average_quality, number_of_switches, number_of_stallings, stalling_duration])


def plot_QoE(results, debug):
    #logs: static_05, static_1, static_2, dyn_trace0, dyn_trace1, dyn_trace2
    #inital_delay, average_quality, number_of_switches, number_of_stallings, stalling_duration
    
    legend=["Static 0.5 Mbit/s", "Static 1 Mbit/s", "Static 2 Mbit/s", "Trace 0", "Trace 1", "Trace 2"]

    N = results.shape[0]

    ind = np.arange(N)    # the x locations for the groups
    width = 0.25       # the width of the bars: can also be len(x) sequence

    inital_delay = results[:,0]
    average_quality = results[:,1]
    number_of_switches = results[:,2]
    number_of_stallings = results[:,3]
    stalling_duration = results[:,4]
    
    # left-y-achis with time scale [s] for inital delay and stalling duration
    fig, ax1 = plt.subplots()
    p1 = ax1.bar(ind-width/2, inital_delay+0.2, width, color="orange")
    p2 = ax1.bar(ind-width/2, stalling_duration+0.2, width, color="blue", bottom=inital_delay+0.2)
    
    # rigth-y-achis with level scale
    ax2 = ax1.twinx()
    p3 = ax2.bar(ind+width/2, average_quality+0.005, width, color="red")
    
    ax1.set_ylim(0, 81)
    ax1.set_yticks(range(0,81,10))
    ax1.set_ylabel('Time [seconds]')

    ax2.set_ylim(0, 2.2)
    #ax2.set_yticks(0,2)#range(0,2,0.2))
    ax2.set_ylabel('Average Quality Level')
    plt.title('Quality of experience values for the different network setups')
    plt.xlabel('Network setup')
    plt.xticks(ind, legend)#, rotation=90)
    plt.legend((p1[0], p2[0], p3[0]), ('Inital Delay', 'Total Stalling Delay and Average number of stalling', 'Average Quality Level and Average Number of Quality Switches'))

    rects = ax1.patches
    print(rects)

    # Make some labels.
    labels = number_of_stallings 

    for result, label, rect in zip(results, labels, rects):
        height = result[0]+result[4]
        ax1.text(rect.get_x() + rect.get_width() / 2, height+1, label,ha='center', va='bottom')

    # Make some labels.
    labels = number_of_switches 
    rects = ax2.patches

    for result, label, rect in zip(results, labels, rects):
        height = result[1]
        ax2.text(rect.get_x() + rect.get_width() / 2, height+0.01, label,ha='center', va='bottom')

    plt.savefig("../figures/q3_b.png")
    plt.show()

    

    return 0


def run_program(folder_path, debug):

    print("    [*] Running Quality of Experiance Analysis ...")
    print("    Checking for logs at given path ...")
    print("")
    logs = get_logs_from_folder(os.path.abspath(folder_path), debug)
    print("    [*] Found "+str(len(logs))+" logs")

    static_05 = []
    static_1 = []
    static_2 = []
    dyn_trace0 = []
    dyn_trace1 = []
    dyn_trace2 = []

    for log in logs:
        print("    [*] Collecting data from log: "+log)
        current_result = extract_QoE_values(folder_path+log , debug)

        log = log.split("_")

        if log[3]=="dynamic":
            trace_number = log[4].split("e")[1]
            if trace_number == "0":
                dyn_trace0.append(current_result)
            elif trace_number == "1":
                dyn_trace1.append(current_result)
            elif trace_number == "2":
                dyn_trace2.append(current_result)
            else:
                assert(False)
        
        if log[3]=="static":
            static_value = log[4].split("M")[0]
            if static_value == "0.5":
                static_05.append(current_result)
            elif static_value == "1":
                static_1.append(current_result)
            elif static_value == "2":
                static_2.append(current_result)
            else:
                assert(False)
    results = np.array([static_05, static_1, static_2, dyn_trace0, dyn_trace1, dyn_trace2])

    print(results)
    print(results.shape)
    average_result = []
    for i in range(results.shape[0]):
        temp_average = []
        for j in range(results.shape[1]):
            temp_average.append(np.average(results[i,:,j]))
        average_result.append(temp_average)
    
    average_result = np.array(average_result)
    print(average_result)
    plot_QoE(average_result,debug)


def main():
    #print(len(sys.argv))
    debug = False
    if len(sys.argv) < 2 or len(sys.argv) >3 :
        print(
            """

    Usage: python3 q3_b.py [-d] path/to/log_dir

    -d:     show debug output


    [*] Please provide the path to the directory (ending with a /) containg only log files 
        and optionally the debug flag: -d
            """
        )
        exit(0)
    
    results=[]
    for arg in sys.argv[1:]:
        if arg == "-d": 
            debug = True
            print("    [!] Using DEBUG mode")
        else:
            folder_path = arg
            run_program(folder_path,debug)

if __name__ == "__main__":
    main()