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
    For looking at data with matplotlib
    
    :param None
    :return: None
    """
    def display_data(self):
        x = [i for i in range(1, len(self.data) + 1)]
        plt.plot(x, self.data)
        plt.show()


    """
    Parses file for data
    
    :param None
    :return: list
    """
    def extract_data(self):
        to_ret = []

        with open(self.fn, "r") as f:
            lines = f.read().split("\n")
            for line in lines:
                print(line)
                #TODO convert the timestamp to an float that makes sense, probably just convert it to seconds
                to_ret.append(int(line.split("-")[1]))

        return to_ret

if __name__=='__main__':
    a = Analysis("output.txt")
    a.display_data()