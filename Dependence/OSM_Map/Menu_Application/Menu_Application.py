from OSM_Map.Menu_Application.Top_Menu import Top_Menu
from OSM_Map.Menu_Application.Right_Menu import Right_Menu
from OSM_Map.Menu_Application.Bottom_Menu import Bottom_Menu
from branca.element import Element

class Menu_Application(Element):

    def __init__(self,map,configuration_layer,entity):
        super(Menu_Application, self).__init__()
        self.map=map
        self.entity=entity
        self.configuration_layer=configuration_layer

    def build(self):

        if self._parent:
            self.OSM_Application=self._parent.get_root()
        else:
            self.OSM_Application = self.map.get_root()

        top = Top_Menu(row=1, col=1, left='1%', width='85%', menuName='顶菜单').add_to(self.OSM_Application)
        top.build(self.map)
        self.OSM_Application.move_to_end(top, last=False)

        rm=Right_Menu(row=7, col=1, left='2%', top='2%', width='12%', menuName='操作界面').add_to(self.OSM_Application)
        rm.build(self.map,self.entity)

        bottom=Bottom_Menu(row=1, col=4, left='5%', width='85%', menuName='主菜单').add_to(self.OSM_Application)
        bottom.build(self.configuration_layer,self.entity)

