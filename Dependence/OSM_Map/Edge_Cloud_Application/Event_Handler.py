from OSM_Map.OSM_Event_Handler import OSM_Anonymous_Event_Handler, OSM_Event_Handler
from jinja2 import Template


class ContextmenuEvent_For_EdgeCloudMarker(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);
                 $('#{{this.configuration_menu.get_name()}}')[0]['belong']=e.target;
                }
                """)

    def __init__(self, configuration_menu):
        super(ContextmenuEvent_For_EdgeCloudMarker, self).__init__()
        self._name = 'ContextmenuEvent_For_EdgeCloudMarker'
        self.event_type = 'contextmenu'
        self.configuration_menu = configuration_menu


class MoveEvent_For_EdgeCloudMarker(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){ 
                {% if this._parent.autopopup %}
                                let lat = e.latlng.lat.toString(),
                                lng = e.latlng.lng.toString();
                                {{this._parent.get_name()}}.bindPopup({{ this._parent.autopopup }});
                {% endif %}
                {{this._parent.get_name()}}['links'].forEach(function(link)
                            {
                            let or=link['origin'];
                            let de=link['destination'];
                            let origin=[or.getLatLng().lat,or.getLatLng().lng];
                            let destination=[de.getLatLng().lat,de.getLatLng().lng];
                            link['link'].setLatLngs([origin,destination]);
                            }
                            );

                 let point = {{this._parent.get_name()}};
                 point['configuration']['location']=[point.getLatLng().lat,point.getLatLng().lng];
                 point['configuration']['position']=point.getXYZ();
                            }
                """)

    def __init__(self):
        super(MoveEvent_For_EdgeCloudMarker, self).__init__()
        self._name = 'MoveEvent_For_EdgeCloudMarker'
        self.event_type = 'move'