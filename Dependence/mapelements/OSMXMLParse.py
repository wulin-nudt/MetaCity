from abc import abstractmethod,ABCMeta
from xml.dom.minidom import parse
from lxml.etree import iterparse
class OSMFileParse(metaclass=ABCMeta):


    @abstractmethod
    def get_nodes(self):
        pass

    @abstractmethod
    def get_ways(self):
        pass

    @abstractmethod
    def get_relations(self):
        pass

    @abstractmethod
    def get_bounds(self):
        pass

    @abstractmethod
    def get_lines(self):
        pass

    @abstractmethod
    def get_areas(self):
        pass

class OSMXMLParse(OSMFileParse):
    def __init__(self,osm_filepath):
        self.__osm_filepath = osm_filepath  # osm文件路径
        self.__osmdom = parse(self.__osm_filepath)  # 打开osm文件
        self.__root = self.__osmdom.documentElement  # 获取osm文件的根节点

    def get_osmroot(self):
        # print(self.__root.toxml()) 输入osm文件的内容
        return  self.__root

    def get_elements(self,tagname):
        return self.__root.getElementsByTagName(tagname) # 获取一组指定的元素

    def get_nodes(self):
        return self.__root.getElementsByTagName('node') #获取osm文件中的node标签

    def get_ways(self):
        return self.__root.getElementsByTagName('way') #获取osm文件中的way标签

    def get_relations(self):
        return self.__root.getElementsByTagName('relation')  # 获取osm文件中的relation标签

    def get_bounds(self):
        return self.__root.getElementsByTagName('bounds')  # 获取osm文件中的bounds标签

    def __get_LinesAndArea(self): #获取osm文件中的Line对象和Area对象
        ways=self.get_ways()
        Line=[] #获取osm文件中的Line对象
        Area=[] #获取osm文件中的Area对象
        for way in ways :
            nd1=way.getElementsByTagName('nd')[0].getAttribute('ref')
            nd2 = way.getElementsByTagName('nd')[-1].getAttribute('ref')
            if nd1 == nd2:
                Area.append(way)
            else:
                Line.append(way)

        return [Line,Area]

    def get_lines(self):
        return self.__get_LinesAndArea()[0]

    def get_areas(self):
        return self.__get_LinesAndArea()[1]

class OSMXMLIterParse(OSMFileParse):
    def __init__(self,osm_filepath):
        self.__osm_filepath = osm_filepath  # osm文件路径
        self.__osmdom = iterparse(self.__osm_filepath,events=('start', 'end'))# 返回文本迭代器对象
        self.__nodes=[]
        self.__relations=[]
        self.__ways = []
        self.__areas=[]
        self.__lines=[]
        self.__bounds=[]

    def create_osmdomiterator(self,osm_filepath):
        return iterparse(osm_filepath,events=('start', 'end'))

    def __construct(self):

        for event, elem in self.__osmdom:
            if event == 'end':
                if elem.tag in ('node', 'way', 'relation'):
                    if elem.tag == 'node':
                        self.__nodes.append(elem)
                    elif elem.tag == 'way':
                        self.__ways.append(elem)
                        nds=elem.findall('nd')
                        if nds[0].attrib['ref'] == nds[-1].attrib['ref'] :
                            self.__areas.append(elem)
                        else:
                            self.__lines.append(elem)
                    elif elem.tag == 'relation':
                        self.__relations.append(elem)
                elif elem.tag == 'bounds':
                    self.__bounds.append(elem)

    def get_nodes(self):
        self.__construct()
        return self.__nodes

    def get_ways(self):
        self.__construct()
        return self.__ways

    def get_relations(self):
        self.__construct()
        return self.__relations

    def get_bounds(self):
        self.__construct()
        return self.__bounds

    def get_lines(self):
        self.__construct()
        return self.__lines

    def get_areas(self):
        self.__construct()
        return self.__areas

# osm=OSMXMLIterParse(r'osmfile/map2.osm')
# print(osm.get_relations()[0].findall('member')[0].attrib)
# print(len(osm.get_nodes()))


# osm=OSMXMLParse(r'osmfile/map2.osm')
# print(osm.get_osmroot())
# print(len(osm.get_lines()))
# print(len(osm.get_nodes()))








