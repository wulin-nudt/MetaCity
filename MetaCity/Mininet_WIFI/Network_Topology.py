from containernet.node import DockerSta
from OSM_Mininet_wifi.node import OSMDockerStaion
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel
from mininet.node import Controller
from OSM_Mininet_wifi.net import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP

class Network_Topology(OSM_Mininet_wifi):

    def generate_topology(self,network_data={}):
        if not network_data:
            self.network_topology=network_data

        setLogLevel('info')

        for k ,v in network_data.items():
            if v['type'] in ['MovingPoint','EdgeCloud']:
                self.addStation(**v)
            elif v['type'] in ['WirelessAccessPoint']:
                self.addAccessPoint(**v)

        self.addController('c1', controller=Controller)

        self.configureWifiNodes()


        for k ,v in network_data.items():
            if v['type'] in ['NetWorkLink']:
                self.addLink(**v)

        self.start()

        CLI(self)
        self.stop()



