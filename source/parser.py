from parsing_instruction import Parsing_Instruction
import matplotlib.pyplot as plt
import os
import re

DEBUG = True

"""
parser.py: parses a directory containing MGEN logging files. From them it creates a corresponding latency file, and from that it creates a corresponding age file

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
    for flow in range(1, num_flows + 1):
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
        files = sorted([file for file in os.listdir(directory_name) if "traffic" in file],
                       key=lambda x: int(''.join(re.findall(r'\d+', x))))
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
            f.write("sequence:" + entry["seq"] + "|latency:" + str(
                subtract(entry["recv"], entry["sent"])) + "|reception:" + str(
                subtract(entry["recv"], data[0]["sent"])) + "|generation:" + str(
                subtract(entry["sent"], data[0]["sent"])) + "\n")
        f.write("total run time:" + str(subtract(data[-1]["recv"], data[0]["recv"])) + "\n")


"""
Creates a file that stores age as a function of time and calculates average age and average peak age

:param string file_name: name of file
:param int file_num: counter of file
:return: None
"""


def write_age_file(directory_name):
    if directory_name[-1] != "/":
        directory_name += "/"

    files = None
    try:
        files = sorted([file for file in os.listdir(directory_name) if "latency" in file],
                       key=lambda x: int(''.join(re.findall(r'\d+', x))))
    except:
        print("Directory Not Found")
        return

    for file_name in files:
        arrival = []
        reception = []
        serTimes = []

        with open(directory_name + file_name) as f:
            for line in f.read().split("\n"):
                if "sequence" in line:
                    line = line.split("|")
                    serTimes.append(float(line[1].split(":")[1]))
                    arrival.append(float(line[3].split(":")[1]))
                    reception.append(float(line[2].split(":")[1]))

        interArrTimes = [0] + [arrival[i] - arrival[i - 1] for i in range(1, len(arrival))]

        # age of information calculation
        n = len(arrival)
        total_time = reception[-1]
        Q1 = (reception[1] - arrival[0]) ** 2 / 2 - (reception[1] - arrival[1]) ** 2 / 2 - arrival[0] ** 2 / 2

        total_AoI = Q1
        total_peak_AoI = reception[1]- arrival[0]
        for i in range(2, n):
            Qi = (reception[i] - arrival[i - 1]) ** 2 / 2 - (reception[i] - arrival[i]) ** 2 / 2
            total_AoI += Qi
            total_peak_AoI += reception[i] - arrival[i-1]

        Tn = (reception[-1] - arrival[-1]) ** 2 / 2
        total_AoI += Tn

        avg_AoI = total_AoI / total_time
        avg_peak_AoI = total_peak_AoI/n
        file_num = ''.join(re.findall(r'\d+', file_name))
        latency_file_name = directory_name + "age" + file_num + ".txt"

        # writing to the file
        print("Writing to file:", latency_file_name)
        with open(latency_file_name, "w") as f:
            f.write("Average Age:" + str(avg_AoI) + "\n")
            f.write("Average Peak Age:" + str(avg_peak_AoI) + "\n")
            f.write("Average Latency:" + str(sum(serTimes) / len(serTimes)) + "\n")
            f.write("Average Interarrival:" + str(sum(interArrTimes) / len(interArrTimes)) + "\n")


"""
Creates the files needed for experimentation. Put all of your logging files in one directory, the program will generate age files from all of them

:param string directory_name: the name of the directory where you mgen logging files are. 
:param Instruction ins: the parsing instructions 
"""


def create_files(directory_name, ins):
    parse_file(directory_name, ins)
    write_age_file(directory_name)


if __name__ == '__main__':


    ins = Parsing_Instruction(recv=True, sent=True, seq=True)
    dir = "/home/jm/Desktop/CORE_Research/data/periodic/data"
    for i in range(13):
        dir_name = dir + str(i)
        create_files(dir_name, ins)



