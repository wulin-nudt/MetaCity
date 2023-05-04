import folium
import json
from OSM_Map.OSM_Marker import Moving_Point_Marker,\
    OSM_Popup,OSM_Icon,OSM_Tooltip,OSM_Signal_Range,Wireless_Access_Point_Marker,NetWorkLink
from OSM_Map.Moving_Point_Application.Moving_Point_Application import Moving_Point_Application
from OSM_Map.Wireless_Access_Point_Application.Wireless_Access_Point_Application import Wireless_Access_Point_Application,Base_Station_Application
from OSM_Map.NetWorkLink_Application.NetWorkLink_Application import NetWorkLink_Application
from OSM_Map.Edge_Cloud_Application.Edge_Cloud_Application import Edge_Cloud_Application
from OSM_Map.Menu_Application.Menu_Application import Menu_Application
from OSM_Map.OSM_Layui import OSM_Layui
from OSM_Map.OSM_Visualization import Vega,VegaEmbed
from OSM_Map.OSM_Folium_Element import Global_Network_Configuration_Layer,OSM_Map,OSM_Application

class EdgeComputingApplication(object):
    def __init__(self,title,location):
        self.map=OSM_Map(location=location, zoom_start=12,min_zoom=4, tiles='openstreetmap',width='85%',height='85%',left='1%',top='1%',display='inline-block')
        self.osm_application=OSM_Application(title=title).add_child(self.map)
        self.osmlayer=Global_Network_Configuration_Layer(name='gncl').add_to(self.map)
        OSM_Layui().add_to(self.osm_application)
        # Vega().add_to(self.osm_application)
        VegaEmbed().add_to(self.osm_application)
        folium.LatLngPopup().add_to(self.map)
        self.__init_Application()

    def __init_Application(self):

        mp = Moving_Point_Application(name='mp', popup=None, tooltip=None,
                                      icon=OSM_Icon(color='red',icon='location-arrow', prefix='fa'),
                                      active=False,configuration={'speed':50}).add_to(self.osmlayer)
        mp.build()

        mp3 = Edge_Cloud_Application(name='ec', popup=None, tooltip=None,
                                     icon=OSM_Icon(color='red', icon='cloud',prefix='fa'),
                                     active=False).add_to(self.osmlayer)
        mp3.build()

        mp1 = Wireless_Access_Point_Application(name='ap', popup=None, tooltip=None,
                                                icon=OSM_Icon(color='red', icon='router', prefix='custom'),
                                                active=False, signal_range=OSM_Signal_Range(radius=500,tooltip=OSM_Tooltip(
                                                                        'test'))).add_to(self.osmlayer)
        mp1.build()

        mp4 = Base_Station_Application(name='bs', popup=None, tooltip=None,
                                                icon=OSM_Icon(color='red', icon='broadcast-tower', prefix='fa'),
                                                active=False, signal_range=OSM_Signal_Range(radius=500,tooltip=OSM_Tooltip(
                                                                        'test'))).add_to(self.osmlayer)
        mp4.build()

        mp2 = NetWorkLink_Application(switching_nodes=[mp1,mp4],name='nl', active=False, tooltip=None, popup=None).add_to(self.osmlayer)
        mp2.build()

        entity = {'Global_Network_Configuration_Layer': self.osmlayer, 'Moving_Point': mp, 'Wireless_Access_Point': mp1,
                  'Edge_Cloud': mp3, 'NetWorkLink': mp2,'Base_Station':mp4}

        Moving_Point_Configuration={mp.type+"_range":500,mp.type+"_dimage":'ubuntu:test2',mp.type+"_sysctls":'{"net.ipv6.conf.all.disable_ipv6":"0"}',mp.type+"_emulation":10}
        Edge_Cloud_Configuration = {mp3.type + "_range": 500, mp3.type + "_dimage": 'ubuntu:test2',mp3.type + "_sysctls": '{"net.ipv6.conf.all.disable_ipv6":"0"}'}
        Wireless_Access_Point_Configuration = {mp1.type + "_range": 500,mp1.type + "_failMode": 'standalone'}
        Base_Station_Configuration = {mp4.type + "_range": 500,mp4.type + "_failMode": 'standalone'}
        NetWorkLink_Configuration = {'bw': 10,'delay':'0ms','jitter':'0ms','loss':0}

        Experiment_Configuration={'mobility_start_time':1,'reverse':False,'mob_rep':1,'mobility_stop_time':'','AUTO_mobility_stop_time':'','Auto_Configuration_mobility_stop_time':True,
                                                           'mobility_mode':'quickly','ac_method':'ssf'}
        SDNController_Configuration={'SDN_Controller':'None','Controller_Name':'c','Controller_Number':1,
                                     'Controller_IP':'127.0.0.1','Controller_Port':6653,'Controller_Protocol':'tcp','Network_Application':'simple_switch'}

        Emulation_Configuration={'EmulationConfiguration':{}}
        Emulation_Configuration['EmulationConfiguration'].update(Experiment_Configuration)
        Emulation_Configuration['EmulationConfiguration'].update(SDNController_Configuration)

        configuration={}
        configuration.update(Moving_Point_Configuration)
        configuration.update(Base_Station_Configuration)
        configuration.update(Edge_Cloud_Configuration)
        configuration.update(Wireless_Access_Point_Configuration)
        configuration.update(NetWorkLink_Configuration)
        configuration.update(Emulation_Configuration)


        self.osmlayer.setConfiguration(configuration=configuration)

        menu = Menu_Application(self.map, self.osmlayer, entity).add_to(self.osm_application)
        menu.build()

    def output(self,name):
        self.map.save(name)