import matplotlib.pyplot as plt
import statistics
import numpy as np
import argparse
import re

def extract_delay(filename):
    lines = []
    # store all lines in vehicle delay file
    with open(filename, 'r') as veh_delay_file:
        for line in veh_delay_file:
            lines.append(line)
    
    # remove empty lines
    veh_data = []
    for i in range(15, len(lines)): # line 16 is where the actual data starts
        if not lines[i].isspace(): # checks if line only contains white space...if false
            veh_data.append(lines[i].split())

    for entry in veh_data:
        veh_name = re.split('_|\.',entry[0]) # split up entire veh name into sub-components
        entry.append(veh_name[1]) # 16th element: vehicle lane (e.g. "EC3")


    checked_veh = [] # for vehicles that have been checked
    total_delay = []
    veh = {}
    for i in range(len(veh_data)):
        if (veh_data[i][0] not in checked_veh):
            total_veh_delay = 0
            veh_name = veh_data[i][0] # e.g. "veh_EC3.0" 
            veh_lane = veh_data[i][16] # e.g. "EC3" or "NC4"; 16th element created above

            indices = [idx for idx, x in enumerate(veh_data) if x[0] == veh_name] # get indices with the same vehicle name
            
            for index in indices:
                total_veh_delay += float(veh_data[index][12]) # calculate total delay for vehs that go through multiple intersections
                
            veh = {veh_name:total_veh_delay} #{'key':'value'}; {vehicle name: total vehicle delay}
            total_delay.append(veh) 
            checked_veh.append(veh_name) # array of vehs that have been calculated already

    return total_delay


def prep_data(total_delay):
    delays = []

    for delay in total_delay: # get each dict entry in list
        for value in delay.itervalues(): # get the value from each dict
            delays.append(value) # add to list of all delays

    return delays



def plot(data, filename):
    # acquire attack rates for xtick labels
    atk_rate = []
    for fn in filename:
        atk_rate.append( fn.split(".txt")[0] )

    fig, ax = plt.subplots()
    ax.boxplot(data, 0, 'r+')

    #get ylim
    ylim = ax.get_ylim()
    ax.set_ylim(ylim[0], ylim[1]+50) # ylim[0]: bottom; ylim[1]: top
    
    pos = np.arange(len(filename)) + 1
    for tick, label in zip(range(len(filename)), ax.get_xticklabels()):
        #k = tick % 2
        median = statistics.median(data[tick])        
        ax.text(pos[tick], ylim[1] + 10, median,
                 horizontalalignment='center', size='x-small', weight='bold')

    ax.set_axisbelow(True)
    ax.set_title('Backpropagation HOL Delay (60s Left Max Out; 120s Straight Max Out)')
    ax.set_xticklabels(atk_rate, fontsize=8) # removed: rotation=45
    ax.set_xlabel('Attack Rates (attacker per vehicle)')
    ax.set_ylabel('Delay (s)')
    #plt.ylim(-50, 800)
    plt.gcf().set_size_inches(12, 6)
    plt.show()
    plt.clf()


def main():
    # command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", nargs='+', help="input the name of the file that you want to plot", type=str, required=True)
    args = parser.parse_args()

    data = []
    for fn in args.filename:    
        total_delay = extract_delay(fn)
        data.append( prep_data(total_delay) )

    plot(data, args.filename)



if __name__== "__main__":
    main()
