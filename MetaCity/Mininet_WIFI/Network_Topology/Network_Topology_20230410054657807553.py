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
from mininet.cli import CLI

# setLogLevel('info')
# net = OSM_Mininet_wifi(controller=Controller,autoAssociation=False)
#
#
# net.addStation(**{'type': 'mp', 'name': 'mp0', 'location': ['28.19417590019824,112.97851960816213', '28.193002986201193,112.9751937967296', '28.191867895884705,112.97231857910405'], 'position': '381,13,0', 'ip': '10.0.0.1/8', 'ip6': '2001:0:0:0:0:0:0:1/64', 'mac': '00:00:00:00:00:01', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
# net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 50, 'coord': ['368,18,0', '306,29,0', '233,41,0', '231,30,0', '215,-44,0', '212,-64,0', '217,-84,0', '214,-99,0', '164,-93,0', '164,-96,0', '54,-73,0', '40,-70,0', '-58,-54,0', '-140,-32,0', '-189,-22,0', '-193,-40,0', '-217,-125,0', '-203,-131,0', '-206,-161,0', '-211,-193,0', '-235,-208,0', '-240,-223,0', '-245,-242,0'], 'distance': 942.3399371249718}, 'node': 'mp0'})
# net.addStation(**{'type': 'mp', 'name': 'mp1', 'location': ['28.197108128878206,112.97564439053659', '28.19650277212775,112.97092388398723'], 'position': '99,339,0', 'ip': '10.0.0.2/8', 'ip6': '2001:0:0:0:0:0:0:2/64', 'mac': '00:00:00:00:00:02', 'range': 500, 'speed': 50, 'dimage': 'ubuntu:test2', 'sysctls': {'net.ipv6.conf.all.disable_ipv6': '0'}},cls=OSMDockerStaion)
# net.OSM_Mobility_For_ConfigurationData(**{'NodeMobilityConfig': {'speed': 50, 'coord': ['86,325,0', '72,325,0', '-18,327,0', '-111,324,0', '-162,322,0', '-227,321,0', '-257,316,0', '-314,299,0', '-348,300,0', '-348,293,0'], 'distance': 445.3186996930291}, 'node': 'mp1'})
# net.startController(**{'controller': 'None', 'name': 'c', 'number': 1, 'ip': '127.0.0.1', 'port': 6653, 'protocol': 'tcp', 'app': 'simple_switch'})
# net.configureWifiNodes()
# net.OSM_Mobility_Setting(**{'mobility_start_time': 1, 'reverse': 0, 'ac_method': 'ssf', 'mob_rep': 1, 'mobility_mode': 'quickly'})
# net.start()
# thread_list = []
# for td in thread_list: td.join()
# net.OSM_Experiment_Ended(data_storage_Directory='/home/kylin/Desktop/PythonProject/OSM_Mininet_WIFI/Mininet_WIFI/Network_Topology/Network_Topology_20230410054657807553.json')
# net.stop()
import threading
print(type(threading.current_thread()))
from os import environ
print(environ)
(host, screen) = environ['DISPLAY'].split(":")
print((host, screen))
if not host:
    print(1)
