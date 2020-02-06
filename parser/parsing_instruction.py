"""
parsing_instructions.py: allows for different data to be parsed, so not all is including in the output file
"""

class Parsing_Instruction:

    def __init__(self):
        self.recv = False
        self.proto = False
        self.flow = False
        self.seq = False
        self.src = False
        self.dst = False
        self.sent = False
        self.size = False
        self.gps = False
