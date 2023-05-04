from Monitor.NetworkMonitor import NetworkDelayMonitor,NetworkMonitor,MonitorType,NetworkBandWidthMonitor
from containernet.node import DockerSta
from OSM_Mininet_wifi.node import OSMDockerStaion,OSMDockerCloud
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel,output
from mn_wifi.mobility import Mobility
from mininet.node import Controller
from OSM_Mininet_wifi.net import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP

setLogLevel('info')
net = OSM_Mininet_wifi(controller=Controller,autoAssociation=False)


net.addStation(**{'type': 'mp', 'name': 'mp0', 'location': ['28.22816205797328,112.96747982609853', '28.22816205797328,112.98601854272884'], 'position': '4580,1961,0', 'ip': '10.0.0.1/8', 'ip6': '2001:0:0:0:0:0:0:1/64', 'mac': '00:00:00:00:00:01', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}, 'NodeMobilityConfig': {'speed': 50, 'distance': 0}},cls=OSMDockerStaion)
net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
net.configureWifiNodes()
net.start()
thread_list = []
for td in thread_list: td.join()
net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230409112900176742.json')
net.stop()
