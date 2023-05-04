import osmnx as ox
import osmnx.folium
from osmnx import utils_graph
import matplotlib.pyplot as plt
import networkx as nx
import json
import requests
import folium
from folium.raster_layers import ImageOverlay,VideoOverlay
from OSM_Map.OSM_Marker import Moving_Point_Marker,\
    OSM_Popup,OSM_Icon,OSM_Tooltip,OSM_Signal_Range,Wireless_Access_Point_Marker,NetWorkLink,OSM_Marker
from OSM_Map.OSM_Layui import OSM_Layui
from OSM_Map.OSM_Folium_Element import Global_Network_Configuration_Layer,OSM_Map
from OSM_Map.Moving_Point_Application.Moving_Point_Application import Moving_Point_Application
from OSM_Map.Wireless_Access_Point_Application.Wireless_Access_Point_Application import Wireless_Access_Point_Application
from OSM_Map.NetWorkLink_Application.NetWorkLink_Application import NetWorkLink_Application
from OSM_Map.Edge_Cloud_Application.Edge_Cloud_Application import Edge_Cloud_Application
from OSM_Map.Menu_Application.Menu_Application import Menu_Application
# G1 = ox.graph_from_xml(filepath='map/1.xml')
# m=ox.plot_graph_folium(G1, tiles='openstreetmap',kwargs={'width':0.1})
# m.save('1.html')
bj_map = folium.Map(location=[39.93, 115.40], zoom_start=12, tiles='openstreetmap',width='85%',height='85%',left='1%',top='1%',display='inline-block')
# OSM_Marker(name='mp', popup=None, tooltip=None,icon=OSM_Icon(color='red',icon='location-arrow', prefix='fa'),active=True,configuration={'speed':50}).add_to(bj_map)
# bj_map = OSM_Map(location=[39.93, 115.40], zoom_start=12, tiles='openstreetmap',width='85%',height='85%',left='1%',top='1%',display='inline-block')
# folium.Marker(
#     location=[39.95, 115.33],
#     popup='Mt. Hood Meadows',
#     icon=folium.Icon(icon='cloud')
# ).add_to(bj_map)
#
# folium.Marker(
#     location=[39.96, 115.32],
#     popup='Timberline Lodge',
#     icon=folium.Icon(color='green')
# ).add_to(bj_map)
p1=folium.Popup('test',parse_html=True,max_width=10000,show=True)

t=folium.Tooltip('test',style='color:blue',sticky=True)
# t1=OSM_Tooltip('test',style='color:blue',sticky=True)
# t2=OSM_Tooltip('test',style='color:blue',sticky=True)
# t3=OSM_Tooltip('test',style='color:blue',sticky=True)
p=folium.Popup(max_width=1000,show=True).add_child(folium.Vega(json.load(open('1.json')), width=1000, height=250))
# p1=OSM_Popup(max_width=1000).add_child(folium.Vega(json.load(open('1.json')), width=1000, height=250))
# p2=OSM_Popup(max_width=1000).add_child(folium.Vega(json.load(open('1.json')), width=1000, height=250))
# p3=OSM_Popup(max_width=1000).add_child(folium.Vega(json.load(open('1.json')), width=1000, height=250))

# folium.Marker(
#     location=[39.93, 115.34],
#     popup=p1,
#     icon=folium.Icon(color='red', icon='info-sign'), # 标记颜色  图标
#     draggable=True,
#     tooltip=t
# ).add_to(bj_map)
#
# folium.Marker(
#     location=[39.96, 115.32],
#     popup=p,
#     icon=folium.Icon(color='red', icon='cloud'), # 标记颜色  图标
#     draggable=True
# ).add_to(bj_map)

# folium.WmsTileLayer(
#
# url='http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi',
#
# name='test',
#
# fmt='image/png',
#
# layers='nexrad-n0r-900913',
#
# attr=u'Weather data © 2012 IEM Nexrad',
#
# transparent=True,
#
# overlay=True,
#
# control=True,
#
# ).add_to(bj_map)
# ImageOverlay(image='https://maps.lib.utexas.edu/maps/historical/newark_nj_1922.jpg',bounds=[[40.712216, -74.22655], [40.773941, -74.12544]]).add_to(bj_map)
# VideoOverlay(video_url='https://www.mapbox.com/bites/00188/patricia_nasa.webm',bounds=[[ 32, -130], [ 13, -100]]).add_to(bj_map)
# folium.WmsTileLayer(url='http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi',layers='nexrad-n0r-900913',format='image/png',transparent=True,attr='Weather data © 2012 IEM Nexrad').add_to(bj_map)
# folium.TileLayer(tiles='Stamen Terrain').add_to(bj_map)
# folium.TileLayer(tiles='OpenStreetMap').add_to(bj_map)
# folium.ClickForMarker().add_to(bj_map)
# folium.LatLngPopup().add_to(bj_map)
# folium.RegularPolygonMarker(location=[39.93, 115.34],
#                             popup='Hawthorne Bridge',
#                             fill_color='#45647d',
#                             number_of_sides=8, radius=20).add_to(bj_map)
# folium.Circle(
#     location=(39.93, 115.39),
#     radius=500,   # 圆的半径
#     popup='Laurelhurst Park',
#     color='#FF1493',
#     fill=True,
#     fill_color='#FFD700'
# ).add_to(bj_map)
# folium.PolyLine(locations=[[39.93, 115.34],[39.96, 115.32]]).add_to(bj_map)
# folium.Polygon(locations=[[39.93, 115.34],[39.96, 115.32],[39.94, 115.33]]).add_to(bj_map)
# folium.Rectangle(bounds=[[39.93, 115.34],[39.96, 115.32]]).add_to(bj_map)

# osmlayer=Global_Network_Configuration_Layer().add_to(bj_map)
#
# mp=Moving_Point_Application(name='Moving_Point',popup=p1,tooltip=t1,icon=OSM_Icon(color='red', icon='location-arrow',prefix='fa'),
#                          active=False).add_to(osmlayer)
# mp.build()
#
# mp3=Edge_Cloud_Application(name='Edge_Cloud',popup=None,tooltip=None,icon=OSM_Icon(color='red', icon='cloud',prefix='fa'),
#                          active=False).add_to(osmlayer)
# mp3.build()
#
# mp1=Wireless_Access_Point_Application(name='Wireless_Access_Point',popup=p2,tooltip=t2,icon=OSM_Icon(color='red', icon='wifi',prefix='fa'),
#                          active=False,signal_range=OSM_Signal_Range(radius=500,tooltip=OSM_Tooltip('test'))).add_to(osmlayer)
# mp1.build()
#
# mp2=NetWorkLink_Application(mp1,name='NetWorkLink',active=False,tooltip=t3,popup=p3).add_to(osmlayer)
# mp2.build()
#
# OSM_Application=bj_map.get_root()
# OSM_Layui().add_to(OSM_Application)
#
# entity={'Global_Network_Configuration_Layer':osmlayer,'Moving_Point':mp,'Wireless_Access_Point':mp1,'Edge_Cloud':mp3,'NetWorkLink':mp2}
# menu=Menu_Application(bj_map,osmlayer,entity).add_to(OSM_Application)
# menu.build()

# # bj_map.fit_bounds([[39, 116], [38.5, 116.5]]) #设置地图显示的边框
bj_map.save('test_09.html')
# for n,e in mp.script._children.items():
#     print(e.render())
# for i,v in p.script._children.items():
#     print(v.render())

from OSM_Map.Edge_Computing_Application import EdgeComputingApplication
e=EdgeComputingApplication(title='test',location=[39.93, 115.40])
# e.start_run()
e.output('3.html')