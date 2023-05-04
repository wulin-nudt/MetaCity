from containernet.net import Containernet
from OSM_Mobility.OSM_CustomMobility import CustomMobility,OSMConfigMobility,OSMConfigMobilityForHigway
from mapelements.OSMMapObject import OSMMapObject
from mapelements.OSMObjectFactory import OSMXMLIterObjectFactory
from OSM_Mobility.OSM_Roads import Roads
from mininet.log import info
# test
import socket
import re
from threading import Thread as thread
from time import sleep
from itertools import chain, groupby
from six import string_types

from mininet.cli import CLI
from mininet.term import makeTerms
from mininet.net import Mininet
from mininet.node import Node, Controller
from mininet.util import (macColonHex, ipStr, ipParse, ipAdd,
                          waitListening, BaseString)
from mininet.link import Link, TCLink, TCULink
from mininet.nodelib import NAT
from mininet.log import info, error, debug, output, warn

from mn_wifi.node import AP, Station, Car, \
    OVSKernelAP, physicalAP
from mn_wifi.wmediumdConnector import error_prob, snr, interference
from mn_wifi.link import IntfWireless, wmediumd, _4address, HostapdConfig, \
    WirelessLink, TCLinkWireless, ITSLink, WifiDirectLink, adhoc, mesh, \
    master, managed, physicalMesh, PhysicalWifiDirectLink, _4addrClient, \
    _4addrAP, phyAP
from mn_wifi.clean import Cleanup as CleanupWifi
from mn_wifi.energy import Energy
from mn_wifi.telemetry import parseData, telemetry as run_telemetry
from mn_wifi.mobility import Tracked as TrackedMob, model as MobModel, \
    Mobility as mob, ConfigMobility, ConfigMobLinks
from mn_wifi.plot import Plot2D, Plot3D, PlotGraph
from mn_wifi.module import Mac80211Hwsim
from mn_wifi.propagationModels import PropagationModel as ppm
from mn_wifi.vanet import vanet
from mn_wifi.sixLoWPAN.net import Mininet_IoT
from mn_wifi.sixLoWPAN.node import OVSSensor, LowPANNode
from mn_wifi.sixLoWPAN.link import LowPANLink
from mn_wifi.sixLoWPAN.util import ipAdd6
from mn_wifi.wwan.net import Mininet_WWAN
from mn_wifi.wwan.node import WWANNode
from mn_wifi.wwan.link import WWANLink

VERSION = "1.0"
class OSM_Mininet_wifi(Containernet):
    def check_if_mob(self):
        if self.mob_model or self.mob_stop_time or self.roads:
            mob_params = self.get_mobility_params()
            stat_nodes, mob_nodes = self.get_mob_stat_nodes()
            method = CustomMobility
            if self.mob_model or self.cars or self.roads:
                method = self.start_mobility
            method(stat_nodes=stat_nodes, mob_nodes=mob_nodes, **mob_params)
            self.mob_check = True
        else:
            if self.draw and not self.isReplaying:
                self.check_dimension(self.get_mn_wifi_nodes())

    def OSM_Mobility_For_Higway(self, *args, **kwargs):
        "Configure mobility parameters"
        if not OSMConfigMobilityForHigway.Roads and not OSMConfigMobility.OSM_MAP:
            raise Exception('OSM_Mobility_For_Higway Config fail')
        if not OSMConfigMobilityForHigway.Roads:
            OSMConfigMobilityForHigway.Roads=Roads(OSMConfigMobility.OSM_MAP)
            OSMConfigMobilityForHigway(*args, **kwargs)
        else:
            OSMConfigMobilityForHigway(*args, **kwargs)

    def OSM_Mobility_Setting(self,mobility_start_time=0,mobility_stop_time=None,mob_rep=1,reverse=False,ac_method='ssf',*args,**kwargs):
        self.startMobility(time=mobility_start_time, mob_rep=mob_rep,reverse=reverse,ac_method=ac_method)
        stat_nodes, mob_nodes = self.get_mob_stat_nodes()
        if mob_nodes:
            node_endtimes=[n.endTime for n in mob_nodes]
            mobility_stop_time= mobility_stop_time if mobility_stop_time is not None else 3*max(node_endtimes)+mobility_start_time
            self.stopMobility(time=mobility_stop_time)
        else: raise Exception('mob_nodes not exist')

        # if not isinstance(mobnode_cofig,dict):
        #     raise Exception('the type of mobnode_cofig object is incorrect,mobnode_cofig must be a dict object')
        # for key,value in mobnode_cofig.items():
        #     coord=value.get('coord',[])
        #     if coord:key.coord=coord
        #     movingtime = value.get('movingtime', [])
        #     if coord and movingtime:key.movingtime=movingtime
        #     self.mobility(key, 'start', time=value.get('node_start_time',mobility_start_time))
        #     endtime=value.get('node_stop_time',None)
        #     if endtime is not None: self.mobility(key, 'stop', time=endtime)
        #     elif endtime is None and movingtime:
        #         endtime=sum(movingtime)+key.startTime
        #         self.mobility(key, 'stop', time=endtime)
        #     elif endtime is None and mobility_stop_time is not None :
        #         endtime=mobility_stop_time
        #         self.mobility(key, 'stop', time=endtime)
        #     else: raise Exception('{}: node_stop_time is None and (movingtime is None or mobility_stop_time is None), incorrect setting'.format(key.name))
        #     node_endtimes.append(endtime)

    def MobilityAutoInit(self,mobnode_cofig={},mobility_start_time=0,mobility_stop_time=None,mob_rep=1,reverse=False,ac_method='ssf',*args,**kwargs):
        self.startMobility(time=mobility_start_time, mob_rep=mob_rep,reverse=reverse,ac_method=ac_method)
        node_endtimes=[]
        if not isinstance(mobnode_cofig,dict):
            raise Exception('the type of mobnode_cofig object is incorrect,mobnode_cofig must be a dict object')
        for key,value in mobnode_cofig.items():
            coord=value.get('coord',[])
            if coord:key.coord=coord
            movingtime = value.get('movingtime', [])
            if coord and movingtime:key.movingtime=movingtime
            self.mobility(key, 'start', time=value.get('node_start_time',mobility_start_time))
            endtime=value.get('node_stop_time',None)
            if endtime is not None: self.mobility(key, 'stop', time=endtime)
            elif endtime is None and movingtime:
                endtime=sum(movingtime)+key.startTime
                self.mobility(key, 'stop', time=endtime)
            elif endtime is None and mobility_stop_time is not None :
                endtime=mobility_stop_time
                self.mobility(key, 'stop', time=endtime)
            else: raise Exception('{}: node_stop_time is None and (movingtime is None or mobility_stop_time is None), incorrect setting'.format(key.name))
            node_endtimes.append(endtime)

        mobility_stop_time= mobility_stop_time if mobility_stop_time is not None else max(node_endtimes)+1+mobility_start_time
        self.stopMobility(time=mobility_stop_time)

    def OSM_MobilityMapInit(self,OSM_File):
        OSMConfigMobility.OSM_MAP= OSMMapObject(OSMXMLIterObjectFactory(OSM_File))
        # self.OSM_MAP = OSMMapObject(OSMXMLIterObjectFactory(OSM_File))
        # self.Roads=Roads(self.OSM_MAP)

    # def get_OSM_Map(self):
    #     if hasattr(self, 'OSM_MAP'):
    #         return self.OSM_MAP
    #     else:
    #         return None
    #
    # def get_Roads(self):
    #     if hasattr(self, 'Roads'):
    #         return self.Roads
    #     else:
    #         return None
    #
    # def NodeMobility_For_Higway_config(self,node,higwayid,node_start_time=0,movingtime=[],node_stop_time=None,speed=None,total_move_time=None,positive_direction=True,*args,**kwargs):
    #     roads=self.get_Roads()
    #     if roads is None:
    #         raise Exception('The Roads object is None')
    #
    #     higway=roads.get_HigwayPointlistById(higwayid)
    #     if higway is None:
    #         raise Exception('The {} id of higway not exist'.format(higwayid))
    #
    #     if higway:
    #         coord=higway[1]
    #         if node_stop_time is None:
    #             if movingtime: node_stop_time=sum(movingtime)+node_start_time
    #             elif speed is not None and speed !=0 :
    #                 higwaylength=Roads.Compute_HigwayLength(higway)
    #                 node_stop_time=(higwaylength/speed)+node_start_time
    #             elif total_move_time is not None : node_stop_time=total_move_time+node_start_time
    #             else: raise Exception('The node_stop_time is uncertainty')
    #         return self.NodeMobilitySimpleConfig(node,coord,movingtime,node_start_time,node_stop_time,positive_direction)
    #     else:return None
    #
    #
    #
    # def NodeMobilitySimpleConfig(self,node,coord=[],movingtime=[],node_start_time=0,node_stop_time=None,positive_direction=True,*args,**kwargs):
    #     if not coord or node is None or node_stop_time is None:
    #         raise Exception('coord is None or node is None or node_stop_time is None')
    #     if positive_direction:
    #         return {node:{'coord':coord,'movingtime':movingtime,'node_start_time':node_start_time,'node_stop_time':node_stop_time}}
    #     else:
    #         coord.reverse()
    #         return {node: {'coord': coord, 'movingtime': movingtime, 'node_start_time': node_start_time,'node_stop_time': node_stop_time}}