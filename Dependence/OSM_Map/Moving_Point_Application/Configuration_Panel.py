from OSM_Map.OSM_Configuration_Menu import Configuration_Panel,MouseDownEvent_For_ConfigurePanel,ResetEvent_For_ConfigurationPanel,SubmitEvent_For_ConfigurationPanel
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.OSM_HTML_BaseElement import Input_For_Form,Button_For_Form,Tabs,Select,Select_For_Form
from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from jinja2 import Template

class Moving_Point_Configuration_Panel(Configuration_Panel):

    def build(self,MovingPoint):
        tab = Tabs(tabs_items=['网络基础设置', 'CPU资源设置','系统设置','仿真测试'])

        tab.add_child(Input_For_Form(labelName='节点名称：', name='name',readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='次序：', name='order', readonly=True), tab_num=1)
        tab.add_child(Input_For_Form(labelName='地理坐标位置：', name='location',readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='驻留点XY坐标：', name='position', readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='IPV4地址：', name='ip',auto_option=True,readonly=True,checked=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='IPV6地址：', name='ip6',auto_option=True,readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='MAC地址：', name='mac',auto_option=True,readonly=True),tab_num=1)
        tab.add_child(Select_For_Form(labelName="移动道路类型:", name=MovingPoint.type + '_network_type',options=[{'drive': 'drive'},{'walk': 'walk'}], width="30%",margin='0px 0px 0px 50px'), tab_num=1)
        tab.add_child(Input_For_Form(labelName='信号接收范围：', name=MovingPoint.type+'_range'),tab_num=1)
        tab.add_child(Input_For_Form(labelName='移动速度：', name='speed'),tab_num=1)

        tab.add_child(Input_For_Form(labelName='cpu带宽(us)：', name=MovingPoint.type+'_cpu_period',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='cpu配额(us)：', name=MovingPoint.type+'_cpu_quota',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='cpu份额相对值：', name=MovingPoint.type+'_cpu_shares',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='物理内存：', name=MovingPoint.type+'_mem_limit',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='虚拟内存：', name=MovingPoint.type+'_memswap_limit',required=False), tab_num=2)

        tab.add_child(Input_For_Form(labelName='操作系统镜像：', name=MovingPoint.type+'_dimage'), tab_num=3)
        tab.add_child(Input_For_Form(labelName='系统内核参数：', name=MovingPoint.type+'_sysctls'), tab_num=3)

        tab.add_child(Input_For_Form(labelName='延迟测试：', name=MovingPoint.type + '_delayTest',required=False), tab_num=4)
        tab.add_child(Input_For_Form(labelName='丢包率测试：', name=MovingPoint.type + '_packetLossTest',required=False), tab_num=4)
        tab.add_child(Input_For_Form(labelName='带宽测试：', name=MovingPoint.type + '_bandWidthTest', required=False),tab_num=4)
        input1=Input_For_Form(labelName='仿真实验方式：', name=MovingPoint.type + '_emulation', required=False, width='40%',placeholder='请输入数值，不设置默认为10')
        Select(name=MovingPoint.type + '_emulationWays', required=False,options=[{'period':'s'},{'times':'times'}],width='10%').add_to(input1)
        tab.add_child(input1,tab_num=4)
        tab.add_child(Select_For_Form(labelName="仿真结果数据聚集程度:",name=MovingPoint.type + '_aggregation',options=[{'1':'1'},{'5':'5'},{'10':'10'},{'20':'20'}],width="30%",margin='0px 0px 0px 100px'),tab_num=4)

        # tab.add_child(Input_For_Select(labelName='', name=MovingPoint.type + '_ways', required=False,options=['ss','44'],width='10%'), tab_num=4)


        self.add_content(tab)

        self.add_content(Button_For_Form(buttonName="保存"))
        self.add_content(ResetEvent_For_ConfigurationPanel())
        self.add_content(SubmitEvent_For_ConfigurationPanel())

        MouseDownEvent_For_ConfigurePanel().add_to(self)
        # SubmitEvent_For_MenuForm(map=map).add_to(self)
