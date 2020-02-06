from parsing_instruction import Parsing_Instruction


"""
parser.py: parses the log file that is created when MGEN generates traffic
"""

"""
Creates a file with the timestamps to be used later

:param array[dict] data: an array of dictionaries, each one holding the timestamp data
:param string write_name: name of file to write to
:return: None
"""
def write_to_file(data, write_name):
    with open(write_name, "w") as f:
        for entry in data:
            for key in entry:
                f.write(key + "-" + entry[key] + "\n")
    
        

"""
Prints a data entry

:param dict data: holds all data from each timestamp entry
:return: None
"""
def print_data_entry(data):
    for key in data:
        print(key, ":", data[key])


"""
Parses a specific timestamp and stores it in a dictionary, deletes any data
the user does not want

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
:return: None
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
    ins = Parsing_Instruction()
    ins.recv = True
    data = parse_file("new1.log", ins)
    write_to_file(data, "output.txt")
