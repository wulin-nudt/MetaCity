import warnings
from OSM_Map.OSM_HTML_BaseElement import UL,LI,HTML_BaseElement,HTML_InnerElement,\
    Form
from OSM_Map.OSM_Event_Handler import OSM_Event_Handler,OSM_Anonymous_Event_Handler
from jinja2 import Template

class Configuration_Menu(HTML_BaseElement):
    _template = Template(u"""
            {% macro header(this, kwargs) %}
            <style>
                #{{this.get_name()}} {
                    position: absolute;
	                display: none;
	                z-index: 999;
                                    }
                                    
			#{{this.get_name()}} ul{
				background-color: white;
				color: #B0C0C7;
				width: 150px;
				position: absolute;
				padding: 10px;
				box-shadow: 0px 0px 5px black;
				border-radius: 10px;
			}
			#{{this.get_name()}} li{
				list-style: none;
				line-height: 40px;
			}
			#{{this.get_name()}} li:hover{
				color: white;
				background-color: darkgrey;
			}
		</style>
            {% endmacro %}
                    
                    
                   {% macro html(this, kwargs) %}
                   <div id='{{this.get_name()}}'>
                    <ul id='{{this.menu.get_name()}}'>
                    {% for name, element in this.menu.html._children.items() %}
                    {{element.render()}}
                    {% endfor %}
                    </ul>
                    </div>
                    {% endmacro %}
                    
                    {% macro script(this, kwargs) %}
                    {% for k,v in this.menu._event.items() %}
                        {% for v1 in v %}
                        $('#{{this.menu.get_name()}}').on('{{k}}',{{v1}});
                        {% endfor %}
                    {% endfor %}
                    
                    {{this._parent.get_MapName()}}.on('click',function(e){ 
                        $('#{{this.get_name()}}').attr("style",`display: none;`);
                        }
                     )
                    {% endmacro %}
                    """)  # noqa

    def __init__(self):
        super(Configuration_Menu, self).__init__()
        self._name = 'Configuration_Menu'
        self.menu=UL()
        self.menu.menuname=self.get_name()
        self._children=self.menu._children
        self.menu._parent=self
        #self.add_child(self.menu)

    def add_option(self,option,name=None, index=None):
        op=None
        if isinstance(option,str):
            op=LI(content=option)
            self.menu.add_child(op,name=name, index=index)
        else:
            self.menu.add_child(option,name=name, index=index)
            op=option
        return op

    def add_child(self, child, name=None, index=None):
        warnings.warn('Method `add_child` is deprecated. Please use `add_option` instead.',
                      FutureWarning, stacklevel=2)
        return self.add_option(child, name=name, index=index)

class ClickEvent_For_CancelOption(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                 $('#{{this.configuration_menu.get_name()}}').attr("style",`display: none;`);
                }
                """)

    def __init__(self,configuration_menu):
        super(ClickEvent_For_CancelOption, self).__init__()
        self._name = 'ClickEvent_For_CancelOption'
        self.event_type = 'click'
        self.configuration_menu=configuration_menu


class ClickEvent_For_ConfigureOption(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                function(e){
                $('#{{this.configuration_menu.get_name()}}').attr("style",`display: none;`);


                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${e.originalEvent.pageX}px; top: ${e.originalEvent.pageY}px;`);
                
                $('#shade_{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: 0px; top: 0px; height:${document.documentElement.scrollHeight}px`);

                let width = $('#{{this.configuration_panel.get_name()}}')[0].offsetWidth;
                let x = e.originalEvent.pageX;
                if(x  > document.documentElement.offsetWidth - width) {
                    x = document.documentElement.offsetWidth - width;
                }
                $('#{{this.configuration_panel.get_name()}}').attr("style",`display: block; left: ${x}px; top: ${e.originalEvent.pageY}px;`);

                 let point = $('#{{this.configuration_menu.get_name()}}')[0]['belong'];
                 $('#{{this.configuration_panel.get_name()}}')[0]['belong']=point;

                 
                 let form_item=$('#{{this.configuration_panel.get_name()}}').children("form").find('input,select');
                 $.each(form_item, function() {
                             let value = point[this.name] ? point[this.name] : point['configuration'][this.name];
                             // let value = point['configuration'][this.name] ? point['configuration'][this.name] : point[this.name];
                             if(typeof(value)!='undefined')
                             {
                             // let value = point[this.name] ? point[this.name] : point['configuration'][this.name];
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

    def __init__(self, configuration_menu, configuration_panel):
        super(ClickEvent_For_ConfigureOption, self).__init__()
        self._name = 'ClickEvent_For_ConfigureOption'
        self.event_type = 'click'
        self.configuration_menu = configuration_menu
        self.configuration_panel = configuration_panel

class Configuration_Panel(HTML_BaseElement):
    _template = Template(u"""
            {% macro header(this, kwargs) %}
              <style>
                #{{this.get_name()}} {
                    position: absolute;
	                display: none;
	                z-index: 999;
	                background-color: white;
	                width: {{this.width}};
                    height: {{this.height}};
                    margin:{{this.margin}};
                    padding:{{this.padding}};
                    }
            
            #{{this.get_name()}} i.layui-icon-close {
             font-size: 30px; 
             color: black; 
             float:right; 
             margin:10px;
			                     }
			                     
            #{{this.get_name()}} i.layui-icon-close:hover {
				color: white;
				background-color: darkgrey;
			}
			
		#shade_{{this.get_name()}} {
            display: none;
            position: absolute;
            width: 100%;
            background-color: rgba(0, 0, 0, .3);
            z-index: 500;
          }
		      </style>
            {% endmacro %}
                    
                    
                   {% macro html(this, kwargs) %}
                   
                   <div id="shade_{{this.get_name()}}"></div>
                   
                   <div id='{{this.get_name()}}'>
                   <div style="margin-bottom:30px">
                   <i class="layui-icon layui-icon-close" onclick="document.getElementById('{{this.get_name()}}').style.display='none'; document.getElementById('shade_{{this.get_name()}}').style.display='none';" ></i> 
                   </div>
                   <form id="{{this.panel.get_name()}}" class="layui-form" action="{{this.panel.action}}" method="{{this.panel.method}}" >
                    {% for name, element in this.panel.html._children.items() %}
                        {{element.render()}}
                    {% endfor %}
                    </form>
                    </div>
                    {% endmacro %}
                    
                    {% macro script(this, kwargs) %}
                    {% for k,v in this.panel._event.items() %}
                        {% for v1 in v %}
                        $('#{{this.panel.get_name()}}').on('{{k}}',{{v1}});
                        {% endfor %}
                    {% endfor %}
                    
                    {% for k,v in this._event.items() %}
                        {% for v1 in v %}
                        $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                        {% endfor %}
                    {% endfor %}
                    {% endmacro %}
                    """)  # noqa

    def __init__(self,width='fit-content',height='fit-content',margin='0',padding='0'):
        super(Configuration_Panel, self).__init__()
        self._name = 'Configuration_Panel'
        self.width=width
        self.height=height
        self.margin=margin
        self.padding=padding
        self.panel = Form(action=None)
        self.panel.panelname = self.get_name()
        self._children=self.panel._children
        self.panel._parent=self


    def add_content(self,content,name=None, index=None):
        if isinstance(content,(HTML_BaseElement,OSM_Event_Handler,OSM_Anonymous_Event_Handler)):
            content.add_to(self.panel,name=name, index=index)
            # self.panel.add_child(content,name=name, index=index)
        else:
            raise Exception("the type of /' content /' object is error ")
        return self


class MouseDownEvent_For_ConfigurePanel(OSM_Anonymous_Event_Handler):
    _template = Template(u"""

     function(e ) {
    var panel = this;
    var x1 = e.offsetX ;
    var y1 = e.offsetY;

        document.onmousemove = function() {

        // 获取鼠标在浏览器中的位置 - 每个事件都有自己独特的事件对象
        var e = window.event;
        var x2 = e.pageX;
        var y2 = e.pageY;

        // 计算left和top
        var l = x2 - x1
        var t = y2 - y1

        // 设置不能超出左上角和右上角
        if(l < 0) {
            l = 0
        }
        if(t < 0) {
            t = 0
        }
          // 设置left和top的最大值 不能超过事件源本身

        if(t > document.documentElement.scrollHeight - panel.offsetHeight) {
            t = document.documentElement.scrollHeight - panel.offsetHeight;
        }
        if(l > document.documentElement.offsetWidth - panel.offsetWidth) {
            l = document.documentElement.offsetWidth - panel.offsetWidth;
        }

        // 设置div的left和top
        panel.style.left = l + 'px'
        panel.style.top = t + 'px'
    };

    document.onmouseup = function(){
                        document.onmousemove = null;
                        document.onmouseup = null;
                    };
    }

                """)

    def __init__(self):
        super(MouseDownEvent_For_ConfigurePanel, self).__init__()
        self._name = 'MouseDownEvent_For_ConfigurePanel'
        self.event_type = 'mousedown'

class ResetEvent_For_ConfigurationPanel(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                    function(e){
                       let point=$(this).parent().slice(-1)[0]['belong'];
                       let form_item=$(this).find('input,select');
                       e.preventDefault();
                       var judge=layer.confirm('IS ReSet？',{icon:7,title:'tips'},function()
                       {
                             $.each(form_item, function() {
                             let value = point[this.name] ? point[this.name] : point['configuration'][this.name];
                             let autoflag = point['Auto_Configuration_'+this.name] ? point['Auto_Configuration_'+this.name] : point['configuration']['Auto_Configuration_'+this.name];
                             // let value = point['configuration'][this.name] ? point['configuration'][this.name] : point[this.name];
                             if(typeof(value)!='undefined')
                             {
                             if(this.type=='checkbox')
                             {
                             $(this).prop("checked", JSON.parse(value));
                             }
                             else
                             {
                             this.value = value;
                             if(value&&autoflag)
                             {
                             this.setAttribute("readOnly", true);
                             }
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
                            layer.close(layer.index);
                       }
                       );
                                }
                """)

    def __init__(self):
        super(ResetEvent_For_ConfigurationPanel, self).__init__()
        self._name = 'ResetEvent_For_ConfigurationPanel'
        self.event_type = 'reset'

class SubmitEvent_For_ConfigurationPanel(OSM_Anonymous_Event_Handler):
    _template = Template(u"""
                    function(e){
                    e.preventDefault();
                    let point=$(this).parent().slice(-1)[0]['belong'];
                    let items = $(this).find('input,select');
                    var judge=layer.confirm('IS SAVE？',{icon:7,title:'tips'},function()
                    {
                    $.each(items, function(){
                         if(this.name)
                         {
                            let v=this.value;
                            if(this.type=='checkbox')
                            {
                            v=$(this).prop("checked");
                            }
                           if(point[this.name])
                           {
                           point[this.name]=v;
                           }
                           else
                           {
                           point['configuration'][this.name]=v;
                            // alert(this.name);
                           // alert(v);
                           }
                          }
                            });
                    layer.close(layer.index);
                    }
                    );
                                }
                """)

    def __init__(self):
        super(SubmitEvent_For_ConfigurationPanel, self).__init__()
        self._name = 'SubmitEvent_For_ConfigurationPanel'
        self.event_type = 'submit'