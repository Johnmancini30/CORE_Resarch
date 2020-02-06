from core.emulator.coreemu import CoreEmu
from core.emulator.emudata import IpPrefixes, NodeOptions
from core.emulator.enumerations import EventTypes
from core.emulator.enumerations import NodeTypes
from core.emane.ieee80211abg import EmaneIeee80211abgModel

# create session and emane network
coreemu = CoreEmu()
session = coreemu.create_session()
session.set_location(47.57917, -122.13232, 2.00000, 1.0)
options = NodeOptions()
options.set_position(80, 50)
emane_network = session.add_node(_type=NodeTypes.EMANE, options=options)

# set custom emane model config
config = {}
session.emane.set_model(emane_network, EmaneIeee80211abgModel, config)

#shutdown session
coreemu.shutdown()
