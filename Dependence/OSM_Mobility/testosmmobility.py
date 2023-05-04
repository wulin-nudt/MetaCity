from mininet.node import Controller
from OSM_Mobility.OSM_Mininet_wifi import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from OSM_Roads import *

setLogLevel('info')
net = OSM_Mininet_wifi(controller=Controller, accessPoint=OVSKernelAP)
sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range='20')
sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', range='20',position='40,50,0')
sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8', range='20',position='60,50,0')
ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='30,50,0', range='30')
ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='1', position='90,50,0', range='30')
ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='1', position='130,50,0', range='30')
c1 = net.addController('c1', controller=Controller)
net.addLink(ap1, ap2)
net.addLink(ap2, ap3)
net.plotGraph(max_x=160, max_y=160)
# mobnode_cofig={sta1:{'coord':['67,25,0', '75,22,0', '83,21,0'],'movingtime':[2,2],'node_start_time':0,'node_stop_time':4},
#                sta2:{'coord':['75,22,0', '83,21,0', '93,23,0'],'movingtime':[2,3],'node_start_time':0,'node_stop_time':5},
#                sta3:{'coord':['102,27,0', '110,34,0', '115,43,0'],'movingtime':[2,4],'node_start_time':0,'node_stop_time':6}}
net.configureWifiNodes()

# net.OSM_MobilityMapInit(r'/home/kylin/Desktop/PythonProject/pythonProject/mapelements/osmfile/map1.osm')
# net.OSM_Mobility_For_Higway(sta1,'173299334',speed=60,positive_direction=False)
# print(sta1.coord)
# net.OSM_Mobility_Setting(mobility_start_time=0,mob_rep=111,reverse=True)

# net.get_Roads()
net.build()
c1.start()
ap1.start([c1])
ap2.start([c1])
ap3.start([c1])
CLI(net)
net.stop()