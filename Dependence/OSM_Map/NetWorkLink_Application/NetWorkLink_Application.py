from OSM_Map.OSM_Marker import NetWorkLink
from OSM_Map.NetWorkLink_Application.Event_Handler import ContextmenuEvent_For_NetWorkLink
from OSM_Map.NetWorkLink_Application.Configuration_Menu import NetWorkLink_Configuration_Menu

class NetWorkLink_Application(NetWorkLink):

    def build(self):
        cm=NetWorkLink_Configuration_Menu().add_to(self)
        cm.build()

        ContextmenuEvent_For_NetWorkLink(cm).add_to(self)


