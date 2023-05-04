from OSM_Map.OSM_Configuration_Menu import Configuration_Panel,MouseDownEvent_For_ConfigurePanel,ResetEvent_For_ConfigurationPanel,SubmitEvent_For_ConfigurationPanel
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.OSM_HTML_BaseElement import Input_For_Form,Button_For_Form,Tabs
from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from jinja2 import Template

class Edge_Cloud_Configuration_Panel(Configuration_Panel):

    def build(self,EdgeCloud):
        tab = Tabs(tabs_items=['网络基础设置', 'CPU资源设置','系统设置'])

        tab.add_child(Input_For_Form(labelName='节点名称：', name='name',readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='地理坐标位置：', name='location',readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='平面XY坐标：', name='position', readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='IPV4地址：', name='ip',auto_option=True,readonly=True,checked=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='IPV6地址：', name='ip6',auto_option=True,readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='MAC地址：', name='mac',auto_option=True,readonly=True),tab_num=1)
        tab.add_child(Input_For_Form(labelName='信号接收范围：', name=EdgeCloud.type+'_range'),tab_num=1)

        tab.add_child(Input_For_Form(labelName='cpu带宽(us)：', name=EdgeCloud.type+'_cpu_period',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='cpu配额(us)：', name=EdgeCloud.type+'_cpu_quota',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='cpu份额相对值：', name=EdgeCloud.type+'_cpu_shares',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='物理内存：', name=EdgeCloud.type+'_mem_limit',required=False), tab_num=2)
        tab.add_child(Input_For_Form(labelName='虚拟内存：', name=EdgeCloud.type+'_memswap_limit',required=False), tab_num=2)

        tab.add_child(Input_For_Form(labelName='操作系统镜像：', name=EdgeCloud.type+'_dimage'), tab_num=3)
        tab.add_child(Input_For_Form(labelName='系统内核参数：', name=EdgeCloud.type+'_sysctls'), tab_num=3)

        self.add_content(tab)

        self.add_content(Button_For_Form(buttonName="保存"))
        self.add_content(ResetEvent_For_ConfigurationPanel())
        self.add_content(SubmitEvent_For_ConfigurationPanel())

        MouseDownEvent_For_ConfigurePanel().add_to(self)