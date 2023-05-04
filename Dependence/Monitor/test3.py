from Monitor.NetworkMonitor import NetworkDelayMonitor,NetworkMonitor
from containernet.node import DockerSta
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel
from mininet.node import Controller
from OSM_Mininet_wifi.net import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP
setLogLevel('info')
net = OSM_Mininet_wifi(controller=Controller,allAutoAssociation=False)
sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range='20',position='20,50,0',cls=DockerSta, dimage="ubuntu:test")
sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', range='20',position='40,50,0',cls=DockerSta, dimage="ubuntu:test")
sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8', range='20',position='60,50,0',cls=DockerSta, dimage="ubuntu:test")
ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='30,50,0', range='30')
ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='1', position='90,50,0', range='30')
ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='1', position='130,50,0', range='30')
c1 = net.addController('c1', controller=Controller)
sta1.cmd()

net.configureWifiNodes()

# net.addLink(sta1, ap1)
# net.addLink(sta2, ap1)
# net.addLink(ap1, ap2)
# net.addLink(ap2, ap3)
net.build()
CLI(net)
net.stop()