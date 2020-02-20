from parsing_instruction import Parsing_Instruction
import sys

"""
parser.py: parses the log file that is created when MGEN generates traffic
"""

"""
Creates a file with the timestamps to be used later. The file format is for each parameter, it prints that parameter name and then
all of the data corresponding to it below, then goes on to the next parameter

:param array[dict] data: an array of dictionaries, each one holding the timestamp data
:param string write_name: name of file to write to
:return: None
"""
def write_to_file(data, write_name):

    with open(write_name, "w") as f:
        for key in data[0].keys():
            f.write(key + "\n")
            for i in range(len(data)):
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
            
        elif tmp[0] == "flow" and instruction.flow:
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
Parses the entire log file

:param string file_name: name of the log file
:param Parsing_Instruction instruction: allows preference to what should be written
:return: list of dictionaries
"""
def parse_file(file_name, instruction):
    all_data = []
    with open(file_name, "r") as f:
        lines = f.read().split("\n")
        for ts in lines[3:]:
            if len(ts):
                all_data.append(parse_timestamp(ts, instruction))

    return all_data


if __name__=='__main__':
    if len(sys.argv) == 3:
        ins = Parsing_Instruction(recv=True, sent=True)

        data = parse_file(sys.argv[1], ins)
        write_to_file(data, sys.argv[2])
