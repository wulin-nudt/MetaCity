from mapelements.OSMMapObject import OSMMapObject
from mapelements.OSMObjectFactory import OSMXMLIterObjectFactory
import math
class Roads(object):
    def __init__(self,OSMMapObject):
        self.osm=OSMMapObject
        self.Init_LineHighways()
        self.Init_RingHighways()
        self.Highways = self.LineHighway
        self.Highways.update(self.RingHighway)
        self.Init_HigwayPointlists()

    def Init_LineHighways(self):
        highway={}
        for id,line in self.osm.get_lines().items():
          if 'highway' in line.get_tag():
              highway[id]=line
        self.LineHighway=highway

    def Init_RingHighways(self):
        highway={}
        for id,area in self.osm.get_areas().items():
          if 'highway' in area.get_tag():
              highway[id]=area
        self.RingHighway=highway

    def Init_HigwayPointlists(self):
        highway=self.Highways
        nodes=self.osm.get_nodes()
        HigwayPointlists=dict()
        for k,h in highway.items():
            pointlist=[]
            for n in h.get_nodes():
                polt_tuple=self.Compute_relativePot(self.osm.get_bounds()[0], nodes[n])
                pot='{},{},0'.format(polt_tuple[0],polt_tuple[1])
                pointlist.append(pot)
            HigwayPointlists[h.get_id()]=(h,pointlist)
        self.HigwayPointlists=HigwayPointlists

    #在经线上, 相差一度维度约为111km
    #在纬线上,相差一度经度约为111cosα（α为该纬线的维度）
    def Compute_relativePot(self,bouds,node,scale_factor=111000): #scale_factor 经纬度比例因子，比如1度等于110公里
        y=(node.get_lat()-bouds.get_minlat())*scale_factor
        x=(node.get_lon()-bouds.get_minlon())*scale_factor*math.cos(math.radians(node.get_lat()))
        # if x<0 or y<0:
        #     raise Exception('node relativePoint x {}<0 or y {} <0'.format(x,y))
        return (int(x-800),int(y-40))

    @classmethod
    def Compute_HigwayLength(cls,higway=None):
        length=0
        if higway is not None:
            for i in range(len(higway[1])-1):
                p1 = higway[1][i].split(',')
                p2 = higway[1][i+1].split(',')
                dif=[float(p2[0])-float(p1[0]),float(p2[1])-float(p1[1]),float(p2[2])-float(p1[2])]
                distance=pow(pow(dif[0],2)+pow(dif[1],2)+pow(dif[2],2),0.5)
                length=length+round(distance, 2)
        return round(length, 2)


    def get_bounds(self):
        return self.osm.get_bounds()

    def get_LineHighways(self):
        return self.LineHighway

    def get_RingHighways(self):
        return self.RingHighway

    def get_Highways(self):
        return self.Highways

    def get_HigwayPointlists(self):
        return self.HigwayPointlists

    def get_HigwayById(self,id=''):
        return self.Highways.get(id,None)

    def get_HigwayPointlistById(self,id=''):
        return self.HigwayPointlists.get(id,None)

# osm=OSMMapObject(OSMXMLIterObjectFactory(r'/home/kylin/Desktop/PythonProject/pythonProject/mapelements/osmfile/map1.osm'))
# r=Roads(osm)
# print(r.get_HigwayPointlistById('173299334'))
# print(r.get_HigwayPointlists())
# print(list(r.get_HigwayPointlists().keys())[-1])
# print(r.Compute_HigwayLength(r.HigwayPointlists['173299334']))
# print(r.get_HigwayPointlist())
# print(r.get_bounds()[0].get_minlat())