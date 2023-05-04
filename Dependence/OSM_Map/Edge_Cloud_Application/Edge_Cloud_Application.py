from OSM_Map.OSM_Marker import Edge_Cloud_Marker
from OSM_Map.Edge_Cloud_Application.Configuration_Menu import Edge_Cloud_Configuration_Menu
from OSM_Map.Edge_Cloud_Application.Event_Handler import ContextmenuEvent_For_EdgeCloudMarker,MoveEvent_For_EdgeCloudMarker

class Edge_Cloud_Application(Edge_Cloud_Marker):

    def build(self):

        cm=Edge_Cloud_Configuration_Menu().add_to(self)
        cm.build()

        ContextmenuEvent_For_EdgeCloudMarker(cm).add_to(self)
        MoveEvent_For_EdgeCloudMarker().add_to(self)