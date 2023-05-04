from OSM_Map.OSM_Configuration_Menu import Configuration_Menu,ClickEvent_For_CancelOption,ClickEvent_For_ConfigureOption
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.Edge_Cloud_Application.Configuration_Panel import Edge_Cloud_Configuration_Panel
from jinja2 import Template

class Edge_Cloud_Configuration_Menu(Configuration_Menu):

    def build(self):
        op1=  self.add_option('配置')
        op2 = self.add_option('删除')
        op3 = self.add_option('取消')

        cp=Edge_Cloud_Configuration_Panel(width='60%',padding='10px').add_to(op1)
        cp.build(self._parent)
        ClickEvent_For_ConfigureOption(self,cp).add_to(op1)
        ClickEvent_For_DeleteOption(self).add_to(op2)
        ClickEvent_For_CancelOption(self).add_to(op3)

class ClickEvent_For_DeleteOption(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 let point=$('#{{this.configuration_menu.get_name()}}')[0]['belong'];
                {{ this._parent.get_LayerName() or this._parent.get_MapName() }}.removeLayer(point);
                         point['links'].forEach(function(link)
                            {
                            let other_point = (link['origin']==point) ? link['destination'] : link['origin'];
                            let i=other_point['links'].indexOf(link);
                            other_point['links'].splice(i, 1);
                            {{ this._parent.get_LayerName() or this._parent.get_MapName() }}.removeLayer(link['link']);
                            }
                            );
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: none;`);
                }
                """)

    def __init__(self,configuration_menu):
        super(ClickEvent_For_DeleteOption, self).__init__()
        self._name = 'ClickEvent_For_DeleteOption'
        self.event_type = 'click'
        self.configuration_menu=configuration_menu