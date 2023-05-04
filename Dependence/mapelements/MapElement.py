class MapElement(object):
    def __init__(self,id,type,tag=dict()):
        self.__id=id
        self.__tag=tag
        self.__type=type

    def get_id(self):
        return self.__id

    def get_tag(self):
        return self.__tag

    def set_tag(self,key,value):
        self.__tag[key]=value

    def get_type(self):
        return  self.__type

class Bounds(object):
    def __init__(self,maxlat,maxlon,minlat,minlon):
        self.__maxlat=maxlat
        self.__maxlon=maxlon
        self.__minlat=minlat
        self.__minlon=minlon

    def get_maxlat(self):
        return self.__maxlat

    def get_maxlon(self):
        return  self.__maxlon

    def get_minlat(self):
        return  self.__minlat

    def get_minlon(self):
        return  self.__minlon

# mm=MapElement(100,'node',{'test':'11'})
# mm.set_tag('test2','12')
# print(mm.get_id())
# print(mm.get_tag())
# print(mm.get_type())

# en=EntityElement(100,'node',{'test':'11'},20.00,25.00)
# print(en.get_type())
# print(en.get_id())
# en.set_tag('test2','12')
# print(en.get_tag())
