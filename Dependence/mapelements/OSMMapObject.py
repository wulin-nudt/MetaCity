from mapelements.OSMObjectFactory import *
class OSMMapObject(object):
    def __init__(self,OSMObjectFactory):

        self.__ojf = OSMObjectFactory
        self.__ojf.start_construct()
        self.__nodes=self.__ojf.get_nodes()
        self.__lines=self.__ojf.get_lines()
        self.__areas=self.__ojf.get_areas()
        self.__bounds=self.__ojf.get_bounds()
        self.__relations=self.__ojf.get_relations()

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

    def get_node_ById(self,id):
        if id in self.__nodes:
            return self.__nodes[id]
        else:
            return None

    def get_line_ById(self,id):
        if id in self.__lines:
            return self.__lines[id]
        else:
            return None

    def get_area_ById(self,id):
        if id in self.__areas:
            return self.__areas[id]
        else:
            return None

    def get_relation_ById(self,id):
        if id in self.__relations:
            return self.__relations[id]
        else:
            return None

# osm=OSMMapObject(OSMXMLIterObjectFactory(r'osmfile/map1.osm'))
# print(osm.get_lines()['50335864'].get_tag())