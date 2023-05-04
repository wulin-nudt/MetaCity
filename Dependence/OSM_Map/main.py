import osmnx as ox
from osmnx import utils_graph
import matplotlib.pyplot as plt
import networkx as nx
import requests

# ox.settings.all_oneway = True
# c=ox.graph_from_xml(filepath='map1.osm')
# ox.plot_graph(c)
# fig, ax = ox.plot_graph(c, node_color='r')
# ox.save_graph_xml(c, filepath='/home/kylin/graph.osm')

# ox.settings.overpass_settings='[out:xml][timeout:{timeout}]{maxsize}'
# ox.settings.cache_only_mode=True
# try:
#     G = ox.graph_from_address('中南大学', dist=6000,custom_filter='["highway"]')
# except:
#     print('test')
#     pass
# ox.plot_graph(G,bgcolor="#555555",node_color='r')

# G= ox.graph_from_bbox(north=28.2100,south=28.1698,east=112.8828,west=112.8159)
# ox.plot_graph(G)

# G = ox.graph_from_place('Wangcheng,changsha,hunan,china',buffer_dist=2000)
# ox.plot_graph(G)


# G = ox.graph_from_point((28.17314535, 112.92207697547268), dist=6000)
# ox.plot_graph(G)

# G = ox.graph_from_xml(filepath='map1.osm',bidirectional=True)
# ox.plot_graph(G)

# from shapely.geometry import Polygon
# ext = [(112.8159,28.1698), (112.8159,28.2100), (112.8828,28.2100), (112.8828,28.1698),(112.8159,28.1698)]
# polygon = Polygon(ext)
# G = ox.graph_from_polygon(polygon=polygon)
# ox.plot_graph(G)

# gdf=ox.geometries_from_address('中南大学',dist=6000,tags = {'amenity':True})
# gdf.plot()
# plt.show()

# gdf=ox.geometries_from_address('中南大学',dist=6000,tags = {'building': True})
# ox.plot_footprints(gdf)

# G = ox.graph_from_address('中南大学', dist=6000)
# ox.plot_graph(G)
# ox.plot_figure_ground(address='中南大学', dist=6000,default_width=0.2)

# ox.settings.all_oneway = True
# G = ox.graph_from_address('中南大学', dist=6000)
# nodes_sh,edges_sh=ox.graph_to_gdfs(G)
# print(nodes_sh)
# print(edges_sh['geometry'])
# ox.save_graph_xml((nodes_sh,edges_sh), filepath='/home/kylin/graph1.osm',oneway=True)

# G = ox.graph_from_address('中南大学', dist=6000)
# nodes_sh,edges_sh=ox.graph_to_gdfs(G)
# C=ox.graph_from_gdfs(nodes_sh,edges_sh)
# print(edges_sh.crs)

# G = ox.graph_from_address('广州大学', dist=6000, network_type='all')
# origin_point = (23.039506, 113.364664)
# origin_node,dist= ox.nearest_nodes(G, origin_point[1], origin_point[0],return_dist=True)
# print(origin_node)
# print(dist)


# G = ox.graph_from_address('广州大学', dist=6000, network_type='all')
# origin_point = (23.039506, 113.364664)
# destination_point = (23.074058, 113.386148)
# origin_node= ox.nearest_nodes(G, origin_point[1], origin_point[0])
# destination_node = ox.nearest_nodes(G, destination_point[1], destination_point[0])
# route=ox.k_shortest_paths(G,origin_node,destination_node,k=30)
# route=list(route)
# ox.plot_graph_routes(G, route)



# point = ox.geocode('中南大学')
# print(point)
from pathlib import Path
import json
proxy = '127.0.0.1:7890'
proxies = {
    "http": "http://%(proxy)s/" % {'proxy': proxy},
    "https": "http://%(proxy)s/" % {'proxy': proxy}
}

query="""<osm-script output='json' timeout="1800" element-limit="100000000">
  <union>
    <area-query ref="3603202711"/>
    <recurse type="node-relation" into="rels"/>
    <recurse type="node-way"/>
    <recurse type="way-relation"/>
  </union>
  <union>
    <item/>
    <recurse type="way-node"/>
  </union>
  <print mode="body"/>
</osm-script>
"""

data={"data": query}
response=requests.post(url='https://maps.mail.ru/osm/tools/overpass/api/interpreter',data=data,proxies=proxies)
# print(response.status_code)
print(response.json())
rj=response.json()

# cache_folder = Path('home')
# cache_folder.mkdir(parents=True, exist_ok=True)
# filename='ttt.json'
# filepath=cache_folder/filename
# filepath.write_text(json.dumps(rj,ensure_ascii=False), encoding="utf-8")

# response=requests.get("https://nominatim.openstreetmap.org/search?format=json&limit=1&dedupe=0&q=%E4%B8%AD%E5%8D%97%E5%A4%A7%E5%AD%A6",proxies=proxies)
# print(response.json())

# from OSM_Downloader import OSM_Downloader
# OSM_Downloader().Download_By_Point(center_point=[28.17314535,112.92207697547268])

# gdf=ox.geocode_to_gdf(['湖南大学','中南大学'])
# gdf.plot()
# plt.show()


# G = ox.graph_from_address('中南大学', dist=6000)
# 形成路网图
# G = ox.project_graph(G)
# plt.rcParams['figure.dpi'] = 400
# fig=plt.figure(figsize=(10,6)) #设置画布大小
# ax = plt.gca()
# ox.plot.plot_graph(G,ax=ax,figsize=(8*4),bgcolor='white',node_color='blue',edge_color='grey',show=True,edge_linewidth=0.3,node_size=5,node_alpha=0.5)
# G_84 = ox.project_graph(G , to_crs='EPSG:4326')
# ox.plot_graph_folium(G_84, tiles='openstreetmap',kwargs={'width':0.1})

# ox.settings.all_oneway=True
# name='中南大学'
# origin='中南大学'
# destination='湖南大学'
# origin=ox.geocode(origin)
# destination = ox.geocode(destination)
# G = ox.graph_from_address(name, dist=10000)
# ox.save_graph_xml(G, filepath='map/graph2.osm')
# G_84 = ox.project_graph(G , to_crs='EPSG:4326')
# origin=ox.nearest_nodes(G_84,origin[1],origin[0])
# destination= ox.nearest_nodes(G_84,destination[1], destination[0])
# rou = ox.shortest_path(G_84, origin, destination)
# m=ox.plot_graph_folium(G_84, tiles='openstreetmap',kwargs={'width':0.1})
# m=ox.plot_route_folium(G_84,rou,route_map=m,weight=2, color="#8b0000")

# from mapelements.OSMMapObject import OSMMapObject,OSMXMLIterObjectFactory
# osm=OSMMapObject(OSMXMLIterObjectFactory(r'/home/kylin/graph.osm'))
# osm1=OSMMapObject(OSMXMLIterObjectFactory(r'/home/kylin/graph1.osm'))
# print(len(osm.get_lines()))
# print(len(osm1.get_lines()))
# print(set(osm.get_lines().keys()) ^ set(osm1.get_lines().keys()))

# name='中南大学'
# origin='中南大学'
# destination='湖南大学'
# origin=ox.geocode(origin)
# destination = ox.geocode(destination)
# G1 = ox.graph_from_xml(filepath='map/1.xml')
# G = ox.graph_from_address(name, dist=6000)
# origin=ox.nearest_nodes(G1,origin[1],origin[0])
# destination= ox.nearest_nodes(G1,destination[1], destination[0])
# rou = ox.shortest_path(G, origin, destination)
# rou1 = ox.shortest_path(G1, origin, destination)
# print(rou1[0])
# print(G1.nodes[9450281425])
# m=ox.plot_graph_folium(G, tiles='openstreetmap',kwargs={'width':0.1})
# m=ox.plot_route_folium(G,rou,route_map=m,weight=2, color="#8b0000")
# m=ox.plot_route_folium(G1,rou1,route_map=m,weight=2, color="#8b0000")
# m.save('2.html')

# import json
# c=json.dumps("xml//ssad")
# print(c)

# from OSM_Map.OSM_Downloader import OSM_Downloader
# d=OSM_Downloader()
# OSM_Downloader.FileType='json'
# c=d.Download_By_Address('中南大学',dist=25000)
# # d.OSM_File_Find_From_CacheIndex([1])
# print(c[0].expanduser())

# G1 = ox.graph_from_xml(filepath='map/1.xml')
# m=ox.plot_graph_folium(G1, tiles='openstreetmap',kwargs={'width':0.1})
# m.save('1.html')


# ox.settings.cache_only_mode=True
# name='中南大学'
# G = ox.graph_from_address(name, dist=6000)
# m=ox.plot_graph_folium(G, tiles='openstreetmap',kwargs={'width':0.1})
# m.save('2.html')

# G = ox.graph_from_place('Wangcheng,changsha,hunan,china',buffer_dist=2000)
# m=ox.plot_graph_folium(G, tiles='openstreetmap',kwargs={'width':0.1})
# m.save('1.html')

# from OSM_Map.OSM_MAP import OSM_Downloader
# d=OSM_Downloader()
# OSM_Downloader.FileType='json'
# c=d.Download_By_Place('Wangcheng,changsha,hunan,china',buffer_dist=2000)
# print(c[0].expanduser())

# G1 = ox.graph_from_xml(filepath='map/1.xml')
# m=ox.plot_graph_folium(G1, tiles='openstreetmap',kwargs={'width':0.1})
# m.save('1.html')
