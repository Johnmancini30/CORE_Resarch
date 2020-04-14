def get_data(file_name):
    serTimes = []
    arrival = []
    total_run_time = None
    with open(file_name) as f:
        for line in f.read().split("\n"):
            if "sequence" in line:
                line = line.split("|")
                serTimes.append(float(line[1].split(":")[1]))
                arrival.append(float(line[3].split(":")[1]))
           
                
                
    interArrTimes = [0] + [arrival[i] - arrival[i-1] for i in range(1, len(arrival))]
    return serTimes, interArrTimes

def calculate_age(file_name):
    serTimes, interArrTimes = get_data(file_name)
    total_run_time = 10.0
    
    requestNum = len(serTimes)

    totalAoI = 0
    lastWaitTime = 0
    totalPeakAoI = 0

    for i in range(1, requestNum):
        lastWaitTime = max(lastWaitTime + serTimes[i-1] - interArrTimes[i], 0)
        totalAoI += interArrTimes[i]*(lastWaitTime + serTimes[i])+(interArrTimes[i]**2)/2
        totalPeakAoI += lastWaitTime + serTimes[i] + interArrTimes[i]

    print("avgAoI:", totalAoI/total_run_time)
    print("avgPeakAoI:", totalPeakAoI/requestNum)
        
    

if __name__=='__main__':
    calculate_age("data6/latency18.txt")
