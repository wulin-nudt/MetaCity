import osmnx as ox
import networkx as nx
import requests
import time
import json
import re
import logging as lg
import warnings
from osmnx import utils_geo,projection,downloader,settings,utils,graph,truncate,simplification,stats
from pathlib import Path
from hashlib import sha1
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon,box

class OSM_Downloader(object):
    FileType='json'
    Index_File=r'cache/index.txt'
    File_Exist=True
    overpass_settings='[out:{FileType}][timeout:{timeout}]{maxsize}'

    def Download_By_Address(self,
    address,
    dist=1000,
    network_type="all_private",
    return_coords=False,
    clean_periphery=True,
    custom_filter=None,
):
        point = ox.geocode(query=address)

        osm_file_paths = self.Download_By_Point(
            point,
            dist,
            network_type=network_type,
            clean_periphery=clean_periphery,
            custom_filter=custom_filter,
        )
        return osm_file_paths

    def Download_By_Point(self,
    center_point,
    dist=1000,
    network_type="all_private",
    clean_periphery=True,
    custom_filter=None,
):
        # create bounding box from center point and distance in each direction
        north, south, east, west = utils_geo.bbox_from_point(center_point, dist)

        # create a graph from the bounding box
        osm_file_paths = self.Download_By_BBox(
            north,
            south,
            east,
            west,
            network_type=network_type,
            clean_periphery=clean_periphery,
            custom_filter=custom_filter,
        )
        return osm_file_paths

    def Download_By_BBox(self,
    north,
    south,
    east,
    west,
    network_type="all_private",
    clean_periphery=True,
    custom_filter=None,
):
        polygon = utils_geo.bbox_to_poly(north, south, east, west)

        osm_file_paths = self.Download_By_Polygon(
            polygon,
            network_type=network_type,
            clean_periphery=clean_periphery,
            custom_filter=custom_filter,
        )
        return osm_file_paths

    def Download_By_Polygon(self,
    polygon,
    network_type="all_private",
    clean_periphery=True,
    custom_filter=None,
):
        print(polygon.centroid.xy)
        print(polygon.bounds)
        print(polygon.boundary)
        print(type(polygon))
        if not polygon.is_valid:  # pragma: no cover
            raise ValueError("The geometry to query within is invalid")
        if not isinstance(polygon, (Polygon, MultiPolygon)):  # pragma: no cover
            raise TypeError(
                "Geometry must be a shapely Polygon or MultiPolygon. If you requested "
                "graph from place name, make sure your query resolves to a Polygon or "
                "MultiPolygon, and not some other geometry, like a Point. See OSMnx "
                "documentation for details."
            )

        if clean_periphery:
            # create a new buffered polygon 0.5km around the desired one
            buffer_dist = 500
            poly_proj, crs_utm = projection.project_geometry(polygon)
            poly_proj_buff = poly_proj.buffer(buffer_dist)
            poly_buff, _ = projection.project_geometry(poly_proj_buff, crs=crs_utm, to_latlong=True)

            # download the network data from OSM within buffered polygon
            response_paths = self._osm_network_download(poly_buff, network_type, custom_filter)
        else:
            # download the network data from OSM
            response_paths = self._osm_network_download(polygon, network_type, custom_filter)

        if not self.File_Exist or not Path(self.Index_File).exists():
            index_item={"center":(polygon.centroid.xy[1][0],polygon.centroid.xy[0][0]),"bounds":polygon.bounds,'filepath':tuple([str(x.expanduser()) for x in response_paths])}
            with open(self.Index_File,'a+') as f:
                f.write("%s\n"%(json.dumps(index_item)))
            self.File_Exist=True

        return response_paths

    def Download_By_Place(
            self,
            query,
            network_type="all_private",
            simplify=True,
            retain_all=False,
            truncate_by_edge=False,
            which_result=None,
            buffer_dist=None,
            clean_periphery=True,
            custom_filter=None,
    ):
        # create a GeoDataFrame with the spatial boundaries of the place(s)
        if isinstance(query, (str, dict)):
            # if it is a string (place name) or dict (structured place query),
            # then it is a single place
            gdf_place = ox.geocode_to_gdf(
                query, which_result=which_result, buffer_dist=buffer_dist
            )
        elif isinstance(query, list):
            # if it is a list, it contains multiple places to get
            gdf_place = ox.geocode_to_gdf(query, buffer_dist=buffer_dist)
        else:  # pragma: no cover
            raise TypeError("query must be dict, string, or list of strings")

        # extract the geometry from the GeoDataFrame to use in API query
        polygon = gdf_place["geometry"].unary_union
        utils.log("Constructed place geometry polygon(s) to query API")

        # create graph using this polygon(s) geometry
        osm_file_paths = self.Download_By_Polygon(
            polygon,
            network_type=network_type,
            clean_periphery=clean_periphery,
            custom_filter=custom_filter,
        )
        return osm_file_paths

    def OSM_File_Find_From_CacheIndex(self,bounds=[],precision=0.1):
        if bounds and Path(self.Index_File).exists():
            polygon1=box(*bounds)
            with open(self.Index_File,'r') as f:
                lines=f.readlines()
                for line in lines:
                    geodata=json.loads(line)
                    x_precision = abs(geodata['bounds'][2]-geodata['bounds'][0])*precision
                    y_precision = abs(geodata['bounds'][3] - geodata['bounds'][1]) * precision
                    bx=[geodata['bounds'][0]+x_precision,geodata['bounds'][1]+y_precision,geodata['bounds'][2]-x_precision,geodata['bounds'][3]-y_precision]
                    polygon2=box(*bx)
                    if polygon2.contains(polygon1):
                        return geodata['filepath'],box(*geodata['bounds'])
        return None,None

    def json_to_graph(self,polygon,json_contents=[],
    json_filepaths=[],
    network_type="all_private",
    simplify=True,
    retain_all=False,
    truncate_by_edge=False,
    clean_periphery=True,
    custom_filter=None):

        if not json_contents and not json_filepaths:
            raise Exception("the json file is not exist")
        if not json_contents:
            for filepath in json_filepaths:
                with open(filepath,'r') as f:
                    json_content = json.load(f)
                    json_contents.append(json_content)

        if clean_periphery:
            # create a new buffered polygon 0.5km around the desired one
            buffer_dist = 500
            poly_proj, crs_utm = projection.project_geometry(polygon)
            poly_proj_buff = poly_proj.buffer(buffer_dist)
            poly_buff, _ = projection.project_geometry(poly_proj_buff, crs=crs_utm, to_latlong=True)

            # create buffered graph from the downloaded data
            bidirectional = network_type in settings.bidirectional_network_types
            G_buff = graph._create_graph(json_contents, retain_all=True, bidirectional=bidirectional)

            # truncate buffered graph to the buffered polygon and retain_all for
            # now. needed because overpass returns entire ways that also include
            # nodes outside the poly if the way (that is, a way with a single OSM
            # ID) has a node inside the poly at some point.
            G_buff = truncate.truncate_graph_polygon(G_buff, poly_buff, True, truncate_by_edge)

            # simplify the graph topology
            if simplify:
                G_buff = simplification.simplify_graph(G_buff)

            # truncate graph by original polygon to return graph within polygon
            # caller wants. don't simplify again: this allows us to retain
            # intersections along the street that may now only connect 2 street
            # segments in the network, but in reality also connect to an
            # intersection just outside the polygon
            G = truncate.truncate_graph_polygon(G_buff, polygon, retain_all, truncate_by_edge)

            # count how many physical streets in buffered graph connect to each
            # intersection in un-buffered graph, to retain true counts for each
            # intersection, even if some of its neighbors are outside the polygon
            spn = stats.count_streets_per_node(G_buff, nodes=G.nodes)
            nx.set_node_attributes(G, values=spn, name="street_count")

        # if clean_periphery=False, just use the polygon as provided
        else:

            # create graph from the downloaded data
            bidirectional = network_type in settings.bidirectional_network_types
            G = graph._create_graph(json_contents, retain_all=True, bidirectional=bidirectional)

            # truncate the graph to the extent of the polygon
            G = truncate.truncate_graph_polygon(G, polygon, retain_all, truncate_by_edge)

            # simplify the graph topology after truncation. don't truncate after
            # simplifying or you may have simplified out to an endpoint beyond the
            # truncation distance, which would strip out the entire edge
            if simplify:
                G = simplification.simplify_graph(G)

            # count how many physical streets connect to each intersection/deadend
            # note this will be somewhat inaccurate due to periphery effects, so
            # it's best to parameterize function with clean_periphery=True
            spn = stats.count_streets_per_node(G)
            nx.set_node_attributes(G, values=spn, name="street_count")
            msg = (
                "the graph-level street_count attribute will likely be inaccurate "
                "when you set clean_periphery=False"
            )
            warnings.warn(msg)

        utils.log(f"graph_from_polygon returned graph with {len(G)} nodes and {len(G.edges)} edges")

        return G

    def _osm_network_download(self,polygon, network_type, custom_filter):
        if custom_filter is not None:
            osm_filter = custom_filter
        else:
            osm_filter = downloader._get_osm_filter(network_type)

        response_file_paths = []

        # create overpass settings string
        overpass_settings = self._make_overpass_settings()

        # subdivide query polygon to get list of sub-divided polygon coord strings
        polygon_coord_strs = downloader._make_overpass_polygon_coord_strs(polygon)

        # pass each polygon exterior coordinates in the list to the API, one at a
        # time. The '>' makes it recurse so we get ways and the ways' nodes.
        for polygon_coord_str in polygon_coord_strs:
            query_str = f"{overpass_settings};(way{osm_filter}(poly:'{polygon_coord_str}');>;);out;"
            response_file_path  = self.overpass_request(data={"data": query_str})
            response_file_paths.append(response_file_path)

        if settings.cache_only_mode:  # pragma: no cover
            raise CacheOnlyModeInterrupt("settings.cache_only_mode=True")

        return response_file_paths

    def _make_overpass_settings(self):
        if settings.memory is None:
            maxsize = ""
        else:
            maxsize = f"[maxsize:{settings.memory}]"
        return OSM_Downloader.overpass_settings.format(FileType=OSM_Downloader.FileType,timeout=settings.timeout, maxsize=maxsize)

    def overpass_request(self,data, pause=None, error_pause=60):
        """
        Send a HTTP POST request to the Overpass API and return JSON response.

        Parameters
        ----------
        data : OrderedDict
            key-value pairs of parameters
        pause : int
            how long to pause in seconds before request, if None, will query API
            status endpoint to find when next slot is available
        error_pause : int
            how long to pause in seconds (in addition to `pause`) before re-trying
            request if error

        Returns
        -------
        response_path : pathlib.Path
        """
        base_endpoint = settings.overpass_endpoint

        # resolve url to same IP even if there is server round-robin redirecting
        downloader._config_dns(base_endpoint)

        # define the Overpass API URL, then construct a GET-style URL as a string to
        # hash to look up/save to cache
        url = base_endpoint.rstrip("/") + "/interpreter"
        prepared_url = requests.Request("GET", url, params=data).prepare().url

        # 重点：

        cached_response_path = self._retrieve_from_cache(prepared_url, check_remark=True)

        if cached_response_path is not None:
            # found response in the cache, return it instead of calling server
            return cached_response_path

        else:
            # if this URL is not already in the cache, pause, then request it
            self.File_Exist = False
            if pause is None:
                this_pause = downloader._get_pause(base_endpoint)
            utils.log(f"Pausing {this_pause} seconds before making HTTP POST request")
            time.sleep(this_pause)

            # transmit the HTTP POST request
            utils.log(f"Post {prepared_url} with timeout={settings.timeout}")
            headers = downloader._get_http_headers()
            response = requests.post(
                url, data=data, timeout=settings.timeout, headers=headers, **settings.requests_kwargs
            )
            sc = response.status_code

            # log the response size and domain
            size_kb = len(response.content) / 1000
            domain = re.findall(r"(?s)//(.*?)/", url)[0]
            utils.log(f"Downloaded {size_kb:,.1f}kB from {domain}")

            try:
                if OSM_Downloader.FileType == 'json':
                    response_content = response.json()
                else:
                    response_content =  response.content.decode('utf-8')
                if "remark" in response_content:
                    utils.log(f'Server remark', level=lg.WARNING)
            except Exception:  # pragma: no cover
                if sc in {429, 504}:
                    # 429 is 'too many requests' and 504 is 'gateway timeout' from
                    # server overload: handle these by pausing then recursively
                    # re-trying until we get a valid response from the server
                    this_pause = error_pause + downloader._get_pause(base_endpoint)
                    utils.log(f"{domain} returned {sc}: retry in {this_pause} secs", level=lg.WARNING)
                    time.sleep(this_pause)
                    cached_response_path = self.overpass_request(data, pause, error_pause)
                    return cached_response_path
                else:
                    # else, this was an unhandled status code, throw an exception
                    utils.log(f"{domain} returned {sc}", level=lg.ERROR)
                    raise Exception(f"Server returned\n{response} {response.reason}\n{response.text}")

            cached_response_path=self._save_to_cache(prepared_url, response_content, sc)
            return cached_response_path

    def _retrieve_from_cache(self,url, check_remark=False):
        """
        Retrieve a HTTP response JSON object from the cache, if it exists.

        Parameters
        ----------
        url : string
            the URL of the request
        check_remark : string
            if True, only return filepath if cached response does not have a
            remark key indicating a server warning

        Returns
        -------
        response_path : pathlib.Path
            cached response for url if it exists in the cache, otherwise None
        """
        # if the tool is configured to use the cache
        if settings.use_cache:

            # return cached response for this url if exists, otherwise return None
            cache_filepath = self._url_in_cache(url)

            if cache_filepath is not None:
                if OSM_Downloader.FileType == 'json':
                    response_content = json.loads(cache_filepath.read_text(encoding="utf-8"))
                else:
                    response_content = cache_filepath.read_text(encoding="utf-8")
                # return None if check_remark is True and there is a server
                # remark in the cached response
                if check_remark and "remark" in response_content:
                    utils.log(f'Found remark, so ignoring cache file "{cache_filepath}"')
                    return None

                utils.log(f'Retrieved response from cache file "{cache_filepath}"')
                return cache_filepath

    def _url_in_cache(self,url):
        """
        Determine if a URL's response exists in the cache.

        Calculates the checksum of url to determine the cache file's name.

        Parameters
        ----------
        url : string
            the URL to look for in the cache

        Returns
        -------
        filepath : pathlib.Path
            path to cached response for url if it exists, otherwise None
        """
        # hash the url to generate the cache filename
        filename = sha1(url.encode("utf-8")).hexdigest() + "."+OSM_Downloader.FileType
        filepath = Path(settings.cache_folder) / filename

        # if this file exists in the cache, return its full path
        return filepath if filepath.is_file() else None

    def _save_to_cache(self,url, response_content, sc):
        """
        Save a HTTP response object to a file in the cache folder.

        Function calculates the checksum of url to generate the cache file's name.
        If the request was sent to server via POST instead of GET, then URL should
        be a GET-style representation of request. Response is only saved to a
        cache file if settings.use_cache is True, response_path is not None, and
        sc = 200.

        Users should always pass OrderedDicts instead of dicts of parameters into
        request functions, so the parameters remain in the same order each time,
        producing the same URL string, and thus the same hash. Otherwise the cache
        will eventually contain multiple saved responses for the same request
        because the URL's parameters appeared in a different order each time.

        Parameters
        ----------
        url : string
            the URL of the request
        response_content : json or text(string)
            the response content
        sc : int
            the response's HTTP status code

        Returns
        -------
        None
        """
        if settings.use_cache:

            if sc != 200:
                utils.log(f"Did not save to cache because status code is {sc}")

            elif response_content is None:
                utils.log("Did not save to cache because response_path is None")

            else:
                # create the folder on the disk if it doesn't already exist
                cache_folder = Path(settings.cache_folder)
                cache_folder.mkdir(parents=True, exist_ok=True)

                # hash the url to make the filename succinct but unique
                # sha1 digest is 160 bits = 20 bytes = 40 hexadecimal characters
                filename = sha1(url.encode("utf-8")).hexdigest() + "."+OSM_Downloader.FileType
                cache_filepath = cache_folder / filename

                # dump to json, and save to file
                if OSM_Downloader.FileType == 'json':
                    cache_filepath.write_text(json.dumps(response_content,ensure_ascii=False), encoding="utf-8")
                else:
                    cache_filepath.write_text(response_content, encoding="utf-8")

                utils.log(f'Saved response to cache file "{cache_filepath}"')
                return cache_filepath