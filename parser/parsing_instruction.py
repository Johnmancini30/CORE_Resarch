"""
parsing_instructions.py: allows for different data to be parsed, so not all is including in the output file
"""

class Parsing_Instruction:

    def __init__(self, recv=False, proto=False, flow=False, seq=False, src=False, dst=False, sent=False, size=False, gps=False):

        self.recv = recv
        self.proto = proto
        self.flow = flow
        self.seq = seq
        self.src = src
        self.dst = dst
        self.sent = sent
        self.size = size
        self.gps = gps
