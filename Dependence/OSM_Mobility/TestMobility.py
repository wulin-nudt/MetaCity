from mininet.node import Controller
from OSM_Mobility.OSM_Mininet_wifi import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from OSM_Roads import *

def topology():
    osm=OSMMapObject(OSMXMLIterObjectFactory(r'/home/kylin/Desktop/PythonProject/pythonProject/mapelements/osmfile/map1.osm'))
    r=Roads(osm)
    net = OSM_Mininet_wifi(controller=Controller, accessPoint=OVSKernelAP)

    info("*** Creating nodes \n")

    # h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range='20')
    # sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', range='20',position='25,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='30,50,0', range='30')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='1', position='90,50,0', range='30')
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='1', position='130,50,0', range='30')
    c1 = net.addController('c1', controller=Controller)

    info("*** Configuring wifi nodes \n")
    net.configureWifiNodes()

    info("*** Associatiing and Creating links \n")
    # net.addLink(ap1, h1)
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)
    sta1.coord = list(r.get_HigwayPointlists().values())[-1][1]
    # sta1.movingtime=[2,6]
    net.plotGraph(max_x=160, max_y=160)
    net.startMobility(time=0,mob_rep=110,ac_method='ssf')
    # print(list(r.get_HigwayPointlist().values())[0])
    net.mobility(sta1, 'start', time=4)
    net.mobility(sta1, 'stop', time=10)
    net.stopMobility(time=11)
    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    info("*** Running CLI \n")
    CLI(net)

    info("*** Stopping network \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()