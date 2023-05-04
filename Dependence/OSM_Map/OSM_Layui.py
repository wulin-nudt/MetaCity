from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from folium.elements import JSCSSMixin
from jinja2 import Template

class OSM_Layui(JSCSSMixin,MacroElement):
    default_js = [
    ('layui',
     'https://unpkg.com/layui@2.7.3/dist/layui.js'),  # noqa
    ]
    default_css = [
    ('layui_css',
     'https://unpkg.com/layui@2.7.3/dist/css/layui.css'), # noqa
    ]
    def __init__(self):
        super(OSM_Layui, self).__init__()

    def render(self, **kwargs):
        super(OSM_Layui, self).render(**kwargs)
