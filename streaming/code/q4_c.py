#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys

debug=False

def import_log(file_name, debug):
    result_list =[]
    with open(file_name) as file:
        file.readline()
        for line in file.readlines():
            if debug: print(line)
            
            line = line.split(" ")
            line = list(map(float,line))
            result_list.append(line[:8])
            #print(result_list)
    return np.array(result_list)

def plot_q4_d_and_e(results,debug):
    if debug: print(results[0][:,:])
    
    # buffered_time over time
    # [2] over [0]

    # quality_level over time
    # [5] over [0]

    # average buffer level and average quality for all bandwidths
    # sum([2])/149 | sum([5])/149 ; 4 times 

    average_bandwidth=[2983.42, 1491.71, 807.95, 432.78]
    legend=["doubled average bandwidth for crf=18", "average bandwidth for crf=18", "average bandwidth for crf=23", "average bandwidth for crf=28"]
    color=["blue", "red","orange", "darkgreen"]
    line_style=["solid","--", "-.",":"]

    #i=0
    fig, ax = plt.subplots()

    for i in range(4):
        time_buffered = results[i][:,2]
        absolute_time = results[i][:,0]-results[i][0,0]

        if debug:
            print(time_buffered)
            print(absolute_time)
            print(type(results[i][0,0]))
            print(results[i][0,0])

        ax.plot(absolute_time, time_buffered, color=color[i], ls=line_style[i], linewidth=1)#, marker="o")
        ax.set(title='buffered time over time',
            ylabel='buffered time [s]',
            xlabel='time [s]')
        #ax.xaxis.set(ticks=[18, 30, 48])
        #ax.set_xticklabels(["crf-18/Br-2205k", "crf-30/Br-334k", "crf-48/Br-36k"])
        #ax.yaxis.set(ticks=values_psnr[:, 1])
        ax.legend(legend)
    plt.savefig('../../images/q4/q4_d_buf_time_over_time.png',dpi = 1200)
    plt.show()

    fig, ax = plt.subplots()
    for i in range(4):
        quality_level = results[i][:,5]
        absolute_time = results[i][:,0]-results[i][0,0]

        if debug:
            print(time_buffered)
            print(absolute_time)
            print(type(results[i][0,0]))
            print(results[i][0,0])

        ax.plot(absolute_time, quality_level, color=color[i], ls=line_style[i], linewidth=1)#, marker="o")
        ax.set(title='quality level over time',
            ylabel='quality level',
            xlabel='time [s]')
        #ax.xaxis.set(ticks=[18, 30, 48])
        #ax.set_xticklabels(["crf-18/Br-2205k", "crf-30/Br-334k", "crf-48/Br-36k"])
        #ax.yaxis.set(ticks=values_psnr[:, 1])
        ax.legend(legend)
    plt.savefig('../../images/q4/q4_e_quality_level_over_time.png',dpi = 1200)
    plt.show()


def plot_q4_f(results, debug):

    legend=["doubled average bandwidth for crf=18", "average bandwidth for crf=18", "average bandwidth for crf=23", "average bandwidth for crf=28"]
    #fig, ax = plt.subplots()
    quality_level = []
    time_buffered = []

    for i in range(4):
        quality_level.append(sum(results[i][:,5])/results[i].shape[0])
        time_buffered.append(sum(results[i][:,2])/results[i].shape[0])

        if debug:
            print(results[i].size)
            print(results[i].shape)
            print(quality_level)
            print(time_buffered)



    # ax.plot(absolute_time, quality_level, color=color[i], ls=line_style[i], linewidth=1)#, marker="o")
    # ax.set(title='quality level over relative time',
    #     ylabel='quality level',
    #     xlabel='relative time [s]')
        #ax.xaxis.set(ticks=[18, 30, 48])
        #ax.set_xticklabels(["crf-18/Br-2205k", "crf-30/Br-334k", "crf-48/Br-36k"])
        #ax.yaxis.set(ticks=values_psnr[:, 1])
    # ax.legend(legend)
    #plt.savefig('../../images/q4/q4_e_quality_level_over_time.png',dpi = 1200)
    #plt.show()

    N = 4

    ind = np.arange(N)    # the x locations for the groups
    width = 0.3       # the width of the bars: can also be len(x) sequence

    fig, ax1 = plt.subplots()
    p1 = ax1.bar(ind-width/2, time_buffered, width, color="green")
    ax2 = ax1.twinx()
    p2 = ax2.bar(ind+width/2, quality_level, width, color="purple")
    

    ax1.set_ylabel('Average buffer level [buffered seconds]')
    ax2.set_ylabel('Average quality level')
    plt.title('Average buffer level and average quality level')
    plt.xlabel('Network bandwidth')
    plt.xticks(ind, legend)#, rotation=90)
    plt.legend((p1[0], p2[0]), ('Average quality level', 'Average buffer level'))

    plt.savefig("../../figures/q4_f_average_quality_and_buffer_level.png")
    plt.show()

def main():
    results=[]
    #TODO help
    for arg in sys.argv[1:]:
        results.append(import_log(arg,debug))
    #plot_q4_d_and_e(results, debug)
    plot_q4_f(results, debug)

if __name__ == "__main__":
    main()