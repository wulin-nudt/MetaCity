from OSM_Map.OSM_Marker import Moving_Point_Marker,OSM_Popup
from OSM_Map.Moving_Point_Application.Configuration_Menu import Moving_Point_Configuration_Menu
from OSM_Map.Moving_Point_Application.Event_Handler import MoveEvent_For_MovingPointMarker,ContextmenuEvent_For_MovingPointMarker,QoSPanelInitEvent_For_MovingPointMarker,TestEvent_For_MovingPointMarker
from OSM_Map.OSM_HTML_BaseElement import Tabs,BaseDiv
from jinja2 import Template
import folium
import json

class Moving_Point_Application(Moving_Point_Marker):

    def build(self):

        cm=Moving_Point_Configuration_Menu().add_to(self)
        cm.build()

        QoS_Panel_for_Moving_Point(max_width=1000,maxHeight=1000,className='testpopup').add_to(self).build(qos_index=['delay','packet_loss','band_width'])
        QoSPanelInitEvent_For_MovingPointMarker(url='/check_emulation_status/').add_to(self)
        # OSM_Popup(max_width=1000).add_child(folium.Vega(json.load(open('1.json')), width=1000, height=250)).add_to(self)
        # TestEvent_For_MovingPointMarker().add_to(self)
        ContextmenuEvent_For_MovingPointMarker(cm).add_to(self)
        MoveEvent_For_MovingPointMarker().add_to(self)

class QoS_Panel_for_Moving_Point(OSM_Popup):
    _template = Template(u"""
        var {{this.get_name()}} = L.popup({{ this.options|tojson }});
        
        let QoS = {{ this.QoS|tojson|safe }};
        {% for name, element in this.html._children.items() %}
            let {{ name }} = $(`{{ element.render(**kwargs).replace('\\n',' ') }}`)[0];
            {{ this.get_name() }}.setContent({{ name }});
            for(x in QoS)
            {
            {{ this._parent.get_name() }}['configuration']['QoS'][x].div = $({{ name }}).find("#"+QoS[x].div)[0];
            }
        {% endfor %}

        {{ this._parent.get_name() }}.bindPopup({{ this.get_name() }})
        {% if this.show %}.openPopup(){% endif %};


        {% for name, element in this.script._children.items() %}
            {{element.render()}}
        {% endfor %}

        {% for k,v in this._event.items() %}
        {% for v1 in v %}
        {{this.get_name()}}.on('{{k}}',{{v1}});
        {% endfor %}
        {% endfor %}
    """)  # noqa

    def build(self,qos_index=['delay']): #'packet_loss'

        if isinstance(qos_index, list):
            self.qoS_panel = Tabs(tabs_items=qos_index).add_to(self)
        else:
            raise Exception("the type of qos_index is error")
        QoS={}
        for i, index in enumerate(qos_index):
            bd = BaseDiv(name=index)
            self.qoS_panel.add_child(bd, tab_num= i+1)
            QoS.update({index: {'div':bd.get_name(),'data':{},'bind':False}})
        QoS.update({'status':False})
        if hasattr(self, '_parent'):
            self._parent.update_configuration({'QoS': QoS})
            self._parent.autopopup = None
        self.QoS=QoS