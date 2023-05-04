from OSM_Map.OSM_Configuration_Menu import Configuration_Menu,ClickEvent_For_CancelOption,ClickEvent_For_ConfigureOption
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.Moving_Point_Application.Configuration_Panel import Moving_Point_Configuration_Panel
from jinja2 import Template

class Moving_Point_Configuration_Menu(Configuration_Menu):

    def build(self):
        op1=  self.add_option('配置')
        op4 = self.add_option('添加新移动点')
        op2 = self.add_option('删除')
        op3 = self.add_option('取消')

        cp=Moving_Point_Configuration_Panel(width='60%',padding='10px').add_to(op1)
        cp.build(self._parent)
        ClickEvent_For_ConfigureOption(self,cp).add_to(op1)
        ClickEvent_For_DeleteOption(self).add_to(op2)
        ClickEvent_For_CancelOption(self).add_to(op3)
        ClickEvent_For_AddOption(self,self._parent).add_to(op4)

class ClickEvent_For_DeleteOption(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 let point=$('#{{this.configuration_menu.get_name()}}')[0]['belong'];
                 
                point['Moving_Point_Layer'].removeLayer(point);
                
                let order=point['Moving_Point_Layer']['configuration']['location'].indexOf(point['location']);

                point['Moving_Point_Layer']['configuration']['location'].splice(order, 1);
                point['Moving_Point_Layer']['configuration']['positions'].splice(order, 1);
                
                point['Moving_Point_Layer'].eachLayer(function(layer)
                          {
                          layer['order']=this['configuration']['location'].indexOf(layer['location'])+1;
                          },
                          point['Moving_Point_Layer']
                          );
                if(point['Moving_Point_Layer'].getLayers().length<=1)
                   {
                   {{ this._parent.get_LayerName() or this._parent.get_MapName() }}.removeLayer(point['Moving_Point_Layer']);
                   }
                   else
                   {
                   point['Moving_Point_Layer']['configuration']['position'] = point['Moving_Point_Layer']['configuration']['positions'][0];
                   }
                
                         point['links'].forEach(function(link)
                            {
                            let other_point = (link['origin']==point) ? link['destination'] : link['origin'];
                            let i=other_point['links'].indexOf(link);
                            other_point['links'].splice(i, 1);
                            {{ this._parent.get_LayerName() or this._parent.get_MapName() }}.removeLayer(link['link']);
                            }
                            );
                            
                point['Moving_Point_Layer']['route'].clearLayers();
                point['Moving_Point_Layer']['configuration']['coord']=undefined;
                point['Moving_Point_Layer']['configuration']['routes']=undefined;
                point['Moving_Point_Layer']['configuration']['routes_distance']=0;
                
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: none;`);
                }
                """)

    def __init__(self,configuration_menu):
        super(ClickEvent_For_DeleteOption, self).__init__()
        self._name = 'ClickEvent_For_DeleteOption'
        self.event_type = 'click'
        self.configuration_menu=configuration_menu


class ClickEvent_For_AddOption(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 let point=$('#{{this.configuration_menu.get_name()}}')[0]['belong'];
                 {{ this._parent.get_LayerName() or this._parent.get_MapName() }}['Moving_Point_Layer']=point['Moving_Point_Layer'];
                 {{this.MovingPoint.get_MapName()}}.on('click',{{this.MovingPoint.get_name()}});
                 let fix= {{this.MovingPoint.get_MapName()}}.getZoom()**6;
                 let x_abs = Math.random() < 0.5 ? -1 : 1; 
                 let y_abs = Math.random() < 0.5 ? -1 : 1; 
                 let x_r = (1 + Math.random())*fix*x_abs;
                 let y_r=  (1 + Math.random())*fix*y_abs;
                 let point_latlng = L.latLng(point.getLatLng().lat+15000/x_r, point.getLatLng().lng+15000/y_r);
                 {{this.MovingPoint.get_MapName()}}.fire('click',
                 {
                 latlng:point_latlng
                 }
                 );
                 {{this.MovingPoint.get_MapName()}}.off('click',{{this.MovingPoint.get_name()}});
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: none;`);
                }
                """)

    def __init__(self, configuration_menu,MovingPoint):
        super(ClickEvent_For_AddOption, self).__init__()
        self._name = 'ClickEvent_For_AddOption'
        self.event_type = 'click'
        self.configuration_menu = configuration_menu
        self.MovingPoint=MovingPoint