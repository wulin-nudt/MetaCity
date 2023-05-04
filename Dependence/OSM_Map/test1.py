
# import folium
# world_map = folium.Map()
# world_map.save('test_01.html')
from jinja2 import Template
from OSM_Map.OSM_Marker import OSM_ClickForMarker
import os
import jinja2
# tt=Template(u"""
#             {% macro script(this, kwargs) %}
#                 function newMarker(e){
#                     var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
#                     new_mark.dragging.enable();
#                     new_mark.on('contextmenu', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
#                     var lat = e.latlng.lat.toString(),
#                        lng = e.latlng.lng.toString();
#                     new_mark.bindPopup({{ this.popup }});
#                     };
#             {% endmacro %}
#             <h1>username:</h1>
#             """)
C=OSM_ClickForMarker()
# print(tt.render(this=C,kwargs=None).encode('utf-8'))
TemplateLoader = jinja2.FileSystemLoader(os.path.abspath('.'))
TemplateEnv = jinja2.Environment(loader=TemplateLoader)
template = TemplateEnv.get_template('jstest.html')
dsconf=template.render(this=C,kwargs=None)
print(dsconf)