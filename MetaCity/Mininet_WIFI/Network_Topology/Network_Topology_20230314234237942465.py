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


net.addStation(**{'type': 'mp', 'name': 'mp1', 'location': ['39.96541148221848,116.27891096048208', '39.96845140501534,116.29512848896013'], 'position': '-556,349,0', 'ip': '10.0.0.8/8', 'ip6': '2001:0:0:0:0:0:0:8/64', 'mac': '00:00:00:00:00:08', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 50, 'coord': ['-600,338,0', '-386,355,0', '-384,345,0', '-315,233,0', '-306,219,0', '-236,106,0', '-226,88,0', '-161,-24,0', '-156,-34,0', '-99,-160,0', '-85,-173,0', '-79,-181,0', '6,-329,0', '37,-430,0', '39,-437,0', '108,-434,0', '116,-563,0', '116,-570,0', '115,-575,0', '111,-579,0', '-25,-616,0', '-26,-622,0', '-24,-633,0', '189,-584,0', '406,-533,0', '549,-499,0', '609,-485,0', '644,-475,0', '651,-474,0', '688,-466,0', '698,-464,0', '862,-425,0', '927,-406,0', '990,-381,0', '989,-371,0', '977,-243,0', '965,-144,0', '962,-114,0', '961,-109,0', '959,-88,0', '945,31,0', '945,39,0', '936,113,0', '935,121,0', '923,229,0', '914,310,0', '909,347,0', '907,371,0', '904,394,0', '879,542,0', '840,651,0', '827,690,0'], 'distance': 3626.669160264288}, 'node': 'mp1'})
net.addAccessPoint(**{'type': 'bs', 'name': 'bs3', 'location': [39.96261776329325, 116.28363132476808], 'position': [-154, 38, 0], 'ssid': 'ssid-bs3', 'ip': '10.0.0.9/8', 'ip6': '2001:0:0:0:0:0:0:9/64', 'mac': '00:00:00:00:00:09', 'range': 1000, 'failMode': 'standalone'})
net.addAccessPoint(**{'type': 'bs', 'name': 'bs4', 'location': [39.96169632050622, 116.29908084869386], 'position': [1163, -64, 0], 'ssid': 'ssid-bs4', 'ip': '10.0.0.10/8', 'ip6': '2001:0:0:0:0:0:0:10/64', 'mac': '00:00:00:00:00:0a', 'range': 1000, 'failMode': 'standalone'})
net.addStation(**{'type': 'mp', 'name': 'mp4', 'location': ['39.95866695973487,116.29741042074008'], 'position': '1021,-401,0', 'ip': '10.0.0.13/8', 'ip6': '2001:0:0:0:0:0:0:13/64', 'mac': '00:00:00:00:00:0d', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}, 'NodeMobilityConfig': {'speed': 50, 'coord': 0, 'distance': 0}},cls=OSMDockerStaion)
net.addStation(**{'type': 'mp', 'name': 'mp5', 'location': ['39.96016712617505,116.2745705052664', '39.95615652100979,116.27869148773114'], 'position': '-926,-234,0', 'ip': '10.0.0.14/8', 'ip6': '2001:0:0:0:0:0:0:14/64', 'mac': '00:00:00:00:00:0e', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 50, 'coord': ['-952,-241,0', '-639,-230,0', '-646,-245,0', '-644,-280,0', '-639,-306,0', '-637,-313,0', '-629,-412,0', '-624,-438,0', '-597,-695,0', '-591,-716,0', '-586,-694,0'], 'distance': 825.138568431186}, 'node': 'mp5'})
net.addDocker(**{'type': 'ec', 'name': 'ec3', 'location': [39.964736299491115, 116.28500174213032], 'position': [-37, 274, 0], 'ip': '10.0.0.15/8', 'ip6': '2001:0:0:0:0:0:0:15/64', 'mac': '00:00:00:00:00:0f', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addDocker(**{'type': 'ec', 'name': 'ec4', 'location': [39.963815915036804, 116.30097054918127], 'position': [1324, 172, 0], 'ip': '10.0.0.16/8', 'ip6': '2001:0:0:0:0:0:0:16/64', 'mac': '00:00:00:00:00:10', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
net.configureWifiNodes()
net.addLink(**{'type': 'nl', 'node1': 'ec4', 'node2': 'bs4', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'ec3', 'node2': 'bs3', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.OSM_Mobility_Setting(**{'mobility_start_time': 1, 'reverse': 0, 'ac_method': 'ssf', 'mob_rep': 1, 'mobility_mode': 'quickly'})
net.start()
thread_list = []
t=NetworkDelayMonitor('mp1', 'ec3', net, monitor_type= {'delay'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230314234237942465.json',**{'period': 50}).thread_
thread_list.append(t)
t=NetworkBandWidthMonitor('mp1', 'ec3', net, monitor_type= {'band_width'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230314234237942465.json',**{'period': 50}).thread_
thread_list.append(t)
t=NetworkDelayMonitor('mp1', 'ec4', net, monitor_type= {'delay'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230314234237942465.json',**{'period': 50}).thread_
thread_list.append(t)
t=NetworkBandWidthMonitor('mp1', 'ec4', net, monitor_type= {'band_width'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230314234237942465.json',**{'period': 50}).thread_
thread_list.append(t)
for td in thread_list: td.join()
net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230314234237942465.json')
net.stop()
