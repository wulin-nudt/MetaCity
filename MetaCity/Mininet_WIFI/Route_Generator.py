import osmnx as ox
import datetime
import shutil
import os
import folium
import json
from shapely.geometry import Polygon,box
from OSM_Map.OSM_Downloader import OSM_Downloader

import geopandas as gpd
# import pandas as pd
# pd.options.display.max_columns=None

class Route_Generator:
    def __init__(self):
        self.osm_downloader = OSM_Downloader()

    def generate_routes(self,loaction={}):
        print(loaction)
        self.datas = {'routes': []}
        for k ,v in loaction.items():
            if not v.get('routes_distance',False) or v.get('network_type','drive')!=v.get('routes_type',''):
                if v.get('location', False):
                    network_type=v.get('network_type','drive')
                    self.datas['routes'].append({'name':k,'route':self.routes(points=v.get('location', None),network_type=network_type),'type':network_type})
        return self.datas

    def routes(self,points=[],network_type='drive'):
        routes=[]
        if points and len(points)>1:
            G=None
            points=[tuple(map(float, p.split(',')))[::-1] for p in points]
            polygon_points=None
            if len(points)<3:
                polygon_points = [p for p in points]
                mid=(0.01+(polygon_points[0][0]+polygon_points[1][0])/2,0.01+(polygon_points[0][1]+polygon_points[1][1])/2)
                polygon_points.append(mid)
            poly = Polygon(polygon_points if polygon_points else points)
            file,polygon1=self.osm_downloader.OSM_File_Find_From_CacheIndex(poly.bounds)
            if file:
                G=self.osm_downloader.json_to_graph(polygon1,simplify=False,truncate_by_edge=True,json_filepaths=file,network_type=network_type)
                # print(G.nodes(data=True))
                # nodes_sh=ox.graph_to_gdfs(G,edges=False,node_geometry=False)

            else:
                polygon2=box(poly.bounds[0]-0.1,poly.bounds[1]-0.1,poly.bounds[2]+0.1,poly.bounds[3]+0.1)
                file=self.osm_downloader.Download_By_Polygon(polygon2)
                file=[str(f.expanduser()) for f in file]
                G=self.osm_downloader.json_to_graph(polygon2,simplify=False,truncate_by_edge=True,json_filepaths=file,network_type=network_type)

            # center=tuple(map(float,points[0].split(',')))
            # G = ox.graph_from_point(center,dist=6000)
            #m=osm_map
            for i in range(len(points)-1):
                # origin=tuple(map(float,points[i].split(',')))
                origin=ox.nearest_nodes(G, points[i][0], points[i][1])
                # destination=tuple(map(float,points[i+1].split(',')))
                destination=ox.nearest_nodes(G, points[i+1][0], points[i+1][1])
                rou = ox.shortest_path(G, origin, destination)
                routes.append(self.route_for_folium(G, rou))
                #m = ox.plot_route_folium(G, rou, route_map=m, weight=2, color="#8b0000")
            #m.save("111.html")
        # ox.plot_graph_folium(G, tiles='openstreetmap', kwargs={'width': 0.1}).save('456123.html')
        return routes


    def route_for_folium(
            self,
            G,
            route,
            other_attribute=None,
            **kwargs,
    ):
        try:

            node_pairs = zip(route[:-1], route[1:])
            uvk = ((u, v, min(G[u][v], key=lambda k: G[u][v][k]["length"])) for u, v in node_pairs)
            gdf_edges = ox.graph_to_gdfs(G.subgraph(route), nodes=False).loc[uvk]
        except Exception as ex:
            self.datas.update({'Exception':[repr(ex)]})
            return []

        return self.get_route_edage(gdf_edges,other_attribute,**kwargs)

    def get_route_edage(self,gdf, other_attribute, **kwargs):

        locations=[]

        # identify the geometry and popup columns
        if other_attribute is None:
            attrs = ["geometry"]
        else:
            attrs = ["geometry", other_attribute]
        for vals in gdf[attrs].values:
            params = dict(zip(["geom", "other_attribute"], vals))
            if params["geom"]:
                location = [[lat, lng] for lng, lat in params["geom"].coords]
                locations.append(location)

        return locations
