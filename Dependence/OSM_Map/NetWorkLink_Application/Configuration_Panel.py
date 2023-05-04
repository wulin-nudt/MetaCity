from OSM_Map.OSM_Configuration_Menu import Configuration_Panel,MouseDownEvent_For_ConfigurePanel,ResetEvent_For_ConfigurationPanel,SubmitEvent_For_ConfigurationPanel
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from OSM_Map.OSM_HTML_BaseElement import Input_For_Form,Button_For_Form
from jinja2 import Template

class NetWorkLink_Configuration_Panel(Configuration_Panel):

    def build(self,NetWorkLink):
        self.add_content(Input_For_Form(labelName='网络链接名称：', name='name', readonly=True))
        self.add_content(Input_For_Form(labelName='源点：', name='node1'))
        self.add_content(Input_For_Form(labelName='目点：', name='node2'))
        self.add_content(Input_For_Form(labelName='带宽：', name='bw'))
        self.add_content(Input_For_Form(labelName='延迟：', name='delay'))
        self.add_content(Input_For_Form(labelName='延迟抖动：', name='jitter'))
        self.add_content(Input_For_Form(labelName='丢包率：', name='loss'))

        self.add_content(Button_For_Form(buttonName="保存"))
        self.add_content(ResetEvent_For_ConfigurationPanel())
        self.add_content(SubmitEvent_For_ConfigurationPanel())

        MouseDownEvent_For_ConfigurePanel().add_to(self)
        # SubmitEvent_For_MenuForm(map=map).add_to(self)