from Monitor.NetworkMonitor import NetworkDelayMonitor,NetworkMonitor,MonitorType
from containernet.node import DockerSta
from OSM_Mininet_wifi.node import OSMDockerStaion
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel
from mininet.node import Controller
from OSM_Mininet_wifi.net import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP

setLogLevel('info')
net = OSM_Mininet_wifi(controller=Controller,autoAssociation=False)
sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range='20',position='70,50,0',cls=OSMDockerStaion, dimage="ubuntu:test2",sysctls={'net.ipv6.conf.all.disable_ipv6':'0'})
sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', range='20',position='80,50,0',cls=OSMDockerStaion, dimage="ubuntu:test2",sysctls={'net.ipv6.conf.all.disable_ipv6':'0'})
sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8', range='20',position='60,50,0',cls=DockerSta, dimage="ubuntu:test2",sysctls={'net.ipv6.conf.all.disable_ipv6':'0'})
ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g',ip='10.0.0.9/8', channel='1',position='60,50,0', range='30')
ap2 = net.addAccessPoint('ap2',ssid='ssid-ap2', mode='g', channel='1', position='90,50,0', range='100')
ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='1', position='130,50,0', range='30')
c1 = net.addController('c1', controller=Controller)
net.configureWifiNodes()


net.addLink(ap2, sta1)
net.addLink(sta2, ap2)
net.addLink(ap1, ap2)
net.addLink(ap2, ap3)
# net.plotGraph(max_x=160, max_y=160)
# mobnode_cofig={sta1:{'coord':['67,25,0', '75,22,0', '83,21,0'],'movingtime':[2,2],'node_start_time':0,'node_stop_time':4},
#                sta2:{'coord':['75,22,0', '83,21,0', '93,23,0'],'movingtime':[2,3],'node_start_time':0,'node_stop_time':5},
#                sta3:{'coord':['102,27,0', '110,34,0', '115,43,0'],'movingtime':[2,4],'node_start_time':0,'node_stop_time':6}}
# net.OSM_MobilityMapInit(r'/home/kylin/Desktop/PythonProject/pythonProject/mapelements/osmfile/map1.osm')
# net.OSM_Mobility_For_Higway(sta1,'173299334',speed=60,positive_direction=False)
# net.OSM_Mobility_Setting(mobility_start_time=0,mob_rep=11,reverse=True)
# net.build()
# c=sta1.cmd("echo $PS1")
# print(c.encode())
net.start()
# stat_nodes,mob_nodes=net.get_mob_stat_nodes()

# mt=NetworkDelayMonitor(sta1,sta2)
# mt.plotGraph()
# mt.extend_monitor_type(MonitorType.Packet_Loss)
# mt.start(period=20)

CLI(net)
net.stop()
