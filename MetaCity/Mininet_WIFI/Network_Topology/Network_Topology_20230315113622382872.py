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


net.addAccessPoint(**{'type': 'bs', 'name': 'bs0', 'location': [40.05193275858459, 116.31430224616513], 'position': [-193, 377, 0], 'ssid': 'ssid-bs0', 'ip': '10.0.0.1/8', 'ip6': '2001:0:0:0:0:0:0:1/64', 'mac': '00:00:00:00:00:01', 'range': 500, 'failMode': 'standalone'})
net.addDocker(**{'type': 'ec', 'name': 'ec0', 'location': [40.05341147233673, 116.31589005291353], 'position': [-58, 542, 0], 'ip': '10.0.0.2/8', 'ip6': '2001:0:0:0:0:0:0:2/64', 'mac': '00:00:00:00:00:02', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addStation(**{'type': 'mp', 'name': 'mp0', 'location': ['40.050355428553644,116.31747785966196', '40.05278713044356,116.30919551635259'], 'position': '77,202,0', 'ip': '10.0.0.3/8', 'ip6': '2001:0:0:0:0:0:0:3/64', 'mac': '00:00:00:00:00:03', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 50, 'coord': ['75,201,0', '83,202,0', '119,161,0', '126,168,0', '84,210,0', '70,209,0', '-328,-25,0', '-361,36,0', '-441,174,0', '-462,212,0', '-510,297,0', '-530,330,0', '-544,355,0', '-608,472,0', '-610,476,0', '-614,483,0', '-619,492,0', '-629,487,0', '-623,478,0'], 'distance': 1221.8110524063234}, 'node': 'mp0'})
net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
net.configureWifiNodes()
net.addLink(**{'type': 'nl', 'node1': 'bs0', 'node2': 'ec0', 'delay': '0ms', 'bw': 10, 'jitter': '0ms', 'loss': 0})
net.OSM_Mobility_Setting(**{'mobility_start_time': 1, 'reverse': 1, 'ac_method': 'ssf', 'mob_rep': 1, 'mobility_mode': 'quickly'})
net.start()
thread_list = []
t=NetworkDelayMonitor('mp0', 'ec0', net, monitor_type= {'delay'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230315113622382872.json',**{'period': 10}).thread_
thread_list.append(t)
for td in thread_list: td.join()
net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230315113622382872.json')
net.stop()
