from mn_wifi.mobility import Tracked,Mobility
import numpy as np
from numpy.random import rand
from mininet.log import debug
from time import sleep, time
from mn_wifi.plot import PlotGraph
from mininet.log import info, error, debug, output, warn
from mapelements.OSMMapObject import OSMMapObject
from mapelements.OSMObjectFactory import OSMXMLIterObjectFactory
from OSM_Mobility.OSM_Roads import Roads
from mn_wifi.associationControl import AssociationControl as AssCtrl

class CustomMobility(Tracked):
    def get_points(self, node, a0, a1, total,movingtime=None):
        x1, y1, z1 = float(a0[0]), float(a0[1]), float(a0[2])
        x2, y2, z2 = float(a1[0]), float(a1[1]), float(a1[2])
        points = []
        perc_dif = []
        ldelta = [0, 0, 0]
        faxes = [x1, y1, z1]  # first reference point
        laxes = [x2, y2, z2]  # last refence point
        dif = [abs(x2-x1), abs(y2-y1), abs(z2-z1)]   # difference first and last axes
        for i in range(len(dif)):
            if dif[i] == 0:
                perc_dif.append(0)
            else:
                # we get the difference among axes to calculate the speed
                perc_dif.append((dif[i] * 100) / total[i])

        dmin = min([x for x in perc_dif if x != 0] if faxes!=laxes else [0.000001])
        t = self.mob_time(node) * 1000  # node simulation time
        dt = t * (dmin / 100) if not movingtime else movingtime*1000

        for i in range(len(perc_dif)):
            if perc_dif[i] != 0:
                ldelta[i] = dif[i] / dt

        # direction of the node
        dir = (self.dir(x1, x2), self.dir(y1, y2), self.dir(z1, z2))

        for n in np.arange(0, dt, 1):
            for i in range(len(ldelta)):
                if dir[i]:
                    if n < dt - 1:
                        faxes[i] += ldelta[i]
                    else:
                        faxes[i] = laxes[i]
                else:
                    if n < dt - 1:
                        faxes[i] -= ldelta[i]
                    else:
                        faxes[i] = laxes[i]
            points.append(self.get_position(faxes))
        return points
    def set_coordinates(self, node):
        coord = self.create_coord(node)
        movingtime=self.get_movingtimes(node,len(coord))
        total = self.get_total_displacement(node)
        points = []
        for i in range(len(coord)):
            a0 = coord[i][0].split(',')
            a1 = coord[i][1].split(',')
            points += (self.get_points(node, a0, a1, total,movingtime[i]))

        t = self.mob_time(node) * 10 if None in movingtime else sum(movingtime)*10
        interval = len(points) / t
        pointsL = []
        for id in np.arange(0, len(points), interval):
            if id < len(points) - interval:
                pointsL.append(points[int(id)])
            else:
                # set the last position according to the coordinates
                pointsL.append(points[int(len(points)-1)])
        return pointsL

    def get_movingtimes(self,node,paths):
        movingtime=[]
        if hasattr(node, 'movingtime'):
            for i in node.movingtime:
                if i<=0:
                    movingtime.append(None)
                else:
                    movingtime.append(i)

        if None in movingtime or len(movingtime)<paths:
            return [None for i in range(paths)]
        else:
            return movingtime

    # def do_handover(self, intf, ap_intf):
    #     "Association Control: mechanisms that optimize the use of the APs"
    #     changeAP = False
    #     if self.ac and intf.associatedTo and ap_intf.node != intf.associatedTo:
    #         changeAP = AssCtrl(intf, ap_intf, self.ac).changeAP
    #         # if changeAP:
    #         #     output('changeap'+str(intf)+''+str(ap_intf)+'\n')
    #         # else:
    #         #     output('not changeap' + str(intf) + '' + str(ap_intf)+'\n')
    #     if self.check_if_ap_exists(intf, ap_intf):
    #         if not intf.associatedTo or changeAP:
    #             if ap_intf.node != intf.associatedTo:
    #                 intf.associate_infra(ap_intf)

    def run(self, mob_nodes, draw, coordinate, dim, mob_start_time=0,
            mob_stop_time=10, reverse=False, mob_rep=1, **kwargs):

        for rep in range(mob_rep):
            sleep(mob_start_time)
            t1 = time()
            i = 0.1
            if reverse:
                for node in mob_nodes:
                    if rep % 2 == 1 or (rep % 2 == 0 and rep > 0):
                        fin_pos = node.params['finPos']
                        node.params['finPos'] = node.params['initPos']
                        node.params['initPos'] = fin_pos
                        if coordinate:
                            coordinate[node].reverse()

            if not coordinate:
                coordinate = dict()
                for node in mob_nodes:
                    self.calculate_diff_time(node)
                    coordinate[node] = self.create_coord(node, tracked=True)
            while mob_start_time <= time() - t1 + mob_start_time<= mob_stop_time:
                t2 = time()
                ismoving = True
                if t2 - t1 >= i:
                    ismoving= False
                    for node, pos in coordinate.items():
                        # print(str(len(pos))+" "+str(node.position)+" "+str(node.time)+"   "+str(node.endTime)+"  "+str(node.matrix_id))
                        # print(time() - t1 + mob_start_time)
                        if (t2 - t1) >= node.startTime and node.time <= node.endTime:
                            ismoving=True
                            node.matrix_id += 1
                            if node.matrix_id < len(coordinate[node]):
                                pos = pos[node.matrix_id]
                            else:
                                pos = pos[len(coordinate[node]) - 1]
                            # print('1:'+str(node.position))
                            # print('1:' + str(node.pos))
                            # print(coordinate[node])
                            self.set_pos(node, pos)
                            # print('2:' + str(node.position))
                            # print('2:'+str(node.pos))
                            node.time += 0.1
                            if draw:
                                node_update = getattr(node, dim)
                                node_update()
                    PlotGraph.pause()
                    i += 0.1
                while self.pause_simulation:
                    pass
                if not ismoving:
                    break
            if rep == mob_rep:
                self.thread_._keep_alive = False
            else:
                for node, pos in coordinate.items():
                    node.time = node.startTime
                    node.matrix_id = 0
                    if not reverse:
                        self.set_pos(node, pos[0])
                        if draw:
                            node_update = getattr(node, dim)
                            node_update()
                PlotGraph.pause()

class OSMConfigMobility(Mobility):
    OSM_MAP=None
    def __init__(self, *args, **kwargs):
        self.OSM_config_mobility(*args, **kwargs)

    def get_OSM_Map(self):
        return self.OSM_MAP

    def NodeMobilitySimpleConfig(self,node,coord=[],movingtime=[],node_start_time=0,node_stop_time=None,positive_direction=True,*args,**kwargs):
        if not coord or node is None or node_stop_time is None:
            raise Exception('coord is None or node is None or node_stop_time is None')
        if positive_direction:
            return {node:{'coord':coord,'movingtime':movingtime,'node_start_time':node_start_time,'node_stop_time':node_stop_time}}
        else:
            coord.reverse()
            return {node: {'coord': coord, 'movingtime': movingtime, 'node_start_time': node_start_time,'node_stop_time': node_stop_time}}

    def OSM_config_mobility(self, *args, **kwargs):
        'configure Mobility Parameters'
        node = args[0]
        stage = args[1]

        if stage == 'start':
            pos = kwargs['position'].split(',') if 'position' in kwargs \
                else node.coord[0].split(',')
            node.params['initPos'] = self.get_position(pos)
            node.startTime = kwargs['time']
        elif stage == 'stop':
            pos = kwargs['position'].split(',') if 'position' in kwargs \
                else node.coord[-1].split(',')
            node.params['finPos'] = self.get_position(pos)
            node.speed = kwargs.get('speed',1)
            self.calculate_diff_time(node, kwargs['time'])

    def MobilityDataConfiguration(self,*args,NodeMobilityConfig={}, **kwargs):
        if not isinstance(NodeMobilityConfig,dict):
            raise Exception('the type of mobnode_cofig object is incorrect,mobnode_cofig must be a dict object')
        for key,value in NodeMobilityConfig.items():
            coord=value.get('coord',[])
            if coord:key.coord=coord
            movingtime = value.get('movingtime', [])
            if coord and movingtime:key.movingtime=movingtime
            self.OSM_config_mobility(key, 'start', time=value.get('node_start_time',0))
            endtime=value.get('node_stop_time',None)
            if endtime is not None: self.OSM_config_mobility(key, 'stop',time=endtime,speed=kwargs.get('speed', None))
            elif endtime is None and movingtime:
                endtime=sum(movingtime)+key.startTime
                self.OSM_config_mobility(key, 'stop',time=endtime,speed=kwargs.get('speed', None))
            else: raise Exception('{}: node_stop_time is None and (movingtime is None or mobility_stop_time is None), incorrect setting'.format(key.name))

class OSMConfigMobilityForHigway(OSMConfigMobility):
    Roads=None
    def __init__(self,*args, **kwargs):
        self.OSM_config_mobility_for_higway(*args, **kwargs)

    def get_Roads(self):
        return self.Roads

    def HigwayConfig_For_NodeMobility(self,node,higwayid,node_start_time=0,movingtime=[],node_stop_time=None,speed=None,total_move_time=None,positive_direction=True,*args,**kwargs):
        roads=self.get_Roads()
        if roads is None:
            raise Exception('The Roads object is None')

        higway=roads.get_HigwayPointlistById(higwayid)
        if higway is None:
            raise Exception('The {} id of higway not exist'.format(higwayid))

        if higway:
            coord=higway[1]
            if node_stop_time is None:
                if movingtime: node_stop_time=sum(movingtime)+node_start_time
                elif speed is not None and speed !=0 :
                    higwaylength=Roads.Compute_HigwayLength(higway)
                    node_stop_time=(higwaylength/speed)+node_start_time
                elif total_move_time is not None : node_stop_time=total_move_time+node_start_time
                else: raise Exception('The node_stop_time is uncertainty')
            return self.NodeMobilitySimpleConfig(node,coord,movingtime,node_start_time,node_stop_time,positive_direction)
        else:
            Exception('NodeMobility_For_Higway_config fail')

    def OSM_config_mobility_for_higway(self,*args, **kwargs):
        NodeMobilityConfig=self.HigwayConfig_For_NodeMobility(*args, **kwargs)
        self.MobilityDataConfiguration(*args,NodeMobilityConfig=NodeMobilityConfig,**kwargs)
        # if not isinstance(NodeMobilityConfig,dict):
        #     raise Exception('the type of mobnode_cofig object is incorrect,mobnode_cofig must be a dict object')
        # for key,value in NodeMobilityConfig.items():
        #     coord=value.get('coord',[])
        #     if coord:key.coord=coord
        #     movingtime = value.get('movingtime', [])
        #     if coord and movingtime:key.movingtime=movingtime
        #     self.OSM_config_mobility(key, 'start', time=value.get('node_start_time',0))
        #     endtime=value.get('node_stop_time',None)
        #     if endtime is not None: self.OSM_config_mobility(key, 'stop',time=endtime,speed=kwargs.get('speed', None))
        #     elif endtime is None and movingtime:
        #         endtime=sum(movingtime)+key.startTime
        #         self.OSM_config_mobility(key, 'stop',time=endtime,speed=kwargs.get('speed', None))
        #     else: raise Exception('{}: node_stop_time is None and (movingtime is None or mobility_stop_time is None), incorrect setting'.format(key.name))

class OSMConfigMobilityForConfigurationData(OSMConfigMobility):
    def __init__(self, *args, **kwargs):
        self.OSM_config_mobility_for_configuration_data(*args, **kwargs)

    def ConfigurationData_For_NodeMobility(self,node,node_start_time=0,movingtime=[],node_stop_time=None,speed=None,total_move_time=None,positive_direction=True,*args,**kwargs):

        if kwargs.get("coord",None):
            coord=kwargs.get("coord",None)
            if node_stop_time is None:
                if movingtime: node_stop_time=sum(movingtime)+node_start_time
                elif speed is not None and speed !=0 and kwargs.get("distance",None):
                    routelength=kwargs.get("distance",None)
                    node_stop_time=(routelength/speed)+node_start_time
                elif total_move_time is not None : node_stop_time=total_move_time+node_start_time
                else: raise Exception('The node_stop_time is uncertainty')
            return self.NodeMobilitySimpleConfig(node,coord,movingtime,node_start_time,node_stop_time,positive_direction)
        else:
            Exception('NodeMobility_For_Higway_config fail')

    def OSM_config_mobility_for_configuration_data(self,*args, **kwargs):
        NodeMobilityConfig=kwargs.get('NodeMobilityConfig',None)
        if NodeMobilityConfig:
            if not isinstance(NodeMobilityConfig, dict):
                raise Exception('the type of mobnode_cofig object is incorrect,mobnode_cofig must be a dict object')
            configdata = self.ConfigurationData_For_NodeMobility(*args,**NodeMobilityConfig,**kwargs)
            kwargs['NodeMobilityConfig']=configdata
            self.MobilityDataConfiguration(*args,**kwargs)

        else:
            raise Exception("The Date of NodeMobilityConfig not Exist")

