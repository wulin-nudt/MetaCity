from OSM_Map.OSM_Marker import Wireless_Access_Point_Marker
from OSM_Map.Wireless_Access_Point_Application.Event_Handler import ContextmenuEvent_For_WirelessAccessPointMarker,MoveEvent_For_WirelessAccessPointMarker,MoveEndEvent_For_WirelessAccessPointMarker
from OSM_Map.Wireless_Access_Point_Application.Configuration_Menu import Wireless_Access_Point_Configuration_Menu

class Wireless_Access_Point_Application(Wireless_Access_Point_Marker):

    def build(self):
        cm=Wireless_Access_Point_Configuration_Menu().add_to(self)
        cm.build()

        ContextmenuEvent_For_WirelessAccessPointMarker(cm).add_to(self)
        MoveEvent_For_WirelessAccessPointMarker().add_to(self)
        MoveEndEvent_For_WirelessAccessPointMarker().add_to(self)

Base_Station_Application=Wireless_Access_Point_Application
