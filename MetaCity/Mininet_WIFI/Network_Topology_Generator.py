import copy

from containernet.node import DockerSta
from OSM_Mininet_wifi.node import OSMDockerStaion
from containernet.cli import CLI
from containernet.term import makeTerm
from mininet.log import info, setLogLevel
from mininet.node import Controller
from OSM_Mininet_wifi.net import OSM_Mininet_wifi
from mn_wifi.net import OVSKernelAP
import osmnx as ox
import datetime
import shutil
import os
import folium
import json

class Network_Topology_Generator:

    def __init__(self,path=None,template=r'Network_Topology_Template.py'):
        if not path:
            self.path = os.path.split(os.path.realpath(__file__))[0]+'/'
        else:
            self.path=path
        self.template=template

    def generate(self,network_topology=None):
        datas={'network_topology':[]}
        if network_topology:
            date=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename= r'Network_Topology_'+date+".py"
            jsonname=r'Network_Topology_'+date+".json"
            datas['network_topology'].append({'filename':filename,'date':date})
            newName=self.path+r'Network_Topology/'+filename
            jsonfile=self.path+r'Network_Topology/'+jsonname
            shutil.copy(self.path+self.template,newName)
            print(network_topology)
            with open(newName, 'a') as f:
                EmulationConfig = []
                isExistMobility=False
                MobilityConfig= {}
                SDNControllerConfig = {}
                for k, v in network_topology.items():
                    if v['type'] in ['mp', 'ec']:
                        kwargs = {}
                        NodeMobilityConfig ={}
                        for k1,v1 in v.items():
                            if k1 in ['NodeMobilityConfig'] and v['type'] in ['mp'] and v1.get('coord',None):
                                NodeMobilityConfig={k1:v1}
                            elif k1 in ['EmulationConfig']:
                                emuconfig={k:{'localconfig':{},'globalconfig':{}}}
                                for k2,v2 in v1.get("localconfig",{}).items():
                                    ec=v2.split(",")
                                    emuconfig[k]['localconfig'].update({k2:ec})
                                emuconfig[k]['globalconfig'].update(v1.get("globalconfig",{}))
                                EmulationConfig.append(emuconfig)
                                    # for e in ec:
                                    #     EmulationConfig.append({k2:[k,e]})
                            else:
                                kwargs.update({k1:v1})
                        if v['type'] in ['mp']:
                            f.write("net.addStation(**%s,cls=OSMDockerStaion)\n"%(kwargs))
                            if NodeMobilityConfig:
                                NodeMobilityConfig.update({'node':k})
                                f.write("net.OSM_Mobility_For_ConfigurationData(**%s)\n"%(NodeMobilityConfig))
                                isExistMobility=True
                        if v['type'] in ['ec']:
                            f.write("net.addDocker(**%s,cls=OSMDockerCloud)\n" % (kwargs))
                    elif v['type'] in ['ap','bs']:
                        kwargs = {}
                        for k1, v1 in v.items():
                            kwargs.update({k1:v1})
                        f.write("net.addAccessPoint(**%s)\n"%(kwargs))

                    elif v['type'] in ['gncl']:
                        for k1, v1 in v.items():
                            if k1 in ['MobilityConfig']:
                                MobilityConfig.update(v1)
                            elif k1 in ['SDNControllerConfig']:
                                SDNControllerConfig.update(v1)

                f.write("net.startController(**%s)\n" % (SDNControllerConfig))

                # f.write("net.addController('c1', controller=Controller)\n")

                f.write("net.configureWifiNodes()\n")

                for k, v in network_topology.items():
                    if v['type'] in ['nl']:
                        kwargs ={}
                        for k1,v1 in v.items():
                            kwargs.update({k1:v1})
                        f.write("net.addLink(**%s)\n"%(kwargs))


                if isExistMobility:
                    f.write("net.OSM_Mobility_Setting(**%s)\n"%(MobilityConfig))

                f.write("net.start()\n")

                f.write("thread_list = []\n")

                if MobilityConfig.get('mobility_mode',None):
                    if MobilityConfig.get('mobility_mode',None) in ['completely']:
                        f.write("thread_list.append(Mobility.thread_)\n")
                        f.write("output('enable mobility complete mode\\n')\n")
                        f.write("output('start mobility\\n')\n")

                emu_tasks = []
                for emu in EmulationConfig:
                    for k,v in emu.items():
                        emu_tasks.extend(self.single_Node_EmulationConfig(node=k,localconfig=v.get("localconfig",{}),globalconfig=v.get("globalconfig",{})))
                print(emu_tasks)
                # EmulationConfig=self.emulationConfig(configs=EmulationConfig)
                for et in emu_tasks:
                    monitor={'NetworkDelayMonitor':['delay','packet_loss'],'NetworkBandWidthMonitor':['band_width']}
                    if et.get('monitor_type',None):
                        monitor_type=set(et.get('monitor_type'))
                        for k ,v in monitor.items():
                            monitor_union=monitor_type & set(v)
                            if monitor_union:
                                f.write("t=%s('%s', '%s', net, monitor_type= %s).start(data_storage_Directory='%s',**%s).thread_\n"%(k,et['client'],et['server'],monitor_union,jsonfile,et['config']))
                                f.write("thread_list.append(t)\n")
                            monitor_type=monitor_type-monitor_union


                f.write("for td in thread_list: td.join()\n")

                # f.write("CLI(net)\n")
                if MobilityConfig.get('mobility_mode',None):
                    if MobilityConfig.get('mobility_mode',None) in ['completely']:
                        f.write("output('enable mobility complete mode\\n')\n")
                        f.write("output('end mobility\\n')\n")

                f.write("net.OSM_Experiment_Ended(data_storage_Directory='%s')\n"%(jsonfile))
                f.write("net.stop()\n")
                return datas

    def single_Node_EmulationConfig(self,node,localconfig={},globalconfig={}):
        # configs=copy.deepcopy(configs)
        base_config={}
        for k,v in globalconfig.items():
            if v.get("key",None):
                base_config.update({v.get("key",None).replace("\"",""):v.get("value",None)})
        emulation_config=[]
        for t, value in localconfig.items():
            for v in value:
                optimize = False
                for temp in emulation_config:
                    if temp.get("monitor_type", None):
                        if t not in temp.get("monitor_type", None) and v == temp.get("server", None):
                            temp.get("monitor_type", None).append(t)
                            optimize = True
                            break
                if not optimize:
                    emulation_config.append({"monitor_type": [t], "client": node, "server": v,'config':base_config})

        return emulation_config



    # def routes(self,osm_map,points=[]):
    #     routes=[]
    #     if points and len(points)>1:
    #         G=None
    #         points=[tuple(map(float, p.split(',')))[::-1] for p in points]
    #         polygon_points=None
    #         if len(points)<3:
    #             polygon_points = [p for p in points]
    #             mid=(0.01+(polygon_points[0][0]+polygon_points[1][0])/2,0.01+(polygon_points[0][1]+polygon_points[1][1])/2)
    #             polygon_points.append(mid)
    #         poly = Polygon(polygon_points if polygon_points else points)
    #         file,polygon1=self.osm_downloader.OSM_File_Find_From_CacheIndex(poly.bounds)
    #         if file:
    #             G=self.osm_downloader.json_to_gdf(polygon1,simplify=False,json_filepaths=file)
    #         else:
    #             polygon2=box(poly.bounds[0]-0.1,poly.bounds[1]-0.1,poly.bounds[2]+0.1,poly.bounds[3]+0.1)
    #             file=self.osm_downloader.Download_By_Polygon(polygon2)
    #             file=[str(f.expanduser()) for f in file]
    #             G=self.osm_downloader.json_to_gdf(polygon2,simplify=False,json_filepaths=file)
    #
    #         # center=tuple(map(float,points[0].split(',')))
    #         # G = ox.graph_from_point(center,dist=6000)
    #         #m=osm_map
    #         for i in range(len(points)-1):
    #             # origin=tuple(map(float,points[i].split(',')))
    #             origin=ox.nearest_nodes(G, points[i][0], points[i][1])
    #             # destination=tuple(map(float,points[i+1].split(',')))
    #             destination=ox.nearest_nodes(G, points[i+1][0], points[i+1][1])
    #             rou = ox.shortest_path(G, origin, destination)
    #             routes.append(self.route_for_folium(G, rou))
    #             #m = ox.plot_route_folium(G, rou, route_map=m, weight=2, color="#8b0000")
    #         #m.save("111.html")
    #     # ox.plot_graph_folium(G, tiles='openstreetmap', kwargs={'width': 0.1}).save('456123.html')
    #     return routes
    #
    #
    # def route_for_folium(
    #         self,
    #         G,
    #         route,
    #         popup_attribute=None,
    #         **kwargs,
    # ):
    #     node_pairs = zip(route[:-1], route[1:])
    #     uvk = ((u, v, min(G[u][v], key=lambda k: G[u][v][k]["length"])) for u, v in node_pairs)
    #     gdf_edges = ox.graph_to_gdfs(G.subgraph(route), nodes=False).loc[uvk]
    #     return self.get_route_edage(gdf_edges,popup_attribute,**kwargs)
    #
    # def get_route_edage(self,gdf, popup_attribute, **kwargs):
    #
    #     locations=[]
    #
    #     # identify the geometry and popup columns
    #     if popup_attribute is None:
    #         attrs = ["geometry"]
    #     else:
    #         attrs = ["geometry", popup_attribute]
    #
    #     for vals in gdf[attrs].values:
    #         params = dict(zip(["geom", "popup_val"], vals))
    #         if params["geom"]:
    #             location = [[lat, lng] for lng, lat in params["geom"].coords]
    #             locations.append(location)
    #
    #     return locations


# n=Network_Topology_Generator()
# k1={"1":2}
# for k,v in k1.items():
#     print ("%s=\'%s\'" % (k, v))
# print(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))