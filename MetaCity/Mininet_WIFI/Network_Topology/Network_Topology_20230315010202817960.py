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


net.addDocker(**{'type': 'ec', 'name': 'ec0', 'location': [40.05228914276983, 116.31424571700252], 'position': [-355, 124, 0], 'ip': '10.0.0.1/8', 'ip6': '2001:0:0:0:0:0:0:1/64', 'mac': '00:00:00:00:00:01', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addAccessPoint(**{'type': 'bs', 'name': 'bs0', 'location': [40.05250229576194, 116.31528095199926], 'position': [-266, 148, 0], 'ssid': 'ssid-bs0', 'ip': '10.0.0.2/8', 'ip6': '2001:0:0:0:0:0:0:2/64', 'mac': '00:00:00:00:00:02', 'range': 500, 'failMode': 'standalone'})
net.addStation(**{'type': 'mp', 'name': 'mp0', 'location': ['40.0502701589399,116.3178515766592', '40.052962124089476,116.30926619652425'], 'position': '-48,-101,0', 'ip': '10.0.0.3/8', 'ip6': '2001:0:0:0:0:0:0:3/64', 'mac': '00:00:00:00:00:03', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 50, 'coord': ['-74,-91,0', '-38,-132,0', '-31,-125,0', '-72,-83,0', '-86,-84,0', '-485,-318,0', '-518,-257,0', '-597,-119,0', '-619,-81,0', '-667,4,0', '-687,37,0', '-701,62,0', '-765,179,0', '-767,183,0', '-771,190,0', '-776,199,0'], 'distance': 1192.2816881692042}, 'node': 'mp0'})
net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
net.configureWifiNodes()
net.addLink(**{'type': 'nl', 'node1': 'ec0', 'node2': 'bs0', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.OSM_Mobility_Setting(**{'mobility_start_time': 1, 'reverse': 0, 'ac_method': 'ssf', 'mob_rep': 1, 'mobility_mode': 'quickly'})
net.start()
thread_list = []
for td in thread_list: td.join()
net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230315010202817960.json')
net.stop()
