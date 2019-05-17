import matplotlib.pyplot as plt
import statistics
import numpy as np
import argparse
import re

def extract_delay(filename, intersections):
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


    total_delay = {}
    veh = {}

    for TL in intersections:
        total_delay["total_delay_" + TL] = []
        

    for i in range(len(veh_data)):
        total_veh_delay = 0
        total_veh_delay = float(veh_data[i][12])
        veh_name = veh_data[i][0] # e.g. "veh_EC3.0" or "veh_route9.0"
        veh_lane = veh_data[i][16] # e.g. "EC3" or "NC4" or "route9"; 16th element created above
            
        veh = {veh_name:total_veh_delay} #{'key':'value'}; {vehicle name: total vehicle delay}
        total_delay["total_delay_combined"].append(veh)

        for TL in intersections:
            if veh_data[i][2] == TL:
                total_delay["total_delay_" + TL].append(veh)

    return total_delay


def prep_data(total_delay, intersections):
    extracted_delays = {}
    for TL in intersections:
        extracted_delays["total_delay_" + TL] = []


    ### creating a list of only each vehicle's delay value
    for TL, delays in total_delay.iteritems(): # e.g. "TL": total_delay_65309555; "delays": [{'veh_route1.0': 0.0}, {'veh_route1.1': 0.0}, {'veh_route1.10': 126.1}]
        for value in delays: # e.g. {'veh_route1.0': 0.0} or {'veh_route1.10': 126.1}
            extracted_delays[TL].append(value.values()[0]) # e.g. 0, 0, 126.1

    return extracted_delays



def plot(data, directory, filename, intersections):
    for TL in intersections:
        key_name = "total_delay_"+TL
        print key_name
        # acquire attack rates for xtick labels
        atk_rate = []
        for fn in filename:
            atk_rate.append( fn.split(".txt")[0] )

        fig, ax = plt.subplots()
        ax.boxplot(data[key_name], 0, 'r+')

        #get ylim
        ylim = ax.get_ylim()
        ax.set_ylim(ylim[0], ylim[1]+50) # ylim[0]: bottom; ylim[1]: top
        
        pos = np.arange(len(filename)) + 1
        for tick, label in zip(range(len(filename)), ax.get_xticklabels()):
            #k = tick % 2
            median = statistics.median(data[key_name][tick])        
            ax.text(pos[tick], ylim[1] + 10, median,
                     horizontalalignment='center', size='x-small', weight='bold')

        ax.set_axisbelow(True)
        ax.set_title('Backpropagation HOL Delay (2 Intersections)')
        ax.set_xticklabels(atk_rate, fontsize=8) # removed: rotation=45
        ax.set_xlabel('Attack Rates (attacker per vehicle)')
        ax.set_ylabel('Delay (s)')
        #plt.ylim(-50, 800)
        plt.gcf().set_size_inches(12, 6)
        #plt.show()
        save_title = directory[0] + "/" + key_name + '.png'
        plt.savefig(save_title)
        plt.clf()
    

def main():
    # command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", nargs='+', help="input the name of the file that you want to plot", type=str, required=True)
    parser.add_argument("-d", "--directory", nargs=1, help="directory that files are located at", type=str)
    parser.add_argument("-i", "--intersections", nargs='+', help="input the TL names that are present in your intersection", type=str)
    args = parser.parse_args()

    folder = args.directory[0]
    args.intersections.append("combined")

    data = {}
    for TL in args.intersections:
        data["total_delay_" + TL] = []

    for fn in args.filename:  
        filepath = folder + "/" + fn
        print filepath
        total_delay = extract_delay(filepath, args.intersections)
        
        extracted_data = prep_data(total_delay, args.intersections)
        for key, value in extracted_data.iteritems():
            data[key].append(value)

    plot(data, args.directory, args.filename, args.intersections)



if __name__== "__main__":
    main()
