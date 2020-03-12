import matplotlib.pyplot as plt
import re

KEY_WORDS = ["recv", "sent", "seq"]
TIME_KEY_WORDS = ["recv", "sent"]
"""
analysis.py: runs analysis on the data that was parsed
"""
class Analysis:

    """
    :param string file_name: file that will be parsed for doing analysis
    """
    def __init__(self, file_name):
        self.fn = file_name
        self.data = self.extract_data()


    """
    To analyze the mean of the data. In the context of received data it makes sense to calculate the average bytes 
    that arrived per second

    :param string: data_type this is to specify which string to use in data dictionary
    :return: None
    """
    def calculate_average(self, data_type):

        cache = {}

        curr_key = 1
        cache[curr_key] = 0
        data = self.data[data_type]
        curr = int(data[0])

        for time in data:
            if curr == int(time):
                cache[curr_key] += 1
            else:
                curr = int(time)
                curr_key += 1
                cache[curr_key] = 1

        num_seconds = len(cache.keys())-2
        tot = 0
        for key in list(cache.keys())[1:-1]:
            tot += cache[key]*125*8




    """
    For looking at data with matplotlib
    
    :param dict: data Conains parameters
    :return: None
    """
    def display_data(self, data, plot_type):
        x = None
        y = None
        x_label = None
        y_label = None

        try:
            x = data["x"]
            y = data["y"]
        except:
            print("Missing x or y data")

        if "x_label" in data:
            plt.xlabel(data["x_label"])
        if "y_label" in data:
            plt.ylabel(data["y_label"])

        if plot_type == "plot":
            plt.plot(x, y)
        elif plot_type == "scatter":
            plt.scatter(x, y)

        plt.show()


    """
    Parses file for data, stores each parameter as key with corresponding list of values
    
    :param None:
    :return: dict of lists
    """
    def extract_data(self):
        to_ret = {}

        with open(self.fn, "r") as f:

            lines = f.read().split("\n")
            curr = None
            i = 0
            while (i < len(lines)):
                if all(c == " " for c in lines[i]):
                    i+= 1
                    continue
                if lines[i] in KEY_WORDS:
                    curr = lines[i]
                    to_ret[curr] = []
                elif curr in TIME_KEY_WORDS:
                    to_ret[curr].append(self.convert_timestamp(lines[i]))
                else:
                    to_ret[curr].append(int(lines[i]))

                i+=1

        return to_ret


    """
    Converts a timestamp to seconds
    
    :param float: time
    :return float:
    """
    @staticmethod
    def convert_timestamp(time):
        to_add = 0.0
        fact = 60*60
        tmp = time.split(":")

        for num in tmp[:-1]:
            to_add += int(num)*fact
            fact/=60

        tmp = tmp[-1].split(".")
        to_add += float(tmp[0]) + float("." + tmp[-1])

        return to_add

    """
    Calculates the age of information with data from one run
    
    :param list: sent A list of times that the packets were sent at
    :param list: recv A list of times when te packets were received
    :return None:
    """
    def calculate_age(self, sent, recv):
        n = 5
        age  = []
        time = []
        sent_time = []

        curr_time = 0
        curr_age = recv[0] - sent[0]
        for i in range(len(sent) - 1):
            curr_age = recv[i] - sent[i]
            age.append(curr_age)
            time.append(curr_time)
            sent_time.append(sent[i+1] - recv[0])
            print(age[-1])
            print(time[-1])
            print(sent_time[-1])


            to_add = (recv[i+1] - recv[i])/n
            for j in range(n):
                curr_time += to_add
                curr_age += to_add
                age.append(curr_age)
                time.append(curr_time)



        print(sent)
        print(recv)

        data = {"x": time, "y": age, "x_label": "Time", "y_label": "Age"}
        plt.scatter(sent_time, [0 for i in range(len(sent_time))])
        self.display_data(data, "plot")

    """
    Sorts the various data by sequence number because sequence number is not always incremental.
    
    :param None:
    :return: None
    """
    def sort_by_sequence(self):
        to_sort = []

        n = len(self.data["seq"])

        for i in range(n):
            to_add = [self.data["seq"][i], "seq"]
            for key in self.data:
                if key != "seq":
                    to_add += [self.data[key][i], key]
            to_sort.append(to_add)

        to_sort = sorted(to_sort)

        tmp = {}
        for val in to_sort:
            for i in range(0, len(val), 2):
                if val[i+1] not in tmp:
                    tmp[val[i+1]] = []

                tmp[val[i+1]].append(val[i])

        for key in tmp:
            self.data[key] = tmp[key]

    """
    This method will remove the ending data where the certain sequences on not incremented by 1, because the traffic flow ended before the were received
    
    :param None:
    :return: None   
    """
    def remove_lost_sequences(self):
        i = 0

        while i < len(self.data["seq"]) - 1 and self.data["seq"][i + 1] - self.data["seq"][i] == 1:
            i += 1
        i = min(i + 1, len(self.data["seq"]))

        self.data["seq"] = self.data["seq"][:i]
        self.data["sent"] = self.data["sent"][:i]
        self.data["recv"] = self.data["recv"][:i]

    """
    Displays the difference in sent time data
    
    :param None:
    :return: None
    """
    def display_sent(self):
        seq = self.data["seq"]
        sent = self.data["sent"]
        recv = self.data["recv"]

        sent_diff = [sent[i + 1] - sent[i] for i in range(len(sent) - 1)]
        x = [i + 1 for i in range(len(sent_diff))]
        avg_diff = sum(sent_diff) / len(sent_diff)
        print("Average time difference for sent packets", avg_diff)
        data = {"x": x, "y": sent_diff, "x_label": "Packet id", "y_label": "Time between sent"}
        self.display_data(data, "scatter")

    """
    Displays the response time data

    :param None:
    :return: None
    """
    def display_response(self):
        seq = self.data["seq"]
        sent = self.data["sent"]
        recv = self.data["recv"]

        process_time = [recv[i] - sent[i] for i in range(len(sent))]
        print("MIN process time", min(process_time))
        print("MAX process time", max(process_time))
        avg_process = sum(process_time) / len(process_time)
        data = {"x": seq, "y": process_time, "x_label": "Packet id", "y_label": "Response Time"}
        print("Average response time for packet", avg_process)
        self.display_data(data, "scatter")


if __name__=='__main__':
    a = Analysis("/home/jm/Desktop/CORE_Research/mgen_queue_experiment/parsed-output--queue.txt")
    a.display_sent()
    a.display_response()
