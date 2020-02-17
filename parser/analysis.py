import matplotlib.pyplot as plt

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

    :param None:
    :return: None
    """
    def calculate_average(self):
        cache = {}

        curr_key = 1
        cache[curr_key] = 0
        curr = int(self.data[0])

        for time in self.data:
            if curr == int(time):
                cache[curr_key] += 1
            else:
                curr = int(time)
                curr_key += 1
                cache[curr_key] = 1

        num_seconds = len(cache.keys())-2
        tot = 0
        for key in list(cache.keys())[1:-1]:
            tot += cache[key]*125
        print(tot/num_seconds)

        print(cache)


    """
    For looking at data with matplotlib
    
    :param None
    :return: None
    """
    def display_data(self):
        cache = {}

        curr_key = 1
        cache[curr_key] = 0
        curr = int(self.data[0])

        for time in self.data:
            if curr == int(time):
                if curr_key in cache:
                    cache[curr_key] += 1
            else:
                curr = int(time)
                curr_key += 1
                cache[curr_key] = 1

        x = list(cache.keys())
        y = list(cache.values())
        print(len(x))

        plt.scatter(x, y)
        plt.show()


    """
    Parses file for data
    
    :param None:
    :return: list
    """
    def extract_data(self):
        to_ret = []

        with open(self.fn, "r") as f:
            lines = f.read().split("\n")
            for line in lines[:-1]:

                #Converting timestamp to seconds
                to_add = 0.0
                tmp = line.split("-")[1].split(".")
                fact = 60*60
                for num in tmp[0].split(":"):
                    to_add += int(num)*fact
                    fact/=60
                to_add += float("." + tmp[-1])
                to_ret.append(to_add)

        return to_ret


if __name__=='__main__':
    a = Analysis("output1.txt")
    a.calculate_average()
    #a.display_data()