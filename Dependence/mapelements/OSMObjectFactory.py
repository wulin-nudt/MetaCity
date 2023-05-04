from  mapelements.EntityElement import *
from mapelements.OSMXMLParse import *
class OSMObjectFactory(metaclass=ABCMeta):

    @abstractmethod
    def get_nodes(self):
        pass

    @abstractmethod
    def get_lines(self):
        pass

    @abstractmethod
    def get_areas(self):
        pass

    @abstractmethod
    def get_bounds(self):
        pass

    @abstractmethod
    def get_relations(self):
        pass

    @abstractmethod
    def start_construct(self):
        pass

    @abstractmethod
    def get_osmfilepath(self):
        pass

class OSMXMLObjectFactory(OSMObjectFactory):
    def __init__(self,osm_filepath):
        self.__osmparse=OSMXMLParse(osm_filepath)
        self.__osm_filepath = osm_filepath
        self.__nodes=dict()
        self.__lines=dict()
        self.__areas=dict()
        self.__bounds = list()
        self.__relations = dict()

    def get_osmfilepath(self):
        return  self.__osm_filepath

    def __nodes_construct(self):  #从osm文件中创建出node(点)对象
        nodes=dict()
        for node in self.__osmparse.get_nodes() :
            id=node.getAttribute('id')
            tag=node.getElementsByTagName('tag')
            tag=dict(zip([tg.getAttribute('k') for tg in tag],[tg.getAttribute('v') for tg in tag]))
            lat=float(node.getAttribute('lat'))
            lon =float(node.getAttribute('lon'))
            nd=Node(id,tag,lat,lon)
            nodes[nd.get_id()]=nd
        return nodes

    def __lines_construct(self): #从osm文件中创建出line(线)对象
        lines=dict()
        for line in self.__osmparse.get_lines() :
            id=line.getAttribute('id')
            tag=line.getElementsByTagName('tag')
            tag = dict(zip([tg.getAttribute('k') for tg in tag], [tg.getAttribute('v') for tg in tag]))
            nodes=line.getElementsByTagName('nd')
            nodes=[nd.getAttribute('ref') for nd in nodes]
            ln=Line(id,tag,nodes)
            lines[ln.get_id()]=ln
        return lines

    def __areas_construct(self): #从osm文件中创建出areas(面)对象
        areas=dict()
        for area in self.__osmparse.get_areas() :
            id=area.getAttribute('id')
            tag=area.getElementsByTagName('tag')
            tag = dict(zip([tg.getAttribute('k') for tg in tag], [tg.getAttribute('v') for tg in tag]))
            nodes=area.getElementsByTagName('nd')
            nodes=[nd.getAttribute('ref') for nd in nodes]
            ar=Area(id,tag,nodes)
            areas[ar.get_id()]=ar
        return areas

    def __bounds_construct(self): #从osm文件中创建出bounds(边界)对象
        bounds=list()
        for bound in self.__osmparse.get_bounds() :
            minlat= bound.getAttribute('minlat')
            minlon= bound.getAttribute('minlon')
            maxlat= bound.getAttribute('maxlat')
            maxlon= bound.getAttribute('maxlon')
            bd=Bounds(minlat=minlat,minlon=minlon,maxlat=maxlat,maxlon=maxlon)
            bounds.append(bd)
        return bounds

    def __relations_construct(self): #从osm文件中创建出relation(关系)对象
        relations=dict()
        for relation in self.__osmparse.get_relations() :
            id= relation.getAttribute('id')
            tag = relation.getElementsByTagName('tag')
            tag = dict(zip([tg.getAttribute('k') for tg in tag], [tg.getAttribute('v') for tg in tag]))
            members=relation.getElementsByTagName('member')
            members=dict(zip(['{}:{}'.format(mb.getAttribute('type').replace('way','line_or_area'),mb.getAttribute('ref')) for mb in members],[mb.getAttribute('role') for mb in members]))
            re=Relation(id,tag,members)
            relations[re.get_id()]=re
        return  relations


    def start_construct(self): #开始进行地图对象构建的函数
        self.__nodes=self.__nodes_construct()
        self.__lines=self.__lines_construct()
        self.__areas=self.__areas_construct()
        self.__bounds=self.__bounds_construct()
        self.__relations=self.__relations_construct()

    def get_nodes(self):
        return self.__nodes

    def get_lines(self):
        return self.__lines

    def get_areas(self):
        return self.__areas

    def get_bounds(self):
        return self.__bounds

    def get_relations(self):
        return self.__relations

class OSMXMLIterObjectFactory(OSMObjectFactory):
    def __init__(self, osm_filepath,mode='fast'): #mode为构建模式，有fast 和 normal 2种，表示创建地图对象的速度
        self.__osmparse = OSMXMLIterParse(osm_filepath)
        self.__osm_filepath=osm_filepath
        self.__nodes = dict()
        self.__lines = dict()
        self.__areas = dict()
        self.__bounds = list()
        self.__relations = dict()
        self.__mode=mode

    def get_osmfilepath(self):
        return  self.__osm_filepath

    def start_construct(self):

        if self.__mode=='fast':
            self.__fast_mode()
        else:
            self.__normal_mode()

    def __fast_mode(self):
        osmtext=self.__osmparse.create_osmdomiterator(self.get_osmfilepath())
        tags = None
        nodes = None
        members = None
        id=None
        lat=None
        lon=None
        for event, elem in osmtext:
            if event == 'start':
                attrs = elem.attrib
                if elem.tag in ('node', 'way', 'relation'):
                    tags = {}
                    id = attrs['id']
                    if elem.tag == 'node':
                        lat = float(attrs['lat'])
                        lon = float(attrs['lon'])
                    elif elem.tag == 'way':
                        nodes = []
                    elif elem.tag == 'relation':
                        members = {}
                elif elem.tag == 'tag':
                    tags[attrs['k']] = attrs['v']
                elif elem.tag == 'nd':
                    nodes.append(attrs['ref'])
                elif elem.tag == 'member':
                    members['{}:{}'.format(attrs['type'], attrs['ref'])] = attrs['role']
            elif event == 'end':
                if elem.tag in ('node', 'way', 'relation','bounds'):
                    if elem.tag == 'node':
                        self.__nodes[id]=Node(id,tags,lat,lon)
                    elif elem.tag == 'way':
                        nds = elem.findall('nd')
                        if nds[0].attrib['ref'] == nds[-1].attrib['ref']:
                            self.__areas[id]=Area(id,tags,nodes)
                        else:
                            self.__lines[id] = Line(id, tags, nodes)
                    elif elem.tag == 'relation':
                        self.__relations[id]=Relation(id,tags,members)
                    elif elem.tag == 'bounds':
                        self.__bounds.append(Bounds(float(elem.attrib['maxlat']),float(elem.attrib['maxlon']),float(elem.attrib['minlat']),float(elem.attrib['minlon'])))
                    elem.clear()

    def __normal_mode(self):
        self.__nodes=self.__nodes_construct()
        self.__lines=self.__lines_construct()
        self.__areas=self.__areas_construct()
        self.__bounds=self.__bounds_construct()
        self.__relations=self.__relations_construct()

    def get_nodes(self):
        return self.__nodes

    def get_lines(self):
        return self.__lines

    def get_areas(self):
        return self.__areas

    def get_bounds(self):
        return self.__bounds

    def get_relations(self):
        return self.__relations

    def __nodes_construct(self):  #从osm文件中创建出node(点)对象
        nodes=dict()
        for node in self.__osmparse.get_nodes():
            id=node.attrib['id']
            tag=node.findall('tag')
            tag=dict(zip([tg.attrib['k'] for tg in tag],[tg.attrib['v'] for tg in tag]))
            lat=float(node.attrib['lat'])
            lon =float(node.attrib['lon'])
            nd=Node(id,tag,lat,lon)
            nodes[nd.get_id()]=nd
        return nodes

    def __lines_construct(self): #从osm文件中创建出line(线)对象
        lines=dict()
        for line in self.__osmparse.get_lines() :
            id=line.attrib['id']
            tag=line.findall('tag')
            tag = dict(zip([tg.attrib['k'] for tg in tag], [tg.attrib['v'] for tg in tag]))
            nodes=line.findall('nd')
            nodes=[nd.attrib['ref'] for nd in nodes]
            ln=Line(id,tag,nodes)
            lines[ln.get_id()]=ln
        return lines

    def __areas_construct(self): #从osm文件中创建出areas(面)对象
        areas=dict()
        for area in self.__osmparse.get_areas() :
            id=area.attrib['id']
            tag=area.findall('tag')
            tag = dict(zip([tg.attrib['k'] for tg in tag], [tg.attrib['v'] for tg in tag]))
            nodes=area.findall('nd')
            nodes=[nd.attrib['ref'] for nd in nodes]
            ar=Area(id,tag,nodes)
            areas[ar.get_id()]=ar
        return areas

    def __bounds_construct(self): #从osm文件中创建出bounds(边界)对象
        bounds=list()
        for bound in self.__osmparse.get_bounds() :
            minlat= float(bound.attrib['minlat'])
            minlon= float(bound.attrib['minlon'])
            maxlat= float(bound.attrib['maxlat'])
            maxlon= float(bound.attrib['maxlon'])
            bd=Bounds(minlat=minlat,minlon=minlon,maxlat=maxlat,maxlon=maxlon)
            bounds.append(bd)
        return bounds

    def __relations_construct(self): #从osm文件中创建出relation(关系)对象
        relations=dict()
        for relation in self.__osmparse.get_relations() :
            id= relation.attrib['id']
            tag = relation.findall('tag')
            tag = dict(zip([tg.attrib['k'] for tg in tag], [tg.attrib['v'] for tg in tag]))
            members=relation.findall('member')
            members=dict(zip(['{}:{}'.format(mb.attrib['type'].replace('way','line_or_area'),mb.attrib['ref']) for mb in members],[mb.attrib['role'] for mb in members]))
            re=Relation(id,tag,members)
            relations[re.get_id()]=re
        return  relations


# ojf=OSMXMLObjectFactory(r'osmfile/map2.osm')
# ojf.start_construct()
# print(len(ojf.get_nodes()))

# ojf=OSMXMLObjectFactory(r'map.osm')
# ojf.start_construct()
#
# print(ojf.get_nodes())
# print(ojf.get_lines())
# print(ojf.get_areas())
# print(ojf.get_bounds()[0].get_minlon())
# print(ojf.get_relations())
# # ojf.prepare_construct()
# # print(ojf.lines_construct()[0].get_tag())
# # print(ojf.areas_construct()[0].get_tag())
# # print(ojf.node_construct())
