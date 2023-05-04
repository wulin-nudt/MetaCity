from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from jinja2 import Template
import folium
from folium.utilities import _parse_size
from OSM_Map.OSM_Folium_Element import OSM_Layer

class HTML_BaseElement(MacroElement):
    _template = Template(u"""
                    {% macro html(this, kwargs) %}
                     <div id='{{this.get_name()}}'>
                     {% for name, element in this.html._children.items() %}
                        {{element.render()}}
                     {% endfor %}
                     </div>
                    {% endmacro %}
                    
                    {% macro script(this, kwargs) %}
                    {% for k,v in this._event.items() %}
                        {% for v1 in v %}
                        $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                        {% endfor %}
                    {% endfor %}
                    {% endmacro %}
                    """)  # noqa
    def __init__(self):
        super(HTML_BaseElement, self).__init__()
        self._name = 'HTML_BaseElement'
        self._event={'click':[],'mouseover':[],'mouseout':[],'submit':[],'mousedown':[],'reset':[]}

        self.html = Element()
        self.html._parent = self

    def render(self, **kwargs):

        for name, element in self._children.items():
            element.render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        header = self._template.module.__dict__.get('header', None)
        if header is not None:
            figure.header.add_child(Element(header(self, kwargs)),
                                    name=self.get_name())

        html = self._template.module.__dict__.get('html', None)
        if html is not None:
            figure.html.add_child(Element(html(self, kwargs)),
                                  name=self.get_name())

        script = self._template.module.__dict__.get('script', None)
        if script is not None:
            figure.script.add_child(Element(script(self, kwargs)),
                                    name=self.get_name())

    def add_EventHandler(self,function,name=None, index=None):
        if(hasattr(function,'event_type')):
            if function.event_type in self._event:
                self._event[function.event_type].append(function.get_name())
                self.add_child(function, name=name, index=index)
            else:
                raise Exception('{} do not support this {} event'.format(self._name,function.event_type))
        else:
            raise Exception('It is not an event handler')

        return self._event[function.event_type]

    def get_MapName(self):

        if self._parent is not None and isinstance(self._parent,folium.folium.Map):
            return self._parent.get_name()
        elif self._parent is not None and hasattr(self._parent,'get_MapName'):
            return self._parent.get_MapName()
        else:
            raise Exception("MAP NOT EXIST")

    def get_LayerName(self):
        if self._parent is not None and isinstance(self._parent,OSM_Layer):
            return self._parent.get_name()
        elif self._parent is not None and hasattr(self._parent,'get_LayerName'):
            return self._parent.get_LayerName()
        else:
            return None

class HTML_InnerElement(HTML_BaseElement):

    def render(self, **kwargs):

        for name, element in self._children.items():
            element.render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        header = self._template.module.__dict__.get('header', None)

        if header is not None:
            figure.header.add_child(Element(header(self, kwargs)),
                                    name=self.get_name())

        script = self._template.module.__dict__.get('script', None)
        if script is not None:
            figure.script.add_child(Element(script(self, kwargs)),
                                    name=self.get_name())


        assert self._parent, ('You cannot render this Element '
                                            'if it is no parents.')

        html = self._template.module.__dict__.get('html', None)
        if html is not None:
            self._parent.html.add_child(Element(html(self, kwargs)),
                                  name=self.get_name())

class ShadeDiv(HTML_BaseElement):
    _template = Template(u"""
                {% macro header(this, kwargs) %}
                <style>
                 #shade_{{this._parent.get_name() or this.get_name()}} {
                         display: none;
                         position: absolute;
                         width: 100%;
                         background-color: rgba(0, 0, 0, .3);
                         z-index: 500;
                         justify-content: center;
                         align-items: center;
                           }
		            </style>
		         {% endmacro %}
		         
               {% macro html(this, kwargs) %}
                    <div id="shade_{{this._parent.get_name() or this.get_name()}}">
                    {% for name, element in this.html._children.items() %}
                        {{element.render()}}
                     {% endfor %}
                    </div>
               {% endmacro %}
               
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#shade_{{this._parent.get_name() or this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa
    def __init__(self):
        super(ShadeDiv, self).__init__()
        self._name='ShadeDiv'


class BaseDiv(HTML_InnerElement):
    _template = Template(u"""
                {% macro header(this, kwargs) %}
               <style> 
                #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width}};
                height: {{this.height}};
                left: {{this.left}};
                top: {{this.top}};
                </style>
		         {% endmacro %}

               {% macro html(this, kwargs) %}
                    <div id="{{this.get_name()}}">
                    {% for name, element in this.html._children.items() %}
                        {{element.render()}}
                     {% endfor %}
                    </div>
               {% endmacro %}

                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,name=None,width='fit-content', height='fit-content',
                 left='0%', top='0%', position='relative'):
        super(BaseDiv, self).__init__()
        self._name = 'BaseDiv'
        if name and isinstance(name,str):
            self._name = name

        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.position = position

class LayuiStaticTable(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
            <table lay-filter="{{this.get_name()}}" id="{{this.get_name()}}">
                    <thead>
                             <tr>
                             {% for k,v in this.thead.items() %}
                                 <th lay-data="{{v}}">{{k}}</th>
                             {% endfor %}
                             </tr> 
                    </thead>
                     <tbody>
                              {% for items in this.tbody%}
                               <tr>
                                   {% for item in items %}
                                    <td>{{item}}</td>
                                   {% endfor %}
                               </tr>
                             {% endfor %}
                     </tbody>
                </table>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
            let table = layui.table;
            table.init('{{this.get_name()}}', {
                height: {{this.height}} 
                ,limit: {{this.limit}}
                ,page: {'limit':{{this.limit}},'limits':[{{this.limit}},2*{{this.limit}}]}
                   });
                {% endmacro %}
                """)  # noqa

    def __init__(self,thead={'test':{'field':'test','width':100,'sort':'true'}},tbody=[],height=300,limit=10): #tbody=[['test',1]]
        super(LayuiStaticTable, self).__init__()
        self._name = 'LayuiStaticTable'
        self.thead={}
        for k,v in thead.items():
            self.thead.update({k:'%s'%(v)})
        self.tbody=tbody
        self.height=height
        self.limit=limit

class LayuiIcon(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                    <div>
                    <div>
                    <i class="layui-icon {{this.iconName}} layui-anim layui-anim-rotate layui-anim-loop" style="font-size: {{this.iconSize}}; color: {{this.iconColor}};"></i>
                    </div>
                    <div>
                    <p style="font-size: {{this.fontSize}}; color: {{this.fontColor}};">{{this.fontContent}}</p>
                    </div>
                    </div>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)
    def __init__(self,iconName='layui-icon-loading',iconSize='100px',iconColor='#1E9FFF',fontContent=None,fontColor=None,fontSize=None):
        super(LayuiIcon, self).__init__()
        self._name="LayuiIcon"
        self.iconName=iconName
        self.iconSize=iconSize
        self.iconColor=iconColor
        self.fontContent=fontContent
        self.fontColor=fontColor
        self.fontSize=fontSize


class Button(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                    <button id='{{this.get_name()}}' type="{{this.type}}" style="width: 100%; height: 100%;"><h4>{{this.buttonName}}</h4></button>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,type='submit',buttonName='按钮'):
        super(Button, self).__init__()
        self._name = 'Button'
        self.buttonName = buttonName
        self.type=type

class Form(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                <form id="{{this.get_name()}}" class="layui-form" action="{{this.action}}" method="{{this.method}}" >
                    {% for name, element in this.html._children.items() %}
                        {{element.render()}}
                    {% endfor %}
                </form>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,action,method='GET'):
        super(Form, self).__init__()
        self._name = 'Form'
        self.action=action
        self.method=method

class Select(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                         <div class="layui-input-inline" style="width:{{this.width}}; margin-left:0px;">
                            <select id="{{this.get_name()}}" name="{{this.name}}" {{this.required}} lay-verify="{{this.required}}">
                                {% for op in this.options %}
                                {% for k,v in op.items()%}
                                <option value="{{k}}">{{v}}</option>
                                {% endfor %}
                                {% endfor %}
                            </select>
                        </div>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,name,required=True,width='60%',options=[{}]):
        super(Select, self).__init__()
        self._name = 'Select'
        self.name=name
        self.required = 'required' if required else ''
        self.width = width
        self.options=options

class Select_For_Form(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                    <div class="layui-form-item">
                        {% if this.labelName %}
                        <label class="layui-form-label" style="white-space: nowrap">{{this.labelName}}</label>
                        {% endif %}
                         <div class="layui-input-inline" style="width:{{this.width}}; margin:{{this.margin}};">
                            <select id="{{this.get_name()}}" name="{{this.name}}" {{this.required}} lay-verify="{{this.required}}">
                                {% for op in this.options %}
                                {% for k,v in op.items()%}
                                <option value="{{k}}">{{v}}</option>
                                {% endfor %}
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,labelName,name,required=True,width='60%',margin='0px 0px 0px 40px',options=[{}]):
        super(Select_For_Form, self).__init__()
        self._name = 'Select_For_Form'
        self.labelName=labelName
        self.name=name
        self.required = 'required' if required else ''
        self.width = width
        self.options=options
        self.margin=margin

class Input_For_Form(HTML_InnerElement):

    _template = Template(u"""
               {% macro html(this, kwargs) %}
                 <div class="layui-form-item">
                    <label class="layui-form-label" style="white-space: nowrap">{{this.labelName}}</label>
                    <div class="layui-input-inline" style="width:{{this.width}}; margin:{{this.margin}};">
                    <input id="{{this.get_name()}}" type="{{this.type}}" name="{{this.name}}" {% if this.type != 'text' %} title='{{this.title}}' {{this.checked}} value={{this.checked_value}} {% endif %} {% if this.type == 'text' %} {{ this.readonly }} {{this.required}} lay-verify="{{this.required}}" placeholder="{{this.placeholder}}" autocomplete="{{this.autocomplete}}"{% endif %} class="{{this.classname}}">
                    </div>
                    {% if this.auto_option %}
                    <div class="layui-input-inline" style="width:20%;">
                    <input id="AUTO_{{this.get_name()}}" lay-filter="AUTO_{{this.get_name()}}" type="checkbox" name="Auto_Configuration_{{this.name}}" title="AUTO" {{this.checked}} value={{this.checked_value}} >
                    </div>
                    {% endif %}
                    {% for name, element in this.html._children.items() %}
                        {{element.render()}}
                    {% endfor %}
                 </div>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                
        {% if this.auto_option %}
        layui.use(['form'], function() {
        var form = layui.form;
        $ = layui.jquery;
        form.on('checkbox(AUTO_{{this.get_name()}})', function(data){
              let point = undefined;
              
              {% if this.belong %}
              point={{this.belong.get_name()}};
              {% else %}
              point=$('#AUTO_{{this.get_name()}}').parents('div').slice(-1)[0]['belong'];
              {% endif %}
              point=point['configuration'];
              
              {% if this.auto_configuration %}
               if(point['{{this.auto_configuration}}'])
               {
               point=point['{{this.auto_configuration}}'];
               }
              {% endif %}
              
              if(data.elem.checked)
              {
              data.elem.value=true;
              $('#{{this.get_name()}}').val(point['AUTO_{{this.name}}']);
              $('#{{this.get_name()}}').prop("readonly",true);
              }
              else
              {
              data.elem.value=false;
              $('#{{this.get_name()}}').prop("readonly",false);
              }
        })
})
                {% endif %}
                {% endmacro %}
                """)  # noqa
    def __init__(self,labelName,name,type='text',width='60%',margin='0px 0px 0px 40px',placeholder='请输入信息',autocomplete='off',readonly=False,auto_option=False,checked=True,required=True,title=None,auto_configuration=None,belong=None):
        super(Input_For_Form, self).__init__()
        self._name = 'Input_For_Form'
        self.labelName=labelName
        self.type=type
        self.classname='layui-input' if type=='text' else ''
        self.name=name
        self.width=width
        self.placeholder=placeholder
        self.autocomplete=autocomplete
        self.readonly = 'readonly' if readonly else ''
        self.auto_option=auto_option
        self.checked = 'checked' if checked else ''
        self.checked_value= 'true' if checked else 'false'
        self.required = 'required' if required else ''
        self.title=title
        self.auto_configuration=auto_configuration
        self.margin=margin
        self.belong=belong


class Button_For_Form(Button):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                <div class="layui-form-item" style='text-align:center'>
                <div class="layui-input-block">
                <button id='{{this.get_name()}}' class="layui-btn" type="{{this.type}}" lay-submit lay-filter="formDemo"><h4>{{this.buttonName}}</h4</button>
                {% if this.includeReset %}
                <button type="reset" class="layui-btn layui-btn-primary">重置</button>
                {% endif %}
                </div>
                </div>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)
    def __init__(self,type='submit',buttonName='按钮',includeReset=True):
        super(Button_For_Form,self).__init__(type=type,buttonName=buttonName)
        self._name='Button_For_Form'
        self.includeReset=includeReset

class UL(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                    <ul id='{{this.get_name()}}'>
                    {% for name, element in this.html._children.items() %}
                    {{element.render()}}
                    {% endfor %}
                    </ul>
                {% endmacro %}
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self):
        super(UL, self).__init__()
        self._name = 'UL'

class LI(HTML_InnerElement):
    _template = Template(u"""
               {% macro html(this, kwargs) %}
                    <li id='{{this.get_name()}}'>
                    {% if this.content %}
                     {{this.content}}
                    {% else %}
                        {% for name, element in this.html._children.items() %}
                        {{element.render()}}
                        {% endfor %}
                    {% endif %}
                    </li>
                {% endmacro %}
                
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,content=None):
        super(LI, self).__init__()
        self._name = 'LI'
        self.content=content

class Tabs(HTML_InnerElement):
    _template = Template(u"""
        {% macro html(this, kwargs) %}
        <div class="layui-tab" id='{{this.get_name()}}' >
           <ul class="layui-tab-title">
              {% for item in this.tabs_items %}
              <li {% if loop.first %} class="layui-this" {% endif %}> {{item}} </li>
              {% endfor %}
           </ul>
           <div class="layui-tab-content">
              {% for item in this.tabs_items %}
              <div class="layui-tab-item {% if loop.first %} layui-show {% endif %}">
              {% set index = loop.index %}
              {% for name, element in this.html._children.items() %}
              {% if this.tabs_content[name] == index %}
              {{element.render()}}
              {% endif %}
              {% endfor %}
              </div>
              {% endfor %}
            </div>
        </div>
                {% endmacro %}
                
                {% macro script(this, kwargs) %}
                {% for k,v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self,tabs_items=[]):
        super(Tabs, self).__init__()
        self._name = 'Tabs'
        self.tabs_items=tabs_items
        self.tabs_content={}

    def add_child(self, child, name=None, index=None,tab_num=1):
        if name is None:
            name = child.get_name()
        if index is None:
            self._children[name] = child
        else:
            items = [item for item in self._children.items()
                     if item[0] != name]
            items.insert(int(index), (name, child))
            self._children = OrderedDict(items)
        child._parent = self
        self.tabs_content[name]=tab_num
        return self
