from OSM_Map.OSM_Menu import Menu,MenuButton,MenuForm,Input_For_Form,Button_For_Form
from OSM_Map.OSM_Event_Handler import OSM_Anonymous_Event_Handler
from jinja2 import Template

class Top_Menu(Menu):

    def build(self,map):
        form = MenuForm(action=r'/geocode/')
        Input_For_Form(labelName='地理位置：', name='location',width='80%').add_to(form)
        Button_For_Form(buttonName="提交").add_to(form)
        SubmitEvent_For_MenuForm(map=map).add_to(form)
        form.add_to(self)

class SubmitEvent_For_MenuForm(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                    function(e){
                        e.preventDefault();
                        let data = $(this).serialize();
                        
                        $.ajax({
                                type: 'POST',
                                url:  e.target.action,
                                data: data,
                                dataType: "json",
                                encode: true,
                                success: function (data) {
                                        {{this.map.get_name()}}.setView(data.location);
                                        e.target.reset();
                                           }
                                });
                            }
                """)

    def __init__(self,map):
        super(SubmitEvent_For_MenuForm, self).__init__()
        self._name = 'SubmitEvent_For_MenuForm'
        self.event_type = 'submit'
        self.map=map