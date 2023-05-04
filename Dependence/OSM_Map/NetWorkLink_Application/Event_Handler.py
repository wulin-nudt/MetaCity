from OSM_Map.OSM_Event_Handler import OSM_Anonymous_Event_Handler,OSM_Event_Handler
from jinja2 import Template


class ContextmenuEvent_For_NetWorkLink(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                         function(e){ 
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);
                 $('#{{this.configuration_menu.get_name()}}')[0]['belong']=e.target;
                            }
                """)

    def __init__(self,configuration_menu):
        super(ContextmenuEvent_For_NetWorkLink, self).__init__()
        self._name = 'ContextmenuEvent_For_NetWorkLink'
        self.event_type = 'contextmenu'
        self.configuration_menu = configuration_menu