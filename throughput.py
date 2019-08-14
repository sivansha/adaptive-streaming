import numpy as np
import matplotlib.pyplot as plt
import sys
import os


def run_program(folder_path, debug):
    results = []
    logs = get_logs_from_folder(os.path.abspath(folder_path), debug)
    for log in logs:
        print("    [*] Collecting data from log: "+log)

        results.append(import_log(folder_path+log , debug))
    plot_bwe(np.array(results),debug)


def plot_bwe(results, debug):
    fig, ax = plt.subplots(num=None, figsize=(20, 11), dpi=80, facecolor='w', edgecolor='k')

    for i in range(results.shape[0]):
        bwe = results[i][:,1]
        absolute_time = results[i][:,0]-results[i][0,0]

        color = ["blue", "red", "orange"]
        line_style = ["--", ":", "-."]

        ax.plot(absolute_time, bwe, color=color[i], ls=line_style[i])#, linewidth=1)#, marker="o")
        ax.set(title='Bandwidth estimation over time for three simultaneous streams with actual network of 3Mb/s',
            ylabel='Bandwidth Estimation [kbit/s]',
            xlabel='Time [s]')
        legend = ["Stream 1","Stream 2","Stream 3"]
        ax.legend(legend)
    plt.savefig('../figures/bwe_over_time.png')
    plt.show()


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

def import_log(file_name, debug):
    result_list =[]
    with open(file_name) as file:
        file.readline()
        for line in file.readlines():
            if debug: print(line)
            
            line = line.split(" ")
            line = list(map(float,line))
            result_list.append([line[0],line[3]])
            #print(result_list)
    return np.array(result_list)


def main():
    #print(len(sys.argv))
    debug = False
    if len(sys.argv) < 2 or len(sys.argv) >3 :
        print(
            """

    Usage: python3 throughput.py [-d] path/to/log_dir

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
