def parse_timestamp(timestamp):
    info = timestamp.split(" ")
    parsed_data = {}
    parsed_data["recv"] = info[0]

    for line in info[2:]:
        tmp = line.split(">")
        if len(tmp) == 2:
            parsed_data[tmp[0]] = tmp[1]

    for key in parsed_data:
        print(key, ":", parsed_data[key])
    
        

def parse_file(file_name):
    with open(file_name, "r") as f:
        lines = f.read().split("\n")
        for ts in lines[3:]:
            parse_timestamp(ts)
            break

    

if __name__=='__main__':
    parse_file("new1.log")
