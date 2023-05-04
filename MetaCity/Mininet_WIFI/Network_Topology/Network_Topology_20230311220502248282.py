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


net.addStation(**{'type': 'mp', 'name': 'mp0', 'location': ['28.19447524943341,112.9771220671689', '28.198046870281217,112.97198996395964'], 'position': '441,-617,0', 'ip': '10.0.0.1/8', 'ip6': '2001:0:0:0:0:0:0:1/64', 'mac': '00:00:00:00:00:01', 'range': 500, 'speed': 10, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 10, 'coord': ['442,-610,0', '492,-484,0', '500,-443,0', '514,-385,0', '453,-366,0', '375,-354,0', '283,-339,0', '269,-338,0', '178,-336,0', '86,-339,0', '88,-304,0', '94,-184,0', '94,-183,0', '84,-184,0', '60,-184,0', '41,-183,0', '-56,-180,0'], 'distance': 976.1293994536938}, 'node': 'mp0'})
net.addStation(**{'type': 'mp', 'name': 'mp1', 'location': ['28.201366783571256,112.96824574399207', '28.198304766080653,112.97807694717699'], 'position': '-429,149,0', 'ip': '10.0.0.2/8', 'ip6': '2001:0:0:0:0:0:0:2/64', 'mac': '00:00:00:00:00:02', 'range': 500, 'speed': 12, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 12, 'coord': ['-436,150,0', '-380,146,0', '-376,120,0', '-300,122,0', '-299,136,0', '-264,136,0', '-194,136,0', '-192,103,0', '-190,56,0', '-186,-1,0', '-183,-91,0', '-182,-117,0', '-181,-157,0', '-169,-158,0', '-153,-159,0', '-60,-162,0', '94,-169,0', '120,-171,0', '272,-177,0', '286,-178,0', '393,-181,0', '536,-188,0'], 'distance': 1288.5081566563074}, 'node': 'mp1'})
net.addAccessPoint(**{'type': 'bs', 'name': 'bs0', 'location': [28.19816983187203, 112.97034851509135], 'position': [-223, -206, 0], 'ssid': 'ssid-bs0', 'ip': '10.0.0.3/8', 'ip6': '2001:0:0:0:0:0:0:3/64', 'mac': '00:00:00:00:00:03', 'range': 500, 'failMode': 'standalone'})
net.addAccessPoint(**{'type': 'bs', 'name': 'bs1', 'location': [28.197621232912816, 112.97896343954396], 'position': [621, -267, 0], 'ssid': 'ssid-bs1', 'ip': '10.0.0.4/8', 'ip6': '2001:0:0:0:0:0:0:4/64', 'mac': '00:00:00:00:00:04', 'range': 500, 'failMode': 'standalone'})
net.addDocker(**{'type': 'ec', 'name': 'ec0', 'location': [28.199421213400182, 112.97024489026016], 'position': [-233, -67, 0], 'ip': '10.0.0.5/8', 'ip6': '2001:0:0:0:0:0:0:5/64', 'mac': '00:00:00:00:00:05', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addDocker(**{'type': 'ec', 'name': 'ec1', 'location': [28.197207841798146, 112.97769071072716], 'position': [496, -313, 0], 'ip': '10.0.0.6/8', 'ip6': '2001:0:0:0:0:0:0:6/64', 'mac': '00:00:00:00:00:06', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.addAccessPoint(**{'type': 'ap', 'name': 'ap2', 'location': [28.204318197480337, 112.97739025881245], 'position': [467, 477, 0], 'ssid': 'ssid-ap2', 'ip': '10.0.0.7/8', 'ip6': '2001:0:0:0:0:0:0:7/64', 'mac': '00:00:00:00:00:07', 'range': 10, 'failMode': 'standalone'})
net.addDocker(**{'type': 'ec', 'name': 'ec2', 'location': [28.204526274030545, 112.97608137295573], 'position': [339, 500, 0], 'ip': '10.0.0.8/8', 'ip6': '2001:0:0:0:0:0:0:8/64', 'mac': '00:00:00:00:00:08', 'range': 500, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerCloud)
net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
net.configureWifiNodes()
net.addLink(**{'type': 'nl', 'node1': 'ap2', 'node2': 'ec2', 'delay': '5ms', 'bw': 10, 'jitter': '1ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'ap2', 'node2': 'bs1', 'delay': '40ms', 'bw': 20, 'jitter': '5ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'ap2', 'node2': 'bs0', 'delay': '80ms', 'bw': 10, 'jitter': '10ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'bs1', 'node2': 'ec1', 'delay': '10ms', 'bw': 10, 'jitter': '1ms', 'loss': 0})
net.addLink(**{'type': 'nl', 'node1': 'bs0', 'node2': 'ec0', 'delay': '20ms', 'bw': 10, 'jitter': '5ms', 'loss': 0})
net.OSM_Mobility_Setting(**{'mobility_start_time': 1, 'reverse': 1, 'ac_method': 'ssf', 'mob_rep': 1, 'mobility_mode': 'quickly'})
net.start()
thread_list = []
t=NetworkDelayMonitor('mp0', 'ec2', net, monitor_type= {'delay', 'packet_loss'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230311220502248282.json',**{'period': 100}).thread_
thread_list.append(t)
t=NetworkBandWidthMonitor('mp0', 'ec2', net, monitor_type= {'band_width'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230311220502248282.json',**{'period': 100}).thread_
thread_list.append(t)
t=NetworkDelayMonitor('mp1', 'ec2', net, monitor_type= {'delay', 'packet_loss'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230311220502248282.json',**{'period': 100}).thread_
thread_list.append(t)
t=NetworkBandWidthMonitor('mp1', 'ec2', net, monitor_type= {'band_width'}).start(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230311220502248282.json',**{'period': 100}).thread_
thread_list.append(t)
for td in thread_list: td.join()
net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230311220502248282.json')
net.stop()
