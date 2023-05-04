from OSM_Map.OSM_Menu import Menu,MenuButton
from OSM_Map.Menu_Application.Configuration_Panel import Global_Network_Configuration_Panel
from OSM_Map.OSM_Event_Handler import OSM_Anonymous_Event_Handler,OSM_Event_Handler
from branca.element import (Element, Figure, JavascriptLink, MacroElement,Html)
from jinja2 import Template

class Right_Menu(Menu):

    def build(self,map,entity={}):

        bn4 = MenuButton(buttonName='全局设置').add_to(self)
        if entity.get('Global_Network_Configuration_Layer', None):
            gncp=Global_Network_Configuration_Panel(width='60%',padding='10px').add_to(bn4)
            gncp.build(entity)
            Global_Network_Configuration_Control(entity.get('Global_Network_Configuration_Layer'),gncp).add_to(bn4)

        bn = MenuButton(buttonName='移动点').add_to(self)
        if entity.get('Moving_Point',None):
            MovingPointControl(entity.get('Moving_Point')).add_to(bn)

        bn1 = MenuButton(buttonName='wifi点').add_to(self)
        if entity.get('Wireless_Access_Point', None):
            WirelessAccessPointControl(entity.get('Wireless_Access_Point')).add_to(bn1)

        bn2 = MenuButton(buttonName='边缘云').add_to(self)
        if entity.get('Edge_Cloud', None):
            EdgeCloudPointControl(entity.get('Edge_Cloud')).add_to(bn2)

        bn6 = MenuButton(buttonName='基站').add_to(self)
        if entity.get('Base_Station', None):
            BaseStationPointControl(entity.get('Base_Station')).add_to(bn6)

        bn3 = MenuButton(buttonName='网络链接').add_to(self)
        if entity.get('NetWorkLink', None):
            NetWorkLinkControl(entity.get('NetWorkLink')).add_to(bn3)

        bn5 = MenuButton(buttonName='重置网络拓扑').add_to(self)
        if entity.get('Global_Network_Configuration_Layer', None):
            ReSetControl(entity.get('Global_Network_Configuration_Layer')).add_to(bn5)

        ClickEvent_For_Menu().add_to(self)
        MoveEndEvent_For_Map().add_to(map)


class Global_Network_Configuration_Control(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function (e)
                {
                this['stateless']=true;
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);
                
                $('#shade_{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: 0px; top: 0px; height:${document.documentElement.scrollHeight}px`);

                let width = $('#{{this.configuration_panel.get_name()}}')[0].offsetWidth;
                let x = e.originalEvent.pageX;
                if(x  > document.documentElement.offsetWidth - width) {
                    x = document.documentElement.offsetWidth - width;
                }
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${x}px; top: ${e.originalEvent.pageY}px;`);
                
                let network_configuration_layer= {{this.global_network_configuration_layer.get_name()}};
                $('#{{this.configuration_panel.get_name()}}')[0]['belong']=network_configuration_layer;
                
                let form_item=$('#{{this.configuration_panel.get_name()}}').children("form").find('input,select');
                $.each(form_item, function() {
                             let value = network_configuration_layer[this.name] ? network_configuration_layer[this.name] : network_configuration_layer['configuration'][this.name];
                             if(typeof(value)!='undefined')
                             {
                             if(this.type=='checkbox')
                             {
                             $(this).prop("checked", JSON.parse(value));
                             }
                             else
                             {
                             this.value = value;
                             }
                             }
                             else
                             {
                             if(this.type=='checkbox')
                             {
                             $(this).prop("checked", true);
                             }
                             else
                             {
                                    if(this.type=='text')
                                    {
                                        this.value='';
                                    }
                                    else if(this.tagName=='SELECT')
                                    {       
                                           $(this).find("option").eq(0).prop("selected",true);
                                    }
                             }
                             }
                             layui.form.render();
                                });
                }
                """)

    def __init__(self, global_network_configuration_layer,configuration_panel):
        super(Global_Network_Configuration_Control, self).__init__()
        self._name = 'Global_Network_Configuration_Control'
        self.event_type = 'click'
        self.global_network_configuration_layer = global_network_configuration_layer
        self.configuration_panel=configuration_panel

class MovingPointControl(OSM_Anonymous_Event_Handler):
    _template = Template(u"""

                function (e)
                {
                if(this['state'])
                {
                this['state']=false;
                this.className = "layui-btn layui-btn-lg layui-btn-radius layui-btn-normal";
                {{this.MovingPoint.get_MapName()}}.off('click',{{this.MovingPoint.get_name()}});
                {{this.MovingPoint._parent.get_name()}}['Moving_Point_Layer'] = undefined;
                }
                else
                {
                this['state']=true;
                this.className = "layui-btn layui-btn-lg layui-btn-radius layui-btn-disabled";
                {{this.MovingPoint.get_MapName()}}.on('click',{{this.MovingPoint.get_name()}});
                {{this.MovingPoint._parent.get_name()}}['Moving_Point_Layer'] = undefined;
                }
                }
                """)

    def __init__(self, MovingPoint):
        super(MovingPointControl, self).__init__()
        self._name = 'MovingPointControl'
        self.event_type = 'click'
        self.MovingPoint = MovingPoint

WirelessAccessPointControl = MovingPointControl
EdgeCloudPointControl = MovingPointControl
BaseStationPointControl = MovingPointControl

class NetWorkLinkControl(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function (e)
                {
                if(this['state'])
                {
                this['state']=false;
                this.className = "layui-btn layui-btn-lg layui-btn-radius layui-btn-normal";
                {{this.NetWorkLink.get_MapName()}}.off('click',{{this.NetWorkLink.get_name()}});
                function unbindLink(layer){
                                    layer.off('click',{{this.NetWorkLink.get_name()}})
                                    if(layer['tmp_popup']){
                                    layer.bindPopup(layer['tmp_popup']);
                                    }
                                    if(layer.dragging)
                                    {
                                    layer.dragging.enable();
                                    }
                                    if(layer.eachLayer)
                                    {
                                    layer.eachLayer(unbindLink);
                                    }
                }
                {{this.NetWorkLink.get_LayerName()}}.eachLayer(unbindLink);
                }
                else
                {
                this['state']=true;
                this.className = "layui-btn layui-btn-lg layui-btn-radius layui-btn-disabled";
                {{this.NetWorkLink.get_MapName()}}.on('click',{{this.NetWorkLink.get_name()}});
                function bindLink(layer){
                                    //alert( {{this.NetWorkLink.get_LayerName()}}.getLayers());
                                    // alert(layer['type']);
                                    let p;
                                    p=layer.getPopup();
                                    layer.unbindPopup();
                                    layer['tmp_popup']=p;
                                    if(layer.dragging)
                                    {
                                    layer.dragging.disable();
                                    }
                                   if(layer['type']!='{{this.NetWorkLink._name}}')
                                    {
                                    layer.on('click',{{this.NetWorkLink.get_name()}});
                                    }
                                    if(layer.eachLayer)
                                    {
                                    layer.eachLayer(bindLink);
                                    }      
                }
                {{this.NetWorkLink.get_LayerName()}}.eachLayer(bindLink);
                }
                }
                """)

    def __init__(self, NetWorkLink):
        super(NetWorkLinkControl, self).__init__()
        self._name = 'NetWorkLinkControl'
        self.event_type = 'click'
        self.NetWorkLink = NetWorkLink

class ClickEvent_For_Menu(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                         function(e){
                           if(!this['former']&& e.target.nodeName=='BUTTON' && !e.target['stateless'])
                           {
                            this['former']=e.target;
                           }
                           else if(e.target.nodeName=='BUTTON' && !e.target['stateless'])
                           {
                             if(e.target!=this['former'])
                             {
                             this['former'].click();
                             this['former']=e.target;
                             }
                             else
                             {
                             this['former']=undefined;
                             }
                           }
                            }
                """)

    def __init__(self):
        super(ClickEvent_For_Menu, self).__init__()
        self._name = 'ClickEvent_For_Menu'
        self.event_type = 'click'

class ReSetControl(OSM_Anonymous_Event_Handler):
    _template = Template(u"""

                function (e)
                {
                this['stateless']=true;
                var judge=layer.confirm('Removes the Network Topology ？',{icon:7,title:'tips'},function()
                {
                {{this.global_network_configuration_layer.get_name()}}.clearLayers();
                layer.close(layer.index);
                }
                );
                }
                """)

    def __init__(self, global_network_configuration_layer):
        super(ReSetControl, self).__init__()
        self._name = 'ReSetControl'
        self.event_type = 'click'
        self.global_network_configuration_layer = global_network_configuration_layer

class MoveEndEvent_For_Map(MacroElement):
    _template = Template(u'''
                {% macro script(this, kwargs) %}
                {{this._parent.get_name()}}.on('moveend',function (e){
                  function update_position(layer)
                  {
                  if(layer.getXYZ)
                  {
                  if(layer['Moving_Point_Layer'])
                  {
                 layer['location']=[layer.getLatLng().lat,layer.getLatLng().lng].toString();
                 layer['position']=layer.getXYZ().toString();
                 let order = layer['order'];
                 layer['Moving_Point_Layer']['configuration']['positions'][order-1] = layer['position'];
                 layer['Moving_Point_Layer']['configuration']['location'][order-1] = layer['location'];
                 layer['Moving_Point_Layer']['configuration']['position']=layer['Moving_Point_Layer']['configuration']['positions'][0];
                 if(layer['Moving_Point_Layer']['configuration']['routes'])
                 {
                 layer['Moving_Point_Layer']['configuration']['coord']=layer['Moving_Point_Layer'].routesToCoord(layer['Moving_Point_Layer']['configuration']['routes']);
                 }
                  }
                  else
                  {
                 layer['configuration']['location']=[layer.getLatLng().lat,layer.getLatLng().lng];
                 layer['configuration']['position']=layer.getXYZ();
                  }
                  }
                  if(layer.eachLayer)
                  {
                  layer.eachLayer(update_position);
                  }
                  }
                this.eachLayer(update_position);
                });
                {% endmacro %}
    ''')
    def __init__(self):
        super(MoveEndEvent_For_Map, self).__init__()
        self._name='MoveEndEvent_For_Map'