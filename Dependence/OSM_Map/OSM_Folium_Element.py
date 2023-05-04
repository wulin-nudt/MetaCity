import folium
from branca.element import (Element, Figure, JavascriptLink, MacroElement,Html)
from jinja2 import Template
from folium import Map

class Function_Element(Element):
    _template = Template(u'''
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    {{this.get_name()}}.on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
    ''')

    def __init__(self):
        super(Function_Element, self).__init__()
        self._name = 'Function_Element'

        self.header = Element()
        self.html = Element()
        self.script = Element()

        self.header._parent = self
        self.html._parent = self
        self.script._parent = self

        self._event = {'click': [], 'mouseover': [], 'mouseout': [],'contextmenu':[],
                       'move':[],'moveend':[],'popupopen':[],'mousedown':[],'mouseup':[],'popupclose':[]}
    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        for name, element in self._children.items():
            element.render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        header = self._template.module.__dict__.get('header', None)
        if header is not None:
            figure.header.add_child(Element(header(self, kwargs)),
                                    name=self.get_name())

        html = self._template.module.__dict__.get('html', None)
        if html is not None:
            figure.html.add_child(Element(html(self, kwargs)),
                                  name=self.get_name())

        script = self._template.module.__dict__.get('script', None)
        if script is not None:
            figure.script.add_child(Element(script(self, kwargs)),
                                    name=self.get_name())

    def get_MapName(self):

        if self._parent is not None and isinstance(self._parent,folium.folium.Map):
            return self._parent.get_name()
        elif self._parent is not None and hasattr(self._parent,'get_MapName'):
            return self._parent.get_MapName()
        else:
            raise Exception("MAP NOT EXIST")

    def get_LayerName(self):
        if self._parent is not None and isinstance(self._parent,OSM_Layer):
            return self._parent.get_name()
        elif self._parent is not None and hasattr(self._parent,'get_LayerName'):
            return self._parent.get_LayerName()
        else:
            return None

    def add_EventHandler(self,function,name=None, index=None):
        if(hasattr(function,'event_type')):
            if function.event_type in self._event:
                self._event[function.event_type].append(function.get_name())
                self.add_child(function, name=name, index=index)
            else:
                raise Exception('{} do not support this {} event'.format(self._name,function.event_type))
        else:
            raise Exception('It is not an event handler')

        return self._event[function.event_type]

class Inner_Element_For_Function(Function_Element):
    _template = Template(u'')

    def __init__(self):
        super(Inner_Element_For_Function, self).__init__()
        self._name = 'Inner_Element_For_Function'

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        for name, child in self._children.items():
            child.render(**kwargs)

        assert self._parent, ('You cannot render this Element '
                                            'if it is no parents.')

        self._parent.script.add_child(Element(
            self._template.render(this=self, kwargs=kwargs)),
            name=self.get_name())

class OSM_Application(Figure):

    def move_to_end(self,element,last=True):
        self._children.move_to_end(element.get_name(), last)

class OSM_Map(Map):
    _template = Template(u"""
        {% macro header(this, kwargs) %}
            <meta name="viewport" content="width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
            <style>
                #{{ this.get_name() }} {
                    position: {{this.position}};
                    width: {{this.width[0]}}{{this.width[1]}};
                    height: {{this.height[0]}}{{this.height[1]}};
                    left: {{this.left[0]}}{{this.left[1]}};
                    top: {{this.top[0]}}{{this.top[1]}};
                    display: {{this.display}};
                }
            </style>
        {% endmacro %}

        {% macro html(this, kwargs) %}
            <div class="folium-map" id={{ this.get_name()|tojson }} ></div>
        {% endmacro %}

        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.map(
                {{ this.get_name()|tojson }},
                {
                    center: {{ this.location|tojson }},
                    crs: L.CRS.{{ this.crs }},
                    {%- for key, value in this.options.items() %}
                    {{ key }}: {{ value|tojson }},
                    {%- endfor %}
                }
            );
            {{ this.get_name() }}.locate({
                               setView: true
                        });

            {%- if this.control_scale %}
            L.control.scale().addTo({{ this.get_name() }});
            {%- endif %}

            {% if this.objects_to_stay_in_front %}
            function objects_in_front() {
                {%- for obj in this.objects_to_stay_in_front %}
                    {{ obj.get_name() }}.bringToFront();
                {%- endfor %}
            };
            {{ this.get_name() }}.on("overlayadd", objects_in_front);
            $(document).ready(objects_in_front);
            {%- endif %}

        {% endmacro %}
        """)
    default_js = [
    ('leaflet',
     'https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.min.js'),
    ('jquery',
     'https://code.jquery.com/jquery-1.12.4.min.js'),
    ('bootstrap',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
    ('awesome_markers',
     '/static/leaflet.awesome-markers/dist/leaflet.awesome-markers.js'),  # noqa
    ]
    default_css = [
    ('leaflet_css',
     'https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.min.css'),
    ('bootstrap_css',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'),
    ('bootstrap_theme_css',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css'),  # noqa
    # ('awesome_markers_font_css',
    #  'https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css'),  # noqa
    ('awesome_markers_font_css',
     '/static/fontawesome/css/all.css'),
    ('myicon',
     '/static/myicon/style.css'),
    ('awesome_markers_css',
     '/static/leaflet.awesome-markers/dist/leaflet.awesome-markers.css'),  # noqa
    ('awesome_rotate_css',
     'https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css'),  # noqa
    ]
    def __init__(
            self,
            location=None,
            width='100%',
            height='100%',
            left='0%',
            top='0%',
            position='relative',
            display='block',
            tiles='OpenStreetMap',
            attr=None,
            min_zoom=0,
            max_zoom=18,
            zoom_start=10,
            min_lat=-90,
            max_lat=90,
            min_lon=-180,
            max_lon=180,
            max_bounds=False,
            crs='EPSG3857',
            control_scale=False,
            prefer_canvas=False,
            no_touch=False,
            disable_3d=False,
            png_enabled=False,
            zoom_control=True,
            **kwargs
    ):
        super(OSM_Map, self).__init__(
            location=location,
            width=width,
            height=height,
            left=left,
            top=top,
            position=position,
            tiles=tiles,
            attr=attr,
            min_zoom=min_zoom,
            max_zoom=max_zoom,
            zoom_start=zoom_start,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            max_bounds=max_bounds,
            crs=crs,
            control_scale=control_scale,
            prefer_canvas=prefer_canvas,
            no_touch=no_touch,
            disable_3d=disable_3d,
            png_enabled=png_enabled,
            zoom_control=zoom_control,
            **kwargs
    )
        self._name = 'OSM_Map'
        self.display=display
        OSM_Application().add_child(self)

    def _repr_html_(self, **kwargs):
        """Displays the HTML Map in a Jupyter notebook."""
        if self._parent is None:
            self.add_to(OSM_Application())
            out = self._parent._repr_html_(**kwargs)
            self._parent = None
        else:
            out = self._parent._repr_html_(**kwargs)
        return out


class OSM_Layer(Function_Element):
    _template = Template(u"""
                {% macro script(this, kwargs) %}
                 var {{this.get_name()}} = L.layerGroup().addTo({{this._parent.get_name()}});
                 {{this.get_name()}}['type']='{{this.type}}';
                 let configuration = {{ this.configuration|tojson|safe }};
                 {{this.get_name()}}['configuration']=configuration;
                 
                 {{this.get_name()}}['configuration']['name']='{{this._name}}';
                 
                 {{this.get_name()}}['configuration']['ipBase']='{{this.ipBase}}';
                 {{this.get_name()}}['configuration']['ip6Base']='{{this.ip6Base}}';
                 {{this.get_name()}}['configuration']['macColonHex']='{{this.macColonHex(this.nextIP,6)}}';
                 
  
                 {{this.get_name()}}['ipv4']={ipBaseNum:{{this.ipBaseNum}},prefixLen:{{this.prefixLen}},nextIP:{{this.nextIP}}};
                 {{this.get_name()}}['ipv6']={ip6BaseNum:{{this.ip6BaseNum}},prefixLen6:{{this.prefixLen6}},nextIP6:{{this.nextIP6}}};
                 {{this.get_name()}}['mac']={nextAddress:{{this.nextIP}}};
                 {{this.get_name()}}['allocateIP']=function (){
                        let i=this['ipv4'].nextIP;
                        let prefixLen=this['ipv4'].prefixLen;
                        let ipBaseNum=this['ipv4'].ipBaseNum;
                        let imax = 0xffffffff >>> prefixLen;
                        if(i > imax)
                         {
                            alert('Not enough IP addresses in the subnet')
                            return;
                         }
                        let mask = 0xffffffff ^ imax;
                        let ipnum = ( ipBaseNum & mask ) + i;
                        this['ipv4']['nextIP']=this['ipv4']['nextIP']+1;
                        return this.ipStr( ipnum )+`/${prefixLen}`;
                      }
                {{this.get_name()}}['ipStr'] = function (ip){
                      let w = ( ip >>> 24 ) & 0xff;
                      let x = ( ip >>> 16 ) & 0xff;
                      let y = ( ip >>> 8 ) & 0xff;
                      let z = ip & 0xff;
                return `${w}.${x}.${y}.${z}`;
                      }
             {{this.get_name()}}['allocateIP6']=function (){
                        let i=BigInt(this['ipv6'].nextIP6);
                        let prefixLen=BigInt(this['ipv6'].prefixLen6);
                        let ipBaseNum=BigInt(this['ipv6'].ip6BaseNum);
                        let MAX_128 = BigInt(0xffffffffffffffffffffffffffffffff)-1n;
                        let ipv6_max = MAX_128 >> prefixLen;
                        if(i>ipv6_max)
                        {
                        alert('Not enough IPv6 addresses in the subnet');
                        return;
                        }
                        let mask = MAX_128 ^ ipv6_max;
                        let ipnum = ( ipBaseNum & mask ) + i;
                        this['ipv6']['nextIP6']=this['ipv6']['nextIP6']+1;
                        return this.ip6Str( ipnum )+`/${prefixLen}`;
                      }
                      
            {{this.get_name()}}['ip6Str'] = function (ip){
                               let b = BigInt(0xffff);
                               let x1 = (ip >> 112n) & b;
                               let x2 = (ip >> 96n) & b;
                               let x3 = (ip >> 80n) & b;
                               let x4 = (ip >> 64n) & b;
                               let x5 = (ip >> 48n) & b;
                               let x6 = (ip >> 32n) & b;
                               let x7 = (ip >> 16n) & b;
                               let x8 = ip & b;
            return `${x1}:${x2}:${x3}:${x4}:${x5}:${x6}:${x7}:${x8}`;
                      }
                      
            {{this.get_name()}}['allocateMAC']=function (bytecount=6){
            let mac= BigInt(this['mac'].nextAddress);
            let pieces = [];
            for(let i=BigInt(bytecount-1);i>=0;i=i-BigInt(1))
            {
                 let piece = ((BigInt(0xff) << (i * BigInt(8))) & mac) >> (i * BigInt(8));
                 let num=(Array(2).join(0) + piece.toString(16)).slice(-2);
                 pieces.push(num);
            }
            let chStr = pieces.join(":"); 
            this['mac'].nextAddress = BigInt(this['mac'].nextAddress) + BigInt(1);
            // this['configuration']['macColonHex'] = chStr;
            return chStr;
            }
            
        {{this.get_name()}}['netParse'] = function(ipstr)
        {
        let prefixLen = 0;
        let ip=0;
        if(ipstr.indexOf('/')!=-1)
        {
            let str = ipstr.split('/');
                ip= str[0];
            let pf= str[1];
            prefixLen = parseInt(pf);
        }
        else
        {
            ip = ipstr;
            prefixLen = 24;
        }
        let args=[];
        ip.split('.').forEach(function(value)
        {
        args.push(parseInt(value));
        }
        );
        while(args.length<4)
        {
        args.push(0);
        }
        let ipBaseNum= (args[0] << 24)|(args[1] << 16)|(args[2] << 8)|(args[3]);
        let nextIP = (0xffffffff >>> prefixLen) & ipBaseNum;
        nextIP = nextIP > 0 ? nextIP : 1;
        return {'ipBaseNum':ipBaseNum,'prefixLen':prefixLen,'nextIP':nextIP};
        }
        
        {{this.get_name()}}['netParse6'] = function(ipstr)
        {
        let prefixLen6 = 0;
        let ip=0;
        if(ipstr.indexOf('/')!=-1)
        {
            let str = ipstr.split('/');
                ip= str[0];
            let pf= str[1];
            prefixLen6 = parseInt(pf);
        }
        else
        {
            ip = ipstr;
            prefixLen6 = 24;
        }
        let args=[];
        ip.split(':').forEach(function(value)
        {
        args.push(BigInt(value));
        }
        );
        while(args.length<8)
        {
        args.push(BigInt(0));
        }
        let ip6BaseNum= (args[0] << BigInt(112))|(args[1] << BigInt(96))|(args[2] << BigInt(80))|(args[3] << BigInt(64))|(args[4] << BigInt(48))|(args[5] << BigInt(32))|(args[6] << BigInt(16))|(args[7]);
        let nextIP6 = 1;
        return {'ip6BaseNum':ip6BaseNum,'prefixLen6':prefixLen6,'nextIP6':nextIP6};
        }
        
        {{this.get_name()}}['macParse'] = function(macstr)
        {
        let args=[];
        macstr.split(':').forEach(function(value)
        {
        args.push(BigInt(value));
        }
        );
        let nextAddress = BigInt(0);
        for (let i = 0; i < args.length; i++) {
        nextAddress = nextAddress | (args[i] << BigInt((args.length-i-1)*8));
                   } 
        return {'nextAddress':nextAddress};
        }
        {{this.get_name()}}['calculateXYZ']=function(center={{this.get_MapName()}}.getCenter(),point)
                     {
                     let x_lng=  L.latLng(center.lat,point.lng);
                     let y_lat = L.latLng(point.lat, center.lng);
                     let coord_x= point.lng > center.lng ? center.distanceTo(x_lng) : 0 - center.distanceTo(x_lng);
                     let coord_y= point.lat > center.lat ? center.distanceTo(y_lat) : 0 - center.distanceTo(y_lat);
                     return [Math.round(coord_x),Math.round(coord_y),0];
                     }
                {% endmacro %}
                """)  # noqa

    def __init__(self,ipBase='10.0.0.0/8',ip6Base='2001:0:0:0:0:0:0:0/64',configuration={},name='OSM_Layer'):
        super(OSM_Layer, self).__init__()
        self._name = name
        self.type = name
        self.ipBase=ipBase
        self.ipBaseNum, self.prefixLen = self.netParse(self.ipBase)
        hostIP = (0xffffffff >> self.prefixLen) & self.ipBaseNum
        self.nextIP = hostIP if hostIP > 0 else 1

        self.ip6Base = ip6Base
        self.ip6BaseNum, self.prefixLen6 = self.netParse6(self.ip6Base)
        self.nextIP6 = 1  # start for address allocation

        self.configuration=configuration


        # self.mp_range=mp_range
        # self.wifi_range=wifi_range
        # self.ec_range=ec_range
        #
        # self.bw=bw
        # self.delay=delay
        # self.jitter=jitter
        # self.loss=loss

    def netParse(self,ipstr):
        """Parse an IP network specification, returning
           address and prefix len as unsigned ints"""
        prefixLen = 0
        if '/' in ipstr:
            ip, pf = ipstr.split('/')
            prefixLen = int(pf)
        # if no prefix is specified, set the prefix to 24
        else:
            ip = ipstr
            prefixLen = 24
        return self.ipParse(ip), prefixLen

    def netParse6(self,ipstr):
        """Parse an IP network specification, returning
           address and prefix len as unsigned ints"""
        prefixLen = 0
        if '/' in ipstr:
            ip, pf = ipstr.split('/')
            prefixLen = int(pf)
        # if no prefix is specified, set the prefix to 24
        else:
            ip = ipstr
            prefixLen = 24
        return self.ip6Parse(ip), prefixLen

    def ipParse(self,ip):
        "Parse an IP address and return an unsigned int."
        args = [int(arg) for arg in ip.split('.')]
        while len(args) < 4:
            args.insert(len(args) - 1, 0)
        return self.ipNum(*args)

    def ip6Parse(self,ip):
        "Parse an IP address and return an unsigned int."
        args = [int(arg) for arg in ip.split(':')]
        while len(args) < 8:
            args.append(0)
        return self.ip6Num(*args)

    def ipNum(self,w, x, y, z):
        """Generate unsigned int from components of IP address
           returns: w << 24 | x << 16 | y << 8 | z"""
        return (w << 24) | (x << 16) | (y << 8) | z

    def ip6Num(self,x1, x2, x3, x4, x5, x6, x7, x8):
        "Generate unsigned int from components of IP address"
        return (x1 << 112) | (x2 << 96) | (x3 << 80) | (x4 << 64) | (x5 << 48) | (x6 << 32) | (x7 << 16) | x8

    def macColonHex(self,mac,bytecount):
        pieces = []
        for i in range(bytecount - 1, -1, -1):
            piece = ((0xff << (i * 8)) & mac) >> (i * 8)
            pieces.append('%02x' % piece)
        chStr = ':'.join(pieces)
        return chStr

    def setConfiguration(self,configuration=None):
        if configuration:
            self.configuration=configuration

Global_Network_Configuration_Layer = OSM_Layer
# o=OSM_Layer(ipBase='10.0.0.1/8')
# print(o.ipBaseNum,o.prefixLen6,o.nextIP6)
# print(o.macColonHex(255,6))
# print(o.ipParse('10.0.0.1'))
# print(o.netParse6('2001:0:0:0:0:0:0:0/64'))
# print(o.ip6Parse('2001:0:0:0:0:0:0:0'))
