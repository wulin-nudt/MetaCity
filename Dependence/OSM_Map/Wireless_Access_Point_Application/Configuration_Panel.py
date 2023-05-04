from OSM_Map.OSM_Configuration_Menu import Configuration_Panel,MouseDownEvent_For_ConfigurePanel,ResetEvent_For_ConfigurationPanel
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.OSM_HTML_BaseElement import Input_For_Form,Button_For_Form,Select_For_Form
from jinja2 import Template

class Wireless_Access_Point_Configuration_Panel(Configuration_Panel):

    def build(self,WirelessAccessPoint):
        self.add_content(Input_For_Form(labelName='节点名称：', name='name',readonly=True))
        self.add_content(Input_For_Form(labelName='地理坐标位置：', name='location',readonly=True))
        self.add_content(Input_For_Form(labelName='平面XY坐标：', name='position', readonly=True))
        self.add_content(Input_For_Form(labelName='ssid：', name='ssid'))
        self.add_content(Input_For_Form(labelName='IPV4地址：', name='ip',auto_option=True,readonly=True,checked=True))
        self.add_content(Input_For_Form(labelName='IPV6地址：', name='ip6',auto_option=True,readonly=True))
        self.add_content(Input_For_Form(labelName='MAC地址：', name='mac',auto_option=True,readonly=True))
        self.add_content(Select_For_Form(labelName="故障模式:", name=WirelessAccessPoint.type + '_failMode',options=[{"standalone": 'standalone', 'secure': 'secure'}], width="50%"))
        self.add_content(Input_For_Form(labelName='信号接收范围：', name=WirelessAccessPoint.type + '_range'))

        self.add_content(Button_For_Form(buttonName="保存"))
        self.add_content(ResetEvent_For_ConfigurationPanel())
        self.add_content(SubmitEvent_For_ConfigurationPanel(WirelessAccessPoint=WirelessAccessPoint))

        MouseDownEvent_For_ConfigurePanel().add_to(self)

class SubmitEvent_For_ConfigurationPanel(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                    function(e){
                    e.preventDefault();
                    let point=$(this).parent().slice(-1)[0]['belong'];
                    let items = $(this).find('input,select');
                    var judge=layer.confirm('IS ReSet？',{icon:7,title:'tips'},function()
                    {
                    $.each(items, function(){
                        if(this.name)
                         {
                           if(point[this.name])
                           {
                           point[this.name]=this.value;
                           }
                           else
                           {
                           point['configuration'][this.name]=this.value;
                           }
                          }
                            });
                    point['signal_range'].setRadius(point['configuration']['{{this.wap_type}}'+'_range']);
                    layer.close(layer.index);
                    }
                    );
                                }
                """)

    def __init__(self,WirelessAccessPoint):
        super(SubmitEvent_For_ConfigurationPanel, self).__init__()
        self._name = 'SubmitEvent_For_ConfigurationPanel'
        self.event_type = 'submit'
        self.wap_type=WirelessAccessPoint.type