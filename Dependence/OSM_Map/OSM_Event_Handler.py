from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from jinja2 import Template

class OSM_Event_Handler(MacroElement):
    _template = Template(u"""
                {% macro script(this, kwargs) %}
                function {{this.get_name()}}(e)
                {
                
                }
                {% endmacro %}
                """)  # noqa
    def __init__(self):
        super(OSM_Event_Handler, self).__init__()
        self._name = 'OSM_Event_Handler'
        self.event_type=''

    def add_to(self, parent, name=None, index=None):
        parent.add_EventHandler(self, name=name, index=index)
        return self


class OSM_Anonymous_Event_Handler(Element):
    _template = Template(u"""
                
                """)  # noqa

    def __init__(self):
        super(OSM_Anonymous_Event_Handler, self).__init__()
        self._name = 'OSM_Anonymous_Event_handler'
        self.event_type = ''

    def add_to(self, parent, name=None, index=None):
        parent.add_EventHandler(self, name=name, index=index)
        return self

    def render(self, **kwargs):

        assert self._parent, ('You cannot render this Element '
                                            'if it is no parents.')

        event=self._parent._event.get(self.event_type,None)
        if not event:
            raise Exception('The Parent do not support this {} event'.format(self.event_type))
        else:
            if self.get_name() in event:
                event.remove(self.get_name())
                event.append(self._template.render(this=self, kwargs=kwargs))
