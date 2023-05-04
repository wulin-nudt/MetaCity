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
# from OSM_Mobility

setLogLevel('info')
net = OSM_Mininet_wifi(controller=Controller,autoAssociation=False)


net.addAccessPoint(**{'type': 'bs', 'name': 'bs0', 'location': [28.195864947632028, 112.96736951933948], 'position': [-199, -14, 0], 'ssid': 'ssid-bs0', 'ip': '10.0.0.1/8', 'ip6': '2001:0:0:0:0:0:0:1/64', 'mac': '00:00:00:00:00:01', 'range': 500, 'failMode': 'standalone'})
net.addDocker(**{'type': 'ec', 'name': 'ec0', 'location': [28.196338160777877, 112.96642547736965], 'position': [-291, 39, 0], 'ip': '10.0.0.2/8', 'ip6': '2001:0:0:0:0:0:0:2/64', 'mac': '00:00:00:00:00:02', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addAccessPoint(**{'type': 'ap', 'name': 'ap1', 'location': [28.19556232117876, 112.9737639534327], 'position': [428, -47, 0], 'ssid': 'ssid-ap1', 'ip': '10.0.0.3/8', 'ip6': '2001:0:0:0:0:0:0:3/64', 'mac': '00:00:00:00:00:03', 'range': 10, 'failMode': 'standalone'})
net.addDocker(**{'type': 'ec', 'name': 'ec1', 'location': [28.195676144688957, 112.97494411056424], 'position': [544, -35, 0], 'ip': '10.0.0.4/8', 'ip6': '2001:0:0:0:0:0:0:4/64', 'mac': '00:00:00:00:00:04', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addStation(**{'type': 'mp', 'name': 'mp0', 'location': ['28.19389840746284,112.96606063760356'], 'position': '-327,-232,0', 'ip': '10.0.0.5/8', 'ip6': '2001:0:0:0:0:0:0:5/64', 'mac': '00:00:00:00:00:05', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}, 'NodeMobilityConfig': {'speed': 50, 'distance': 0}},cls=OSMDockerStaion)
net.addStation(**{'type': 'mp', 'name': 'mp1', 'location': ['28.193381548684243,112.96931475555427'], 'position': '-8,-290,0', 'ip': '10.0.0.6/8', 'ip6': '2001:0:0:0:0:0:0:6/64', 'mac': '00:00:00:00:00:06', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}, 'NodeMobilityConfig': {'speed': 50, 'distance': 0}},cls=OSMDockerStaion)
net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
net.configureWifiNodes()
net.addLink(**{'type': 'nl', 'node1': 'bs0', 'node2': 'ec0', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'bs0', 'node2': 'ap1', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'ap1', 'node2': 'ec1', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.start()
thread_list = []
for td in thread_list: td.join()
net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230503000757325886.json')
net.stop()
