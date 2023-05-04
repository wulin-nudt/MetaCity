from OSM_Map.OSM_Menu import Menu,MenuButton
from OSM_Map.OSM_HTML_BaseElement import ShadeDiv,LayuiIcon
from OSM_Map.OSM_Event_Handler import OSM_Anonymous_Event_Handler,OSM_Event_Handler
from OSM_Map.Menu_Application.Configuration_Panel import EmulationTest_Configuration_Panel,Emulation_Configuration_Panel
from jinja2 import Template

class Bottom_Menu(Menu):

    def build(self,global_network_configuration_layer,entity={}):

        Data_Filter={}
        Moving_Point_Data={}
        Edge_Cloud_Data={}
        Wireless_Access_Point_Data={}
        Base_Station_Data = {}
        NetWorkLink_Data={}
        if entity.get('Moving_Point',None):
            Moving_Point_Data = {
            entity.get('Moving_Point').type: [{'source':['configuration'],'dataitems':['name', 'location', 'position','ip', 'ip6', 'mac', 'range', 'speed',
                                    'cpu_period', 'cpu_quota', 'cpu_shares', 'mem_limit',
                                    'memswap_limit','dimage','sysctls',{'NodeMobilityConfig':['speed','coord','distance/routes_distance']},{'EmulationConfig':{'localconfig':['delay/delayTest','packet_loss/packetLossTest','band_width/bandWidthTest'],'globalconfig':{'emulationWay':['key/emulationWays','value/emulation']}}}]}]}

        if entity.get('Edge_Cloud', None):
            Edge_Cloud_Data = {
            entity.get('Edge_Cloud').type: [{'source':['configuration'],'dataitems':['name', 'location', 'position', 'ip', 'ip6', 'mac', 'range', 'speed',
                                    'cpu_period', 'cpu_quota', 'cpu_shares', 'mem_limit',
                                    'memswap_limit','dimage','sysctls']}]}

        if entity.get('Wireless_Access_Point', None):
            Wireless_Access_Point_Data = {
            entity.get('Wireless_Access_Point').type:[{'source':['configuration'],'dataitems': ['name', 'location', 'position','ssid', 'ip', 'ip6', 'mac', 'range','failMode']}]}

        if entity.get('Base_Station', None):
            Base_Station_Data = {
            entity.get('Base_Station').type:[{'source':['configuration'],'dataitems': ['name', 'location', 'position','ssid', 'ip', 'ip6', 'mac', 'range','failMode']}]}

        if entity.get('NetWorkLink', None):
            NetWorkLink_Data = {
            entity.get('NetWorkLink').type: [{'source':['configuration'],'dataitems':['node1', 'node2','delay', 'bw','jitter', 'loss']}]}

        global_network_configuration_layer_Data={global_network_configuration_layer.type:[{'source':['configuration','EmulationConfiguration'],
                                                                                           'dataitems':[
                                                                                               {'MobilityConfig':['mobility_start_time','mobility_stop_time','reverse','ac_method','mob_rep','mobility_mode']},
                                                                                               {'SDNControllerConfig':['controller/SDN_Controller','name/Controller_Name','number/Controller_Number','ip/Controller_IP','port/Controller_Port','protocol/Controller_Protocol','app/Network_Application']}
                                                                                           ]}]}
        Data_Filter.update(Moving_Point_Data)
        Data_Filter.update(Edge_Cloud_Data)
        Data_Filter.update(Wireless_Access_Point_Data)
        Data_Filter.update(Base_Station_Data)
        Data_Filter.update(NetWorkLink_Data)
        Data_Filter.update(global_network_configuration_layer_Data)

        bn1=MenuButton(buttonName='移动点路径规划', row=1, col=1).add_to(self)
        sd1=ShadeDiv().add_to(bn1)
        LayuiIcon(iconName='layui-icon-loading',fontContent='移动点路径规划中',fontSize='30px',fontColor='red').add_to(sd1)
        UploadRouteControl(global_network_configuration_layer, data_filter={entity.get('Moving_Point').type:[{'source':['configuration'],'dataitems':['location','routes_distance','network_type','routes_type']}]}, url='/generate_routes/').add_to(bn1)

        bn3=MenuButton(buttonName='仿真测试', row=1, col=4).add_to(self)
        etcp=EmulationTest_Configuration_Panel(width='70%',padding='10px').add_to(bn3)
        etcp.build(global_network_configuration_layer)
        EmulationTest_Configuration_Control(configuration_panel=etcp).add_to(bn3)

        bn4=MenuButton(buttonName='仿真实验预配置', row=1, col=2).add_to(self)
        ecp=Emulation_Configuration_Panel(width='70%',padding='10px').add_to(bn4)
        ecp.build(global_network_configuration_layer)
        Emulation_Configuration_Control(configuration_panel=ecp,layer=global_network_configuration_layer).add_to(bn4)

        bn2=MenuButton(buttonName='上传网络拓扑数据', row=1, col=3).add_to(self)
        sd2=ShadeDiv().add_to(bn2)
        LayuiIcon(iconName='layui-icon-loading',fontContent='正在上传',fontSize='30px',fontColor='red').add_to(sd2)
        UploadNetworkTopologControl(global_network_configuration_layer, Data_Filter, url='/network_topolog/',ecp_table=etcp.table).add_to(bn2)





class UploadNetworkTopologControl(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function (e)
                {
                let data_filter = {{ this.data_filter|tojson|safe }};
                let network_Topology={};
                function obtain_Value(value,layer,type)
                    {
                        let v1 = typeof(layer[value])!= "undefined" ? layer[value] : layer[type+'_'+value];
                        if(typeof(v1)=='string' && v1.at(0)=='{' && v1.at(-1)=='}')
                        {
                        v1 = JSON.parse(v1);
                        }
                        else if(!isNaN(Number(v1)))
                        {
                        
                            if(typeof(v1)=='string' && v1.length==0)
                            {
                            v1=undefined;
                            }
                            else
                            {
                            v1=Number(v1);
                            }
                        }
                        return v1;
                    }
                function obtain_configuration(network_Topology,value,layer,type)
                    {
                        if(typeof(value)=='string')
                        {
                            let alias = value.split('/');
                            let data=obtain_Value(alias.at(-1),layer,type);
                                if(typeof(data)!= "undefined")
                                {
                                    network_Topology[alias[0]]=data;
                                }
                        }
                        else if(Array.isArray(value))
                        {   
                            for(let i=0;i<value.length;i++)
                            {
                                obtain_configuration(network_Topology,value[i],layer,type);
                            }
                        }
                        else if(Object.prototype.toString.call(value) === '[object Object]')
                        {
                            for(n in value)
                            {
                                network_Topology[n]={};
                                obtain_configuration(network_Topology[n],value[n],layer,type);
                            }
                        }
                    }
                function collect_configuration(layer,data_filter,network_Topology){
                    let type=layer['type'];
                    if(type && data_filter[type] && layer['configuration'])
                    {
                        let name = layer['configuration']['name'];
                        if(name)
                        {
                            network_Topology[name]={};
                            network_Topology[name]['type']=type;
                            
                            data_filter[type].forEach(function(collection)
                            {
                            let layer_source=layer;
                            for(let se of collection['source']) 
                                {
                                    if(layer_source[se])
                                    {
                                        layer_source=layer_source[se];
                                    }
                                    else
                                    {
                                        break;
                                    }
                                }
                            collection['dataitems'].forEach(
                                function(value)
                                {
                                    obtain_configuration(network_Topology[name],value,layer_source,type);
                                });
                            });
                        }
                    }
                }
                    
                {{this.layer.get_name()}}.getLayers().forEach(function(layer)
                {
                collect_configuration(layer,data_filter,network_Topology);
                });
                
                collect_configuration({{this.layer.get_name()}},data_filter,network_Topology);
                
                var judge=layer.confirm('IS Upload The Data of Network Topology ？',{icon:7,title:'tips'},function()
                {
                $('#shade_{{this._parent.get_name()}}').attr("style",`display: flex; left: 0px; top: 0px; height:${document.documentElement.scrollHeight}px`);
                $.ajax({
                    type: 'POST',
                    url:  {{this.url}},
                    data: JSON.stringify(network_Topology),
                    contentType: 'application/json',
                    dataType: "json",
                    encode: true,
                    success: function (data) {
                    if(data["state"]=='success')
                    {
                    $('#shade_{{this._parent.get_name()}}').attr("style",`display: none;`);
                    data['network_topology'].forEach(function(value)
                    {
                    $('#{{this.ecp_table.get_name()}} tbody').prepend(`<tr><td>${value['filename']}</td><td>${value['date']}</td></tr>`);
                    });
                    let table = layui.table;
                    table.init('{{this.ecp_table.get_name()}}', {
                             height: {{this.ecp_table.height}}
                             ,limit: {{this.ecp_table.limit}}
                             ,page: {'limit':{{this.ecp_table.limit}},'limits':[{{this.ecp_table.limit}},2*{{this.ecp_table.limit}}]}
                   });
                    alert("上传成功");
                    }
                    else
                    {
                    $('#shade_{{this._parent.get_name()}}').attr("style",`display: none;`);
                    alert("上传失败");
                    }
                       }
                    });
                layer.close(layer.index);
                }
                );
                }
                """)

    def __init__(self,layer,data_filter,url,**kwargs):
        super(UploadNetworkTopologControl, self).__init__()
        self._name = 'UploadNetworkTopologControl'
        self.event_type = 'click'
        self.layer=layer
        self.data_filter=data_filter
        self.url=url
        self.ecp_table=kwargs.get('ecp_table',None)

class UploadRouteControl(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function (e)
                {
                let data_filter = {{ this.data_filter|tojson|safe }};
                let routes={};
                let nameToLayer={};
                let center={{this.layer.get_MapName()}}.getCenter();
                //let locationToCoord={};
                function obtain_Value(value,layer,type)
                    {
                        let v1 = typeof(layer[value])!= "undefined" ? layer[value] : layer[type+'_'+value];
                        return v1;
                    }
                function obtain_configuration(network_Topology,value,layer,type)
                    {
                        if(typeof(value)=='string')
                        {
                            let alias = value.split('/');
                            let data=obtain_Value(alias.at(-1),layer,type);
                                if(typeof(data)!= "undefined")
                                {
                                    network_Topology[alias[0]]=data;
                                }
                        }
                        else if(Array.isArray(value))
                        {   
                            for(let i=0;i<value.length;i++)
                            {
                                obtain_configuration(network_Topology,value[i],layer,type);
                            }
                        }
                        else if(Object.prototype.toString.call(value) === '[object Object]')
                        {
                            for(n in value)
                            {
                                network_Topology[n]={};
                                obtain_configuration(network_Topology[n],value[n],layer,type);
                            }
                        }
                    }
                function collect_configuration(layer,data_filter,routes,nameToLayer){
                    let type=layer['type'];
                    if(type && data_filter[type] && layer['configuration'])
                    {
                        let name = layer['configuration']['name'];
                        if(name)
                        {   
                            routes[name]={};
                            nameToLayer[name]=layer;
                            data_filter[type].forEach(function(collection)
                            {
                            let layer_source=layer;
                            for(let se of collection['source']) 
                                {
                                    if(layer_source[se])
                                    {
                                        layer_source=layer_source[se];
                                    }
                                    else
                                    {
                                        break;
                                    }
                                }
                            collection['dataitems'].forEach(
                                function(value)
                                {
                                    obtain_configuration(routes[name],value,layer_source,type);
                                });
                            });
                        }
                    }
                }
                    
                {{this.layer.get_name()}}.getLayers().forEach(function(layer)
                {
                collect_configuration(layer,data_filter,routes,nameToLayer);
                });
                
                collect_configuration({{this.layer.get_name()}},data_filter,routes,nameToLayer);
                
                /*{{this.layer.get_name()}}.eachLayer(function(layer){
                                    // text=text + " " + layer.getLatLng();
                                    let type=layer['type'];
                                    if(type && data_filter[type] && layer['configuration'])
                                    {
                                    let name = layer['configuration']['name'];
                                    if(name)
                                    {
                                    routes[name]={};
                                    nameToLayer[name]=layer;
                                    data_filter[type].forEach(
                                    function(value)
                                    {
                                        function obtain_Value(value)
                                        {
                                           let v1 = typeof(layer['configuration'][value])!= "undefined" ? layer['configuration'][value] : layer['configuration'][type+'_'+value];
                                            return v1;
                                        }
                                        function obtain_configuration(routes,value)
                                        {
                                            if(typeof(value)=='string')
                                            {   
                                                let alias = value.split('/');
                                                let data=obtain_Value(alias.at(-1));
                                                if(data)
                                                {
                                                    routes[alias[0]]=data;
                                                }
                                            }
                                            else if(Array.isArray(value))
                                            {   
                                                for(let i=0;i<value.length;i++)
                                                {
                                                 obtain_configuration(routes,value[i]);
                                                }
                                            }
                                            else if(Object.prototype.toString.call(value) === '[object Object]')
                                            {
                                                for(n in value)
                                                {
                                                    routes[n]={};
                                                    obtain_configuration(routes[n],value[n]);
                                                }
                                            }
                                        }
                                        obtain_configuration(routes[name],value);
                                    }
                                    );
                                    }
                                    }
                                    }
                );*/
                var judge=layer.confirm('IS Upload The Data of Moving Point ？',{icon:7,title:'tips'},function()
                {
                $('#shade_{{this._parent.get_name()}}').attr("style",`display: flex; left: 0px; top: 0px; height:${document.documentElement.scrollHeight}px`);
                $.ajax({
                    type: 'POST',
                    url:  {{this.url}},
                    data: JSON.stringify(routes),
                    contentType: 'application/json',
                    dataType: "json",
                    encode: true,
                    success: function (data) {
                    if(data["Exception"])
                    {
                    $('#shade_{{this._parent.get_name()}}').attr("style",`display: none;`);
                    alert("寻找路径失败,请重新尝试，错误代码:"+data["Exception"].toString());
                    }
                    else if(data["state"]=='success')
                    {
                    data["routes"].forEach(function(mp)
                    {
                    let edge_color=['#006400','#EE82EE','#0000FF','#00FFFF','#F0FFF0'];
                    n=mp['name'];
                    let route_layer=undefined;
                    let moving_point = nameToLayer[n];
                    if(moving_point && moving_point['configuration'])
                    {
                    route_layer=moving_point['route'];
                    moving_point['configuration']['routes']=[];
                    moving_point['configuration']['coord']=[];
                    moving_point['configuration']['routes_distance']=0;
                    if(typeof (moving_point['configuration']['routes_type']) != 'undefined')
                    {
                    if(mp['type']!=moving_point['configuration']['routes_type'])
                    {
                    route_layer.clearLayers();
                    }
                    }
                    moving_point['configuration']['routes_type']=mp['type'];
                    }
                    else
                    {
                    route_layer={{this.layer.get_name()}};
                    }
                    let distance=0;
                    mp['route'].forEach(function(point,index)
                    {
                    point.forEach(function(edge){
                    let route =  L.polyline(edge,{color:edge_color[index%5]}).addTo(route_layer);
                    edge.forEach(function(e){
                        let xyz={{this.layer.get_name()}}.calculateXYZ(center,L.latLng(e));
                        if(moving_point && moving_point['configuration'] && moving_point['configuration']['coord'].at(-1)!=xyz.toString())
                        {
                        moving_point['configuration']['coord'].push(xyz.toString());
                        if(moving_point['configuration']['routes'].length>0)
                        {
                        distance=distance + L.latLng(e).distanceTo(L.latLng(moving_point['configuration']['routes'].at(-1)));
                        // alert(e.toString()+","+moving_point['configuration']['routes'].at(-1).toString());
                        moving_point['configuration']['routes_distance']=distance;
                        }
                        moving_point['configuration']['routes'].push(e);
                        }
                         });
                    });
                    });
                    // alert(n);
                    });
                    $('#shade_{{this._parent.get_name()}}').attr("style",`display: none;`);
                    alert("上传成功");
                    }
                    else
                    {
                    $('#shade_{{this._parent.get_name()}}').attr("style",`display: none;`);
                    alert("上传失败");
                    }
                       }
                    });
                layer.close(layer.index);
                }
                );
                }
                """)

    def __init__(self,layer,data_filter,url):
        super(UploadRouteControl, self).__init__()
        self._name = 'UploadRouteControl'
        self.event_type = 'click'
        self.layer=layer
        self.data_filter=data_filter
        self.url=url


class EmulationTest_Configuration_Control(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function (e)
                {
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);


                let width = $('#{{this.configuration_panel.get_name()}}')[0].offsetWidth;
                let x = e.originalEvent.pageX;
                if(x  > document.documentElement.offsetWidth - width) {
                    x = document.documentElement.offsetWidth - width;
                }
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${x}px; top: ${e.originalEvent.pageY-500}px;`);
                $('#shade_{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: 0px; top: 0px; height:${document.documentElement.scrollHeight}px`);
                }
                """)

    def __init__(self,configuration_panel):
        super(EmulationTest_Configuration_Control, self).__init__()
        self._name = 'EmulationTest_Configuration_Control'
        self.event_type = 'click'
        self.configuration_panel = configuration_panel

class Emulation_Configuration_Control(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function (e)
                {
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);


                let width = $('#{{this.configuration_panel.get_name()}}')[0].offsetWidth;
                let x = e.originalEvent.pageX;
                if(x  > document.documentElement.offsetWidth - width) {
                    x = document.documentElement.offsetWidth - width;
                }
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${x}px; top: ${e.originalEvent.pageY-500}px;`);
                $('#shade_{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: 0px; top: 0px; height:${document.documentElement.scrollHeight}px`);
                
                let configuration_layer= {{this.layer.get_name()}};
                let form_item=$('#{{this.configuration_panel.get_name()}}').children("form").find('input,select');
                let EmulationConfiguration = configuration_layer['configuration']['EmulationConfiguration'];
                $.each(form_item, function() {
                             let value = EmulationConfiguration[this.name];
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

    def __init__(self,configuration_panel,layer):
        super(Emulation_Configuration_Control, self).__init__()
        self._name = 'Emulation_Configuration_Control'
        self.event_type = 'click'
        self.configuration_panel = configuration_panel
        self.layer=layer