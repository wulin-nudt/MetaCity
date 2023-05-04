from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from OSM_Map.OSM_HTML_BaseElement import Button,HTML_BaseElement,Form,Input_For_Form,Button_For_Form
from jinja2 import Template

class Menu(HTML_BaseElement):
    _template = Template(u"""
            {% macro header(this, kwargs) %}
            <style>
                #{{this.get_name()}} {
                    position: relative;
                    width:{{this.width}};
                    height:{{this.height}};
	                display:{{this.display}};
	                vertical-align:{{this.vertical_align}};
	                margin: {{this.margin}};
	                left: {{this.left}};
                    top: {{this.top}};
                                    }
            </style>
            {% endmacro %}
            
            {% macro html(this, kwargs) %}
              <div id='{{this.get_name()}}'>
              <table class="layui-table" lay-skin="nob" style='table-layout: fixed; width: 100%; caption-side: top;'>
              <caption><center><h1>{{this.menuName}}</h1></center></caption>
              
              {% for r in this.get_row() %}
                <tr>
                 {% for c in this.get_col() %}
                    <td id="{{this.get_datacellName(r,c)}}" align='center'> 
                    {% for name, element in this.html._children.items() %}
                                {% if element.row == r and  element.col==c %}
                                 {{element.render()}}
                                {% endif %}
                    {% endfor %}
                    </td>
                 {% endfor %}
                </tr>
              {% endfor %}
              </table>
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

    def __init__(self,row=None,col=1,menuName='菜单',width='fit-content',
                 height='fit-content',margin='0',vertical_align='top',left='0%',top='0%',display='inline-block'):
        super(Menu, self).__init__()
        self._name = 'Menu'
        if row:
            self.row=range(row)
        else:
            self.row = row
        self.col=range(col)
        self.menuName=menuName
        self.width=width
        self.height=height
        self.margin=margin
        self.vertical_align=vertical_align
        self.left=left
        self.top=top
        self.display=display

    def get_datacellName(self,row,col):
        return self.get_name()+"_"+str(row)+"_"+str(col)

    def get_row(self):
        if not self.row:
            self.row=range(len(self._children))
        return self.row

    def get_col(self):
        return self.col

class MenuElement(HTML_BaseElement):

    def __init__(self, row=None, col=1):
        if row:
            self.row = row-1
        else:
            self.row=row
        self.col = col-1

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
            ht=Element(html(self, kwargs))
            ht.row=self.get_row()
            ht.col=self.get_col()
            self._parent.html.add_child(ht,
                                  name=self.get_name())

    def get_row(self):
        if self.row is None and self._parent:
            l=list(self._parent._children.keys())
            self.row=l.index(self.get_name())
        return self.row

    def get_col(self):
        return self.col

class MenuButton(MenuElement,Button):
    _template = Template(u"""
    
                {% macro html(this, kwargs) %}
                
                <button id='{{this.get_name()}}' type="{{this.type}}" class="layui-btn layui-btn-lg layui-btn-radius layui-btn-normal" style="width: 100%; height: 100%;">{{this.buttonName}}</button>
                {% endmacro %}
                
                {% macro script(this, kwargs) %}
                {% for k, v in this._event.items() %}
                    {% for v1 in v %}
                    $('#{{this.get_name()}}').on('{{k}}',{{v1}});
                    {% endfor %}
                {% endfor %}
                {% endmacro %}
                """)  # noqa

    def __init__(self, row=None, col=1, buttonName='按钮',type='submit'):
        MenuElement.__init__(self,row=row, col=col)
        Button.__init__(self,type=type,buttonName=buttonName)
        self._name = 'MenuButton'

class MenuForm(MenuElement,Form):
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
    def __init__(self,action,row=None,col=1,method='GET'):
        MenuElement.__init__(self, row=row, col=col)
        Form.__init__(self,action=action,method=method)
        self._name = 'MenuForm'