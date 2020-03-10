from core.emulator.coreemu import CoreEmu
from core.emulator.emudata import IpPrefixes, LinkOptions
from core.emulator.enumerations import EventTypes
from core.emulator.enumerations import NodeTypes
import subprocess
import logging

DEBUG = True

def test_network():
    # ip generator for example

    prefixes = IpPrefixes(ip4_prefix="10.83.0.0/16")

    if DEBUG:
        result = str(subprocess.run(['tc', 'qdisc', 'show'], stdout=subprocess.PIPE).stdout)
        print(result)
        
        for line in str(result).split("\n"):
            pass
            #print(line)
        print("\n\n\n")

    # create emulator instance for creating sessions and utility methods

    coreemu = CoreEmu()


    session = coreemu.create_session()

    # must be in configuration state for nodes to start, when using "node_add" below

    session.set_state(EventTypes.CONFIGURATION_STATE)

    # create switch network node

    switch = session.add_node(_type=NodeTypes.SWITCH)

    lo = LinkOptions()
    lo.jitter = 1000
    # create nodes
    for _ in range(2):
        #print("ADDING NODE")
        node = session.add_node()

        interface = prefixes.create_interface(node)
        session.add_link(node.id, switch.id, interface_one=interface, link_options=lo)
        #session.add_link(node.id, switch.id, interface_one=interface)

    session.instantiate()
    if DEBUG:
        result = subprocess.run(['tc', 'qdisc', 'show'], stdout=subprocess.PIPE)
        print("\n\n\n")
        print(result.stdout)
    session.shutdown()


    coreemu.shutdown()

if __name__ in ['__main__', "__builtin__"]:
    test_network()
