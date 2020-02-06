from core.emulator.coreemu import CoreEmu
from core.emulator.emudata import IpPrefixes, LinkOptions
from core.emulator.enumerations import EventTypes
from core.emulator.enumerations import NodeTypes
import subprocess
import logging

DEBUG = False

def test_network():
    # ip generator for example

    prefixes = IpPrefixes(ip4_prefix="10.83.0.0/16")

    if DEBUG:
        result = subprocess.run(['tc', 'qdisc', 'show'], stdout=subprocess.PIPE)
        print(result.stdout)

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
        node = session.add_node()

        interface = prefixes.create_interface(node)


        #session.add_link(node.id, switch.id, interface_one=interface, link_options=lo)
        session.add_link(node.id, switch.id, interface_one=interface)


    session.instantiate()
    session.shutdown()

    
    if DEBUG:
        result = subprocess.run(['tc', 'qdisc', 'show'], stdout=subprocess.PIPE)
        print("\n\n\n")
        print(result.stdout)



        
    coreemu.shutdown()

if __name__=='__main__':
    log_format = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s"
    logging.basicConfig(filename='example.log', level=logging.DEBUG, format=log_format)
    test_network()
