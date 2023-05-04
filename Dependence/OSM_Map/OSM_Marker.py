from folium.features import ClickForMarker,Circle,path_options
from folium.map import Popup,Tooltip,Marker,Icon
from folium.utilities import parse_options,camelize
from branca.element import (Element, Figure, JavascriptLink, MacroElement,Html)
from OSM_Map.OSM_Folium_Element import Inner_Element_For_Function,Function_Element
from jinja2 import Template
from folium import PolyLine

class OSM_Signal_Range(Inner_Element_For_Function):
    _template = Template(u"""
            let {{ this.get_name() }} = L.circle(
                e.latlng,
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_LayerName() or this._parent.get_MapName() }});
            
            {{this.get_name()}}['type']='{{this._name}}';
            
            {% for name, element in this.script._children.items() %}
                        {{element.render()}}
            {% endfor %}
        """)

    def __init__(self, radius=50, popup=None, tooltip=None, **kwargs):
        super(OSM_Signal_Range, self).__init__()
        self._name = 'OSM_Signal_Range'
        self.options = path_options(line=False, radius=radius, **kwargs)
        self.radius=radius

        if popup is not None and type(popup)!=Popup:
            self.add_child(popup if type(popup)==OSM_Popup
                           else OSM_Popup(str(popup)))
        else:
            p=OSM_Popup('radius: {}'.format(radius),max_width=300)
            self.add_child(p)

        if tooltip is not None and type(tooltip)!=Tooltip:
            self.add_child(tooltip if isinstance(tooltip, OSM_Tooltip)
                           else Tooltip(str(tooltip)))



class OSM_Tooltip(Inner_Element_For_Function):
    _template = Template(u"""
            {{ this._parent.get_name() }}.bindTooltip(
                `<div{% if this.style %} style={{ this.style|tojson }}{% endif %}>
                     {{ this.text }}
                 </div>`,
                {{ this.options|tojson }}
            );
        """)
    valid_options = {
        'pane': (str, ),
        'offset': (tuple, ),
        'direction': (str, ),
        'permanent': (bool, ),
        'sticky': (bool, ),
        'interactive': (bool, ),
        'opacity': (float, int),
        'attribution': (str, ),
        'className': (str, ),
    }

    def __init__(self, text, style=None, sticky=True, **kwargs):
        super(OSM_Tooltip, self).__init__()
        self._name = 'Tooltip'

        self.text = str(text)

        kwargs.update({'sticky': sticky})
        self.options = self.parse_options(kwargs)

        if style:
            assert isinstance(style, str), \
                'Pass a valid inline HTML style property string to style.'
            # noqa outside of type checking.
            self.style = style

    def parse_options(self, kwargs):
        """Validate the provided kwargs and return options as json string."""
        kwargs = {camelize(key): value for key, value in kwargs.items()}
        for key in kwargs.keys():
            assert key in self.valid_options, (
                'The option {} is not in the available options: {}.'
                .format(key, ', '.join(self.valid_options))
            )
            assert isinstance(kwargs[key], self.valid_options[key]), (
                'The option {} must be one of the following types: {}.'
                .format(key, self.valid_options[key])
            )
        return kwargs



class OSM_Icon(Inner_Element_For_Function):
    _template = Template(u"""
    
            var {{ this.get_name() }} = L.AwesomeMarkers.icon(
                {{ this.options|tojson }}
            );
            {{ this._parent.get_name() }}.setIcon({{ this.get_name() }});
            
        """)
    color_options = {'red', 'darkred',  'lightred', 'orange', 'beige',
                     'green', 'darkgreen', 'lightgreen',
                     'blue', 'darkblue', 'cadetblue', 'lightblue',
                     'purple',  'darkpurple', 'pink',
                     'white', 'gray', 'lightgray', 'black'}

    def __init__(self, color='blue', icon_color='white', icon='info-sign',
                 angle=0, prefix='glyphicon', **kwargs):
        super(OSM_Icon, self).__init__()
        self._name = 'OSM_Icon'
        if color not in self.color_options:
            warnings.warn('color argument of Icon should be one of: {}.'
                          .format(self.color_options), stacklevel=2)
        self.options = parse_options(
            marker_color=color,
            icon_color=icon_color,
            icon=icon,
            prefix=prefix,
            extra_classes='fa-rotate-{}'.format(angle),
            **kwargs
        )


class OSM_Popup(Inner_Element_For_Function):
    _template = Template(u"""
        var {{this.get_name()}} = L.popup({{ this.options|tojson }});

        {% for name, element in this.html._children.items() %}
            let {{ name }} = $(`{{ element.render(**kwargs).replace('\\n',' ') }}`)[0];
            {{ this.get_name() }}.setContent({{ name }});
        {% endfor %}

        {{ this._parent.get_name() }}.bindPopup({{ this.get_name() }})
        {% if this.show %}.openPopup(){% endif %};
        

        {% for name, element in this.script._children.items() %}
            {{element.render()}}
        {% endfor %}
        
        {% for k,v in this._event.items() %}
        {% for v1 in v %}
        {{this.get_name()}}.on('{{k}}',{{v1}});
        {% endfor %}
        {% endfor %}
    """)  # noqa
    def __init__(self, html=None, parse_html=False, max_width='100%',
                 show=False, sticky=False, **kwargs):
        super(OSM_Popup, self).__init__()
        self._name = 'OSM_Popup'
        script = not parse_html

        if isinstance(html, Element):
            self.html.add_child(html)
        elif isinstance(html, str):
            self.html.add_child(Html(html, script=script))

        self.show = show
        self.options = parse_options(
            max_width=max_width,
            autoClose=False if show or sticky else None,
            closeOnClick=False if sticky else None,
            **kwargs
        )

class OSM_Marker(Function_Element):
    _template = Template(u"""
    {% macro script(this, kwargs) %}
            
            function {{this.get_name()}}(e){
            
                    let {{this.get_name()}} = L.marker(e.latlng,{"autoPan": true}).addTo({{this._parent.get_name()}});
                    
                    let configuration = {{ this.configuration|tojson|safe }};
                    {{this.get_name()}}['configuration']=configuration;
            
        
                    {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    {{this.get_name()}}.on('{{k}}',{{v1}});
                    {% endfor %}
                    {% endfor %}

                    let lat = e.latlng.lat.toString(),
                       lng = e.latlng.lng.toString();

                    {% for name, element in this.script._children.items() %}
                                {{element.render()}}
                    {% endfor %}

                    };
                    
                {% if this.active %}
                {{this.get_MapName()}}.on('click', {{this.get_name()}});
                {% endif %}
            
     {% endmacro %}
    """)

    def __init__(self, name='', popup=None, tooltip=None,
                 icon=None, active=True, configuration={},**kwargs):
        super(OSM_Marker, self).__init__()
        self._name = name
        self.type = name
        self.options = parse_options(
            draggable=True or None,
            autoPan=True or None,
            **kwargs
        )

        self.active = active
        self.configuration=configuration

        if icon is not None and type(icon) != Icon:
            self.add_child(icon if type(icon) == OSM_Icon
                           else OSM_Icon(color='red', icon='arrow-circle-up', prefix='fa'))
            self.icon = icon

        if popup is not None and type(popup) != Popup:
            self.autopopup = ''
            # self.popup=popup if isinstance(popup, Popup) else Popup(str(popup),max_width=300)

            self.add_child(popup if type(popup) == OSM_Popup
                           else OSM_Popup(str(popup)))
        else:
            self.autopopup = '"Latitude: " + lat + "<br>Longitude: " + lng '
            p = OSM_Popup('Latitude: ${lat} <br>Longitude: ${lng} ', max_width=300)
            self.add_child(p)

        if tooltip is not None and type(tooltip) != Tooltip:
            self.add_child(tooltip if isinstance(tooltip, OSM_Tooltip)
                           else Tooltip(str(tooltip)))

    def update_configuration(self,configuration=None):
        if configuration and isinstance(configuration,dict):
            self.configuration.update(configuration)

class Moving_Point_Marker(OSM_Marker):
    _template = Template(u"""
            {% macro script(this, kwargs) %}
            
                function {{this.get_name()}}(e){
                    let Moving_Point_Layer = undefined;
                    if(!{{this._parent.get_name()}}['Moving_Point_Layer'])
                    {
                    Moving_Point_Layer = L.layerGroup().addTo({{this._parent.get_name()}});
                    {{this._parent.get_name()}}['Moving_Point_Layer'] = Moving_Point_Layer;
                    let configuration = {{ this.configuration|tojson|safe }};
                    Moving_Point_Layer['configuration']=configuration;
                    Moving_Point_Layer['route']=L.layerGroup().addTo(Moving_Point_Layer);
                    for (x in {{this._parent.get_name()}}['configuration']) {
                    Moving_Point_Layer['configuration'][x]={{this._parent.get_name()}}['configuration'][x];
                                }
                    if(!{{this._parent.get_name()}}['{{this.type}}'])
                    {
                    {{this._parent.get_name()}}['{{this.type}}']=0;
                    }
                    Moving_Point_Layer['configuration']['name']='{{this._name}}'+ {{this._parent.get_name()}}['{{this.type}}'];
                    {{this._parent.get_name()}}['{{this.type}}']+=1;
                   Moving_Point_Layer['type']='{{this.type}}';
                   Moving_Point_Layer['configuration']['location']=[];
                   Moving_Point_Layer['configuration']['position']='0,0,0';
                   Moving_Point_Layer['configuration']['positions']=[];
                   Moving_Point_Layer['configuration']['routes_distance']=0;
                   Moving_Point_Layer['configuration']['routes_type']=undefined;
                   Moving_Point_Layer['configuration']['coord']=undefined;
                   Moving_Point_Layer['configuration']['routes']=undefined;
                   Moving_Point_Layer['configuration']['ip']={{this.get_LayerName()}}.allocateIP();
                   Moving_Point_Layer['configuration']['AUTO_ip']=Moving_Point_Layer['configuration']['ip'];
                   Moving_Point_Layer['configuration']['Auto_Configuration_ip']=true;
                   Moving_Point_Layer['configuration']['ip6']={{this.get_LayerName()}}.allocateIP6();
                   Moving_Point_Layer['configuration']['AUTO_ip6']=Moving_Point_Layer['configuration']['ip6'];
                   Moving_Point_Layer['configuration']['Auto_Configuration_ip6']=true;
                   Moving_Point_Layer['configuration']['mac']={{this.get_LayerName()}}.allocateMAC();
                   Moving_Point_Layer['configuration']['AUTO_mac']=Moving_Point_Layer['configuration']['mac'];
                   Moving_Point_Layer['configuration']['Auto_Configuration_mac']=true;
                   Moving_Point_Layer['routesToCoord'] = function(routes)
                   {
                   let center={{this._parent.get_MapName()}}.getCenter();
                   let coord=[];
                   routes.forEach(function(route){
                   let point=L.latLng(route);
                   let x_lng=  L.latLng(center.lat,point.lng);
                   let y_lat = L.latLng(point.lat, center.lng);
                   let coord_x= point.lng > center.lng ? center.distanceTo(x_lng) : 0 - center.distanceTo(x_lng);
                   let coord_y= point.lat > center.lat ? center.distanceTo(y_lat) : 0 - center.distanceTo(y_lat);
                   coord.push([Math.round(coord_x),Math.round(coord_y),0].toString());
                   });
                   return coord;
                   }
                    }
                    else
                    {
                    Moving_Point_Layer = {{this._parent.get_name()}}['Moving_Point_Layer'];
                    }
                    
                    let {{this.get_name()}} = L.marker(e.latlng,{"autoPan": true}).addTo(Moving_Point_Layer);
                    
                    {{this.get_name()}}['links']=[];
                    
                    {{this.get_name()}}['Moving_Point_Layer'] = Moving_Point_Layer;
                    
                    {{this.get_name()}}['configuration']=Moving_Point_Layer['configuration'];
                    
                    {{this.get_name()}}.getXYZ=function (){
                     let point = this;
                     let center={{this._parent.get_MapName()}}.getCenter();
                     let x_lng=  L.latLng(center.lat,point.getLatLng().lng);
                     let y_lat = L.latLng(point.getLatLng().lat, center.lng);
                     let coord_x= point.getLatLng().lng > center.lng ? center.distanceTo(x_lng) : 0 - center.distanceTo(x_lng);
                     let coord_y= point.getLatLng().lat > center.lat ? center.distanceTo(y_lat) : 0 - center.distanceTo(y_lat);
                     return [Math.round(coord_x),Math.round(coord_y),0];
                   }
                    {{this.get_name()}}['location'] = [e.latlng.lat,e.latlng.lng].toString();
                    Moving_Point_Layer['configuration']['location'].push({{this.get_name()}}['location']);
                    
                    {{this.get_name()}}['position']={{this.get_name()}}.getXYZ().toString();
                    Moving_Point_Layer['configuration']['positions'].push({{this.get_name()}}['position']);
                    
                    Moving_Point_Layer['configuration']['position'] = Moving_Point_Layer['configuration']['positions'][0];
                     
                     
                    {{this.get_name()}}['order']=Moving_Point_Layer['configuration']['location'].length;
                    
                    Moving_Point_Layer['route'].clearLayers();
                    Moving_Point_Layer['configuration']['coord']=undefined;
                    Moving_Point_Layer['configuration']['routes']=undefined;
                    Moving_Point_Layer['configuration']['routes_distance']=0;
                    

                    {{this.get_name()}}.dragging.enable();
                    {{this.get_name()}}['type']='{{this.type}}';


                    {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    {{this.get_name()}}.on('{{k}}',{{v1}});
                    {% endfor %}
                    {% endfor %}

                    let lat = e.latlng.lat.toString(),
                       lng = e.latlng.lng.toString();

                    {% for name, element in this.script._children.items() %}
                                {{element.render()}}
                    {% endfor %}

                    };
                {% if this.active %}
                {{this.get_MapName()}}.on('click', {{this.get_name()}});
                {% endif %}

            {% endmacro %}
            """)  # noqa

    def __init__(self, name='Moving_Point_Marker', popup=None, tooltip=None,
                 icon=None, active=True,configuration={}, **kwargs):
        super(Moving_Point_Marker, self).__init__(name=name,popup=popup,tooltip=tooltip,icon=icon,active=active,configuration=configuration,**kwargs)

class Edge_Cloud_Marker(OSM_Marker):
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                function {{this.get_name()}}(e){
                    let {{this.get_name()}} = L.marker(e.latlng,{"autoPan": true}).addTo({{this._parent.get_name()}});
                    {{this.get_name()}}['links']=[];
                    
                    let configuration = {{ this.configuration|tojson|safe }};
                    {{this.get_name()}}['configuration']=configuration;
                    
                    for (x in {{this._parent.get_name()}}['configuration']) {
                    {{this.get_name()}}['configuration'][x]={{this._parent.get_name()}}['configuration'][x];
                                      }
                    
                    if(!{{this._parent.get_name()}}['{{this.type}}'])
                    {
                    {{this._parent.get_name()}}['{{this.type}}']=0;
                    }
                    {{this.get_name()}}['configuration']['name']='{{this._name}}'+ {{this._parent.get_name()}}['{{this.type}}'];
                    {{this._parent.get_name()}}['{{this.type}}']+=1;
                    {{this.get_name()}}['configuration']['location']=[e.latlng.lat,e.latlng.lng];
                    {{this.get_name()}}.getXYZ=function (){
                     let point = this;
                     let center={{this._parent.get_MapName()}}.getCenter();
                     let x_lng=  L.latLng(center.lat,point.getLatLng().lng);
                     let y_lat = L.latLng(point.getLatLng().lat, center.lng);
                     let coord_x= point.getLatLng().lng > center.lng ? center.distanceTo(x_lng) : 0 - center.distanceTo(x_lng);
                     let coord_y= point.getLatLng().lat > center.lat ? center.distanceTo(y_lat) : 0 - center.distanceTo(y_lat);
                     return [Math.round(coord_x),Math.round(coord_y),0];
                   }
                   {{this.get_name()}}['configuration']['position']={{this.get_name()}}.getXYZ();
                   
                   {{this.get_name()}}['configuration']['ip']={{this.get_LayerName()}}.allocateIP();
                   {{this.get_name()}}['configuration']['AUTO_ip']={{this.get_name()}}['configuration']['ip'];
                   {{this.get_name()}}['configuration']['Auto_Configuration_ip']=true;
                   {{this.get_name()}}['configuration']['ip6']={{this.get_LayerName()}}.allocateIP6();
                   {{this.get_name()}}['configuration']['AUTO_ip6']={{this.get_name()}}['configuration']['ip6'];
                   {{this.get_name()}}['configuration']['Auto_Configuration_ip6']=true;
                   {{this.get_name()}}['configuration']['mac']={{this.get_LayerName()}}.allocateMAC();
                   {{this.get_name()}}['configuration']['AUTO_mac']={{this.get_name()}}['configuration']['mac'];
                   {{this.get_name()}}['configuration']['Auto_Configuration_mac']=true;
                   
                    {{this.get_name()}}.dragging.enable();
                    {{this.get_name()}}['type']='{{this.type}}';
                    
                    
                    {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    {{this.get_name()}}.on('{{k}}',{{v1}});
                    {% endfor %}
                    {% endfor %}
                    
                    let lat = e.latlng.lat.toString(),
                       lng = e.latlng.lng.toString();
                       
                    {% for name, element in this.script._children.items() %}
                                {{element.render()}}
                    {% endfor %}
                    
                    };
                {% if this.active %}
                {{this.get_MapName()}}.on('click', {{this.get_name()}});
                {% endif %}
                
            {% endmacro %}
            """)  # noqa
    def __init__(self,name='Edge_Cloud_Marker',popup=None, tooltip=None,
                 icon=None,active=True,configuration={}, **kwargs):
        super(Edge_Cloud_Marker, self).__init__(name=name,popup=popup,tooltip=tooltip,icon=icon,active=active,configuration=configuration,**kwargs)



class Wireless_Access_Point_Marker(OSM_Marker):
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                function {{this.get_name()}}(e){
                    let {{this.get_name()}} = L.marker(e.latlng,{"autoPan": true}).addTo({{this._parent.get_name()}});
                    {{this.get_name()}}['links']=[];
                    
                    let configuration = {{ this.configuration|tojson|safe }};
                    {{this.get_name()}}['configuration']=configuration;
                    
                    for (x in {{this._parent.get_name()}}['configuration']) {
                    {{this.get_name()}}['configuration'][x]={{this._parent.get_name()}}['configuration'][x];
                                      }
                    
                    if(!{{this._parent.get_name()}}['ovs'])
                    {
                    {{this._parent.get_name()}}['ovs']=0;
                    }
                    {{this.get_name()}}['configuration']['name']='{{this._name}}'+ {{this._parent.get_name()}}['ovs'];
                    {{this._parent.get_name()}}['ovs']+=1;
                    
                    {{this.get_name()}}['configuration']['ssid']='ssid-'+ {{this.get_name()}}['configuration']['name'];
                    {{this.get_name()}}['configuration']['location']=[e.latlng.lat,e.latlng.lng];
                    {{this.get_name()}}.getXYZ=function (){
                     let point = this;
                     let center={{this._parent.get_MapName()}}.getCenter();
                     let x_lng=  L.latLng(center.lat,point.getLatLng().lng);
                     let y_lat = L.latLng(point.getLatLng().lat, center.lng);
                     let coord_x= point.getLatLng().lng > center.lng ? center.distanceTo(x_lng) : 0 - center.distanceTo(x_lng);
                     let coord_y= point.getLatLng().lat > center.lat ? center.distanceTo(y_lat) : 0 - center.distanceTo(y_lat);
                     return [Math.round(coord_x),Math.round(coord_y),0];
                   }
                   {{this.get_name()}}['configuration']['position']={{this.get_name()}}.getXYZ();
                   
                   {{this.get_name()}}['configuration']['ip']={{this.get_LayerName()}}.allocateIP();
                   {{this.get_name()}}['configuration']['AUTO_ip']={{this.get_name()}}['configuration']['ip'];
                   {{this.get_name()}}['configuration']['Auto_Configuration_ip']=true;
                   {{this.get_name()}}['configuration']['ip6']={{this.get_LayerName()}}.allocateIP6();
                   {{this.get_name()}}['configuration']['AUTO_ip6']={{this.get_name()}}['configuration']['ip6'];
                   {{this.get_name()}}['configuration']['Auto_Configuration_ip6']=true;
                   {{this.get_name()}}['configuration']['mac']={{this.get_LayerName()}}.allocateMAC();
                   {{this.get_name()}}['configuration']['AUTO_mac']={{this.get_name()}}['configuration']['mac'];
                   {{this.get_name()}}['configuration']['Auto_Configuration_mac']=true;
                   
                   if({{this.get_name()}}['configuration']['{{this.type}}'+'_range']==undefined)
                   {
                   {{this.get_name()}}['configuration']['{{this.type}}'+'_range']={{this.signal_range.radius}};
                   }
                    
                    {{this.get_name()}}.dragging.enable();
                    {{this.get_name()}}['type']='{{this.type}}';
                    
                    
                    {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    {{this.get_name()}}.on('{{k}}',{{v1}});
                    {% endfor %}
                    {% endfor %}
                    
                    let lat = e.latlng.lat.toString(),
                       lng = e.latlng.lng.toString();

                    {% for name, element in this.script._children.items() %}
                                {{element.render()}}
                    {% endfor %}
                    
                    {% if this.signal_range %}
                                {{this.get_name()}}['signal_range']={{this.signal_range.get_name()}};
                                {{this.get_name()}}['signal_range'].setRadius({{this.get_name()}}['configuration']['{{this.type}}'+'_range']);
                    {% endif %}
                    };
                {% if this.active %}
                {{this.get_MapName()}}.on('click', {{this.get_name()}});
                {% endif %}
                //{{this.get_MapName()}}.on('mousemove',function(e,data){alert(Object.keys(e));})
            {% endmacro %}
            """)  # noqa
    def __init__(self,name='Wireless_Access_Point_Marker',popup=None, tooltip=None,
                 icon=None,active=True,signal_range=None,configuration={},**kwargs):
        super(Wireless_Access_Point_Marker, self).__init__(name=name,popup=popup,tooltip=tooltip,
                                                           icon=icon,active=active,configuration=configuration,**kwargs)

        if signal_range is not None and type(signal_range)!=Circle:

            sr= signal_range if isinstance(signal_range, OSM_Signal_Range) else OSM_Signal_Range(radius=signal_range)
            self.add_child(sr)
            self.signal_range = sr
        else:
            self.signal_range = None

class NetWorkLink(Function_Element):
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                function {{this.get_name()}}(e){
                let condition1=false;
                let condition2=false;
                let condition3=false;
                let switching_nodes = {{ this.switching_nodes|tojson|safe }};
                if({{this.get_MapName()}}['link_of_origin'])
                {
                   if({{this.get_MapName()}}['link_of_origin']==e.target)
                    {
                    condition1=true;
                    }
                    
                   if(!switching_nodes.includes({{this.get_MapName()}}['link_of_origin']['type']))
                    {
                    if(e.target['type'] && !switching_nodes.includes(e.target['type']))
                    {
                    condition2=true;
                    }
                    }
                  
                  if(e.target=={{this.get_MapName()}})
                   {
                    condition3=true;
                   }
                    
                }
                if(condition1||condition2||condition3)
                    {
                     {{this.get_MapName()}}.off('mousemove',NetWorkLink);
                     {{this.get_LayerName() or this.get_MapName()}}.removeLayer({{this.get_MapName()}}['poly_line']);
                     {{this.get_MapName()}}['link_of_origin']=undefined;
                     {{this.get_MapName()}}['poly_line']=undefined;
                     return;
                    }
                    
                    if({{this.get_MapName()}}['link_of_origin'])
                    {
                     let origin={{this.get_MapName()}}['poly_line'].getLatLngs()[0];
                     let destination=[e.target.getLatLng().lat,e.target.getLatLng().lng];
                     {{this.get_MapName()}}['poly_line'].setLatLngs([origin,destination]).addTo({{this.get_LayerName() or this.get_MapName()}});
                     {{this.get_MapName()}}['poly_line']['origin']={{this.get_MapName()}}['link_of_origin'];
                     {{this.get_MapName()}}['poly_line']['destination']=e.target;
                     {{this.get_MapName()}}['poly_line']['configuration']['node1']={{this.get_MapName()}}['link_of_origin']['configuration']['name'];
                     {{this.get_MapName()}}['poly_line']['configuration']['node2']=e.target['configuration']['name'];
                     let link={origin:{{this.get_MapName()}}['link_of_origin'],
                               destination:e.target,
                               link:{{this.get_MapName()}}['poly_line']
                                };
                     {{this.get_MapName()}}['link_of_origin']['links'].push(link);
                     e.target['links'].push(link);
                     {{this.get_MapName()}}.off('mousemove',NetWorkLink);
                     {{this.get_MapName()}}['link_of_origin']=undefined;
                     {{this.get_MapName()}}['poly_line']=undefined;
                    }
                    else 
                    {
                    let origin=[e.target.getLatLng().lat,e.target.getLatLng().lng];
                    let {{this.get_name()}}=L.polyline([origin,origin]);
                     {{this.get_name()}}['type']='{{this.type}}';
                     
                     let configuration = {{ this.configuration|tojson|safe }};
                     {{this.get_name()}}['configuration']=configuration;
                     
                    for (x in {{this._parent.get_name()}}['configuration']) {
                    {{this.get_name()}}['configuration'][x]={{this._parent.get_name()}}['configuration'][x];
                                      }
                     
                    if(!{{this._parent.get_name()}}['{{this.type}}'])
                    {
                    {{this._parent.get_name()}}['{{this.type}}']=0;
                    }
                    
                     {{this.get_name()}}['configuration']['name']='{{this._name}}'+ {{this._parent.get_name()}}['{{this.type}}'];
                     {{this._parent.get_name()}}['{{this.type}}']+=1;
                     
                     
                     {{this.get_MapName()}}['poly_line']={{this.get_name()}};
                     {{this.get_MapName()}}['link_of_origin']=e.target;
                     {{this.get_MapName()}}.on('mousemove',NetWorkLink);
                     
                     
                    {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    {{this.get_name()}}.on('{{k}}',{{v1}});
                    {% endfor %}
                    {% endfor %}
                     
                    {% for name, element in this.script._children.items() %}
                    {{element.render()}}
                    {% endfor %}
                    
                    }

                    }
                
                
                function NetWorkLink(e)
                {
                let origin=e.target['poly_line'].getLatLngs()[0];
                let destination=[e.latlng.lat,e.latlng.lng];
                e.target['poly_line'].setLatLngs([origin,destination]).addTo({{this.get_LayerName() or this.get_MapName()}});
                }
                
                {% if this.active %}
                {% if this.get_LayerName() %}
                
                {{this.get_LayerName()}}.eachLayer(function(layer){
                                    layer.on('click',{{this.get_name()}});
                                    }
                                    );
                
                {% endif %}
                {% endif %}
            
            {% endmacro %}
            """)  # noqa

    def __init__(self,switching_nodes=[],name='NetWorkLink',popup=None, tooltip=None,
                 active=True,configuration={},**kwargs):
        super(NetWorkLink, self).__init__()
        self.switching_nodes=[ s.type for s in switching_nodes] if switching_nodes else []
        self._name = name
        self.type = name
        self.configuration=configuration
        self.options = path_options(line=True, **kwargs)

        if popup is not None and type(popup)!=Popup:

            self.add_child(popup if type(popup)==OSM_Popup
                           else OSM_Popup(str(popup)))

        if tooltip is not None and type(tooltip)!=Tooltip:
            self.add_child(tooltip if isinstance(tooltip, OSM_Tooltip)
                           else Tooltip(str(tooltip)))

    def update_configuration(self,configuration=None):
        if configuration and isinstance(configuration,dict):
            self.configuration.update(configuration)