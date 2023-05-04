from OSM_Map.OSM_Event_Handler import OSM_Anonymous_Event_Handler,OSM_Event_Handler
from jinja2 import Template

class ContextmenuEvent_For_MovingPointMarker(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);
                 $('#{{this.configuration_menu.get_name()}}')[0]['belong']=e.target;
                }
                """)

    def __init__(self,configuration_menu):
        super(ContextmenuEvent_For_MovingPointMarker, self).__init__()
        self._name = 'ContextmenuEvent_For_MovingPointMarker'
        self.event_type = 'contextmenu'
        self.configuration_menu=configuration_menu

class MoveEvent_For_MovingPointMarker(OSM_Anonymous_Event_Handler):
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
                 point['location']=[point.getLatLng().lat,point.getLatLng().lng].toString();
                 point['position']=point.getXYZ().toString();
                 let order = point['order'];
                 point['Moving_Point_Layer']['configuration']['positions'][order-1] = point['position'];
                 point['Moving_Point_Layer']['configuration']['location'][order-1] = point['location'];
                 point['Moving_Point_Layer']['configuration']['position'] =  point['Moving_Point_Layer']['configuration']['positions'][0];
                 point['Moving_Point_Layer']['route'].clearLayers();
                 point['Moving_Point_Layer']['configuration']['coord']=undefined;
                 point['Moving_Point_Layer']['configuration']['routes']=undefined;
                 point['Moving_Point_Layer']['configuration']['routes_distance']=0;
                            }
                """)

    def __init__(self):
        super(MoveEvent_For_MovingPointMarker, self).__init__()
        self._name = 'MoveEvent_For_MovingPointMarker'
        self.event_type = 'move'

class QoSPanelInitEvent_For_MovingPointMarker(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                   let point = e.target;
                   if(!point['configuration']['QoS']['status'])
                   {
                   point.closePopup();
                   let datas={'filename':[],'aggregation':5};
                   let filename=[];
                   if(point['configuration']['QoS_Sources'])
                   {
                   point['configuration']['QoS_Sources'].forEach(
                   function(file)
                   {
                   if(file.status=='success')
                   {
                   filename.push(file.filename)
                   }
                   }
                   );
                   }
                   datas['filename']=filename;
                   let key = point['type']+'_aggregation';
                   datas['aggregation']= point['configuration'][key] ? point['configuration'][key] : datas['aggregation'];
                   if(filename.length)
                   {
                    $.ajax({
                    type: 'POST',
                    url:  {{this.url}},
                    data: JSON.stringify(datas),
                    contentType: 'application/json',
                    dataType: "json",
                    encode: true,
                    success: function (data) 
                     {
                     if(data["state"]=='success')
                     {
                     let name = point['configuration']['name'];
                     data["statistics"].forEach(
                     function(statistic)
                     {
                     chart=statistic.chart;
                     if(chart[name])
                     {
                     for(index in chart[name])
                     {
                        if(point['configuration']['QoS'][index])
                        {
                        point['configuration']['QoS'][index]['data'][statistic.filename]=chart[name][index];
                        // alert(point['configuration']['QoS'][index]['data'][statistic.filename]['description'])
                        }
                     }
                     }
                     });
                point['configuration']['QoS']['status']=true;
                let vegadata = point['configuration']['QoS'];
                for (index in vegadata)
                {
                if(vegadata[index].data)
                {  
                  let n=filename.at(-1);
                  if(vegadata[index].data[n])
                  {
                  vegaEmbed(vegadata[index].div,vegadata[index].data[n]);
                  vegadata[index].bind=true;
                  }
                  else
                  {
                  vegaEmbed(vegadata[index].div,{});
                  vegadata[index].bind=false;
                  }
                }
                }
                setTimeout(function(){
                point.openPopup();
                }, 1);
                // let p = point.getPopup();
                // alert(p.getContent().innerHTML);
                // point.unbindPopup();
                // let popup_content=$(point.getPopup().getContent()).parents('.leaflet-popup');
                // popup_content.remove();
                // point.bindPopup(p);
                // point.fire('click');
                // alert("test");
                //let popup_content=$(point.getPopup().getContent()).parents('.leaflet-popup-content');
                //popup_content.width('500');
                // popup_content.height('400');
                }
                else
                {
                    alert("仿真并未运行结束,暂时并未有可视化结果，请稍后重新加载");
                }
                }
                });
                }
                else
                {
                  alert("目前没有任何仿真程序正在运行,因此没有任何可视化结果");
                }
                // let point = {{this._parent.get_name()}};
                // alert(point['configuration']['QoS_Sources']);
                }
                else
                {
                let vegadata = point['configuration']['QoS'];
                let popup_li = $(point.getPopup().getContent()).find('.layui-tab-title > li');
                // let show_li = $(point.getPopup().getContent()).find('.layui-tab-title > li.layui-this');
                let popup_div = $(point.getPopup().getContent()).find('.layui-tab-content .layui-tab-item');
                // let show_div = $(point.getPopup().getContent()).find('.layui-tab-content .layui-tab-item.layui-show');
                let auto_show = undefined;
                let reset=false;
                for (index in vegadata)
                {
                if(vegadata[index].bind)
                {  
                  if(!auto_show)
                  {
                  auto_show=$(vegadata[index].div).parent();
                  }
                }
                else
                {
                  let tt=$(vegadata[index].div).parent();
                  if(tt.hasClass('layui-show'))
                  {
                  tt.removeClass('layui-show');
                  let i = popup_div.index(tt);
                  popup_li.eq(i).removeClass('layui-this');
                  reset=true;
                  }
                }
                }
                if(reset && auto_show)
                {
                  point.closePopup();
                  auto_show.addClass('layui-show');
                  let i = popup_div.index(auto_show);
                  popup_li.eq(i).addClass('layui-this');
                  setTimeout(function(){
                      point.openPopup();
                       }, 1);
                }
                }
                
                }
                """)

    def __init__(self,url):
        super(QoSPanelInitEvent_For_MovingPointMarker, self).__init__()
        self._name = 'QoSPanelInitEvent_For_MovingPointMarker'
        self.event_type = 'popupopen'
        self.url=url


class TestEvent_For_MovingPointMarker(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                alert("test");
                }
                """)

    def __init__(self):
        super(TestEvent_For_MovingPointMarker, self).__init__()
        self._name = 'TestEvent_For_MovingPointMarker'
        self.event_type = 'popupclose'