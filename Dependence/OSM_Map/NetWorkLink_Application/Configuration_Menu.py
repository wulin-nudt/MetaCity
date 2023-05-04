from OSM_Map.OSM_Configuration_Menu import Configuration_Menu,ClickEvent_For_CancelOption,ClickEvent_For_ConfigureOption
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.NetWorkLink_Application.Configuration_Panel import NetWorkLink_Configuration_Panel
from jinja2 import Template

class NetWorkLink_Configuration_Menu(Configuration_Menu):

    def build(self):
        op1=  self.add_option('配置')
        op2 = self.add_option('删除')
        op3 = self.add_option('取消')

        cp=NetWorkLink_Configuration_Panel(width='60%',padding='10px').add_to(op1)
        cp.build(self._parent)
        ClickEvent_For_ConfigureOption(self,cp).add_to(op1)

        ClickEvent_For_DeleteOption(self).add_to(op2)
        ClickEvent_For_CancelOption(self).add_to(op3)

class ClickEvent_For_DeleteOption(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 let link=$('#{{this.configuration_menu.get_name()}}')[0]['belong'];
                  {{ this._parent.get_LayerName() or this._parent.get_MapName() }}.removeLayer(link);
                            let i=link['origin']['links'].indexOf(link);
                            link['origin']['links'].splice(i, 1);
                            i=link['destination']['links'].indexOf(link);
                            link['destination']['links'].splice(i, 1);
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: none;`);
                }
                """)

    def __init__(self,configuration_menu):
        super(ClickEvent_For_DeleteOption, self).__init__()
        self._name = 'ClickEvent_For_DeleteOption'
        self.event_type = 'click'
        self.configuration_menu=configuration_menu
