from parsing_instruction import Parsing_Instruction
import matplotlib.pyplot as plt
import os
import re
num_flows = 0

"""
parser.py: parses a directory contianing MGEN logging files. From them it creates a corresponding latency file, and from that it creates a corresponding age file

NOTE: 
1. When creating the log file names in your directory, label them sequential in the way you want the latency and age files to be created by putting a number in there somewhere. So if you
wanted files traffic1.log, traffic2.log, and traffic5.log parsed, they would correspond to age1.log, age2.log, age5.log respectively. 

2. include the string "traffic" in your MGEN logging file names
"""


"""
Creates a file with the timestamps to be used later. The file format is for each parameter, it prints that parameter name and then
all of the data corresponding to it below, then goes on to the next parameter. It prints to seperate files based on flow

This is not used to replicate the experiements of the paper, but it could be used so I kept it in the code

:param array[dict] data: an array of dictionaries, each one holding the timestamp data
:param string write_name: name of file to write to
:return: None
"""
def write_to_file(data, write_name):

    for flow in range(1, num_flows+1):
        with open(write_name + str(flow) + ".txt", "w") as f:
            for key in data[0].keys():
                if key != "flow":
                    f.write(key + "\n")
                    for i in range(len(data)):
                        if data[i]["flow"] == str(flow):
                            f.write(data[i][key] + "\n")
        

"""
Prints a data entry

:param dict data: holds all data from each timestamp entry
:return: None
"""
def print_data_entry(data):
    for key in data:
        print(key, ":", data[key])


"""
Parses a specific timestamp and stores it in a dictionary

:param string timestmap: a specific entry from log file
:return: dict
"""
def parse_timestamp(timestamp, instruction):
    info = timestamp.split(" ")
    parsed_data = {}
    if instruction.recv:
        parsed_data["recv"] = info[0]
    

    for line in info[2:]:
        tmp = line.split(">")

        if tmp[0] == "flow":
            parsed_data[tmp[0]] = tmp[1]
            global num_flows
            num_flows = max(num_flows, int(tmp[1]))
        
        if tmp[0] == "proto" and instruction.proto:
            parsed_data[tmp[0]] = tmp[1]
            
        elif tmp[0] == "seq" and instruction.seq:
            parsed_data[tmp[0]] = tmp[1]

        elif tmp[0] == "src" and instruction.src:
            parsed_data[tmp[0]] = tmp[1]

        elif tmp[0] == "dst" and instruction.dst:
            parsed_data[tmp[0]] = tmp[1]

        elif tmp[0] == "sent" and instruction.sent:
            parsed_data[tmp[0]] = tmp[1]

        elif tmp[0] == "size" and instruction.size:
            parsed_data[tmp[0]] = tmp[1]

        elif tmp[0] == "gps" and instruction.gps:
            parsed_data[tmp[0]] = tmp[1]

    return parsed_data


"""
Does subtraction with two time stamps

:param string: t1
:param string: t2
"""
def subtract(t1, t2):
    return round(convert_timestamp(t1) - convert_timestamp(t2), 6)

"""
Converts a timestamp to seconds

:param float: time
:return float:
"""
def convert_timestamp(time):
    to_add = 0.0
    fact = 60 * 60
    tmp = time.split(":")

    for num in tmp[:-1]:
        to_add += int(num) * fact
        fact /= 60

    tmp = tmp[-1].split(".")
    to_add += float(tmp[0]) + float("." + tmp[-1])

    return round(to_add, 6)

"""
Parses the entire log file

:param string directory_name: the name of the directory containing traffic files
:param instruction instruction: some instructions for the parsing
"""
def parse_file(directory_name, instruction):
    if directory_name[-1] != "/":
        directory_name += "/"

    files = None
    try:
        files = sorted([file for file in os.listdir(directory_name) if "traffic" in file], key = lambda x: int(''.join(re.findall(r'\d+', x))))
    except:
        print("Directory Not Found")
        return

    for file_name in files:
        all_data = []

        with open(directory_name + file_name, "r") as f:
            lines = f.read().split("\n")
            for ts in lines:
                if len(ts) and "RECV" in ts and "sent" in ts:
                    all_data.append(parse_timestamp(ts, instruction))


        file_num = ''.join(re.findall(r'\d+', file_name))
        latency_file_name = directory_name + "latency" + file_num + ".txt"
        write_latency_file(all_data, latency_file_name)

        age_file_name = directory_name + "age" + file_num + ".txt"
        write_age_file(latency_file_name, age_file_name, plot=False)


"""
Writes to the output file, writes the sequence, latency, and reception time

:param array[dict] data: an array of dictionaries, each one holding the timestamp data
:param string file_name: name of file to write to
:param int file_num: counter of file
:return: None
"""
def write_latency_file(data, file_name):
    with open(file_name, "w") as f:
        for entry in data:
            f.write("sequence:" + entry["seq"] + "|latency:" + str(subtract(entry["recv"], entry["sent"])) + "|reception:" + str(subtract(entry["recv"], data[0]["sent"])) + "|generation:" + str(subtract(entry["sent"], data[0]["sent"])) + "\n")
        f.write("total run time:" + str(subtract(data[-1]["recv"], data[0]["recv"])) + "\n")


"""
Creates a file that stores age as a function of time and calculates average age and average peak age

:param string file_name: name of file
:param int file_num: counter of file
:return: None
"""
def write_age_file(file_name, output_file_name, plot=False):
    n = 10**6
    m = {}
    total_time = None
    generation = []

    #stores all values in m from latency files, and also stores total time of the run
    with open(file_name, "r") as f:
        for line in f.read().split("\n"):
            if len(line):
                if "sequence" in line:
                    line = line.split("|")
                    m[int(line[0].split(":")[1])] = [float(line[1].split(":")[1]), float(line[2].split(":")[1])]
                    generation.append(float(line[3].split(":")[1]))
                else:
                    total_time = float(line.split(":")[1])

    #an array of each millionth of a second from 0 to total_time
    time = [round(i*(1/(n)), 6) for i in range(int(total_time*n) + 1)]
    age = []



    latency_x = [] #for plotting purposes only
    latency_y = []


    curr_age = None
    seq = 0
    for t in time:
        if t == 0:
            latency_x.append(t)
            latency_y.append(m[seq][0])
            curr_age = m[seq][0]
            seq += 1
        elif t >= m[seq][1]:
            latency_x.append(m[seq][1])
            latency_y.append(m[seq][0])
            curr_age = m[seq][0]
            seq += 1
        else:
            curr_age += time[1]

        age.append(round(curr_age, 6))

    time = time[0:len(age)]

    if plot:
        gen = [generation[i] for i in range(1, len(generation)) if generation[i] <= time[-1]]
        x = [0 for i in range(len(gen))]
        plt.plot(time, age, color="green", label= "Age")
        plt.scatter(gen, x, color="red", label="Packet Generation")
        plt.scatter(latency_x, latency_y, label="Latency", s=50, facecolors='none', edgecolors='b')
        plt.axis("scaled")
        plt.legend()
        plt.xlim(0, 2.5)
        plt.xlabel("Time (sec)")
        plt.ylabel("Age (sec)")
        plt.show()


    #writing to the file
    latency = [m[key][0] for key in m.keys()]
    interarrival = [generation[i] - generation[i-1] for i in range(1, len(generation))]
    with open(output_file_name, "w") as f:
        f.write("Average Age:" + str(sum(age)/len(age)) + "\n")
        f.write("Average Latency:" + str(sum(latency)/len(latency)) + "\n")
        f.write("Average Interarrival:" + str(sum(interarrival)/len(interarrival)) + "\n")


"""
Creates the files needed for experimentation. Put all of your logging files in one directory, the program will generate age files from all of them

:param string directory_name: the name of the directory where you mgen logging files are. 
:param Instruction ins: the parsing instructions 
"""
def create_files(directory_name, ins):
    parse_file(directory_name, ins)


if __name__=='__main__':
    """
    0: lambda = .1
    1: lambda = 1
    i: lambda = i for i = 2, ... , 9
    10: lambda = 9.5
    11: lambda = 9.9
    """

    ins = Parsing_Instruction(recv=True, sent=True, seq=True)
    create_files("/home/jm/Desktop/CORE_Research/parser/data", ins)

