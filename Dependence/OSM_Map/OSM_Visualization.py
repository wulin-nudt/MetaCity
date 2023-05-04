from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from folium.elements import JSCSSMixin
from jinja2 import Template

class Vega(JSCSSMixin,MacroElement):
    default_js = [
        ('d3',
         'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js'),
        ('vega',
         'https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js'),
        ('jquery',
         'https://code.jquery.com/jquery-2.1.0.min.js'),
    ]
    _template = Template(u"""
                    {% macro script(this, kwargs) %}
                    function osm_vega_parse(spec, div) {
                             vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });
                                                   }
                    {% endmacro %}
    """)
    def __init__(self):
        super(Vega, self).__init__()
        self._name = 'Vega'

    def render(self, **kwargs):
        super(Vega, self).render(**kwargs)


class VegaEmbed(JSCSSMixin,MacroElement):
    default_js = [
        ('vega5',
         'https://cdn.jsdelivr.net/npm/vega@5'),
        ('VegaEmbed',
         'https://cdn.jsdelivr.net/npm/vega-embed@6'),
        ('vegalite',
         'https://cdn.jsdelivr.net/npm/vega-lite@5')
    ]
    def __init__(self):
        super(VegaEmbed, self).__init__()
        self._name = 'VegaEmbed'

    def render(self, **kwargs):
        super(VegaEmbed, self).render(**kwargs)