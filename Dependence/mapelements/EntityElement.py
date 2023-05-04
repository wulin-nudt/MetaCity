from mapelements.MapElement import *
class Node(MapElement):
    def __init__(self,id,tag,lat,lon):
        super(Node,self).__init__(id,'NODE',tag)
        self.__lat=lat
        self.__lon=lon

    def get_lat(self):
        return  self.__lat

    def get_lon(self):
        return  self.__lon

class Line(MapElement):
    def __init__(self,id,tag,nodes=list()):
        super(Line,self).__init__(id,'LINE',tag)
        self.__nodes=nodes

    def get_nodes(self):
        return self.__nodes

class Area(MapElement):
    def __init__(self,id,tag,nodes=list()):
        super(Area,self).__init__(id,'AREA',tag)
        self.__nodes=nodes

    def get_nodes(self):
        return self.__nodes

class Relation(MapElement):
    def __init__(self,id,tag,members=dict()):
        super(Relation,self).__init__(id,'RELATION',tag)
        self.__members=members

    def get_members(self):
        return  self.__members



# nn=Node(10,{'test':'11'},23.33,24.55)
# nn1=Node(12,{'test':'11'},23.33,24.55)
# # ll=Line(111,{'test':'11'},[nn,nn1])
# # print(ll.get_id())
# # print(ll.get_nodes())
# # print(nn.get_tag())
# # nn.set_tag('test2','22')
# # print(nn.get_tag())