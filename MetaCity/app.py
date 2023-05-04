from flask import Flask,jsonify,url_for,request,redirect,render_template
import osmnx as ox
import config
from Mininet_WIFI.Network_Topology_Generator import Network_Topology_Generator
from Mininet_WIFI.Route_Generator import Route_Generator
from Mininet_WIFI.Perform_Emulation import Perform_Emulation
from Mininet_WIFI.QoS_Statistics_Generator import QoS_Statistics_Generator
import json
from OSM_Map.Edge_Computing_Application import EdgeComputingApplication
import os

app = Flask(__name__)

app.config.from_object(config)

eapp=EdgeComputingApplication(title='test',location=[39.90733207991023,116.39126356336165])
eapp.output(r'templates/index.html')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/geocode/', methods=['GET','POST'])
def geocode():
    ox.plot_route_folium()
    if request.method == 'GET':
        location= request.args.get('location')
    elif request.method == 'POST':
        location=request.form.get('location')
    geocode=list(ox.geocode(location))
    output={"location":geocode}
    return jsonify(output)

@app.route('/network_topolog/', methods=['POST'])
def network_topolog():

    data=None
    datas={}
    print(data)
    if request.method == 'POST':
        data=request.json
    if data:
        nt = Network_Topology_Generator()
        datas.update(nt.generate(network_topology=data))
        datas.update({"state":'success'})
        print(datas)
        return jsonify(datas)
    else:
        datas.update({"state": 'fail'})
        return jsonify(datas)

@app.route('/generate_routes/', methods=['POST'])
def generate_routes():
    data=None
    datas={}
    if request.method == 'POST':
        data=request.json

    if data:
        rg = Route_Generator()
        datas.update(rg.generate_routes(loaction=data))
        datas.update({"state":'success'})
        print(datas)
        return jsonify(datas)
    else:
        datas.update({"state": 'fail'})
        return jsonify(datas)

@app.route('/emulation/', methods=['POST'])
def emulate_network():
    data=None
    datas={}
    if request.method == 'POST':
        data=request.json
        print(data)
    if data:
        print("Begin Emulation")
        datas.update({"situations": []})
        for d in data:
            if d.get('filename',None):
                pe=Perform_Emulation(filename=d.get('filename',None))
                status = pe.perform()
                if status:

                    datas["situations"].append({'filename':d.get('filename',None),'status':"success"})

                else:

                    datas["situations"].append({'filename':d.get('filename',None),'status':"fail"})

        datas.update({"state":'success'})
        # with open('3.json', 'r', encoding='utf-8') as f:
        #     datas.update({"outcome":json.load(f)})
        print(datas)
        return jsonify(datas)
    else:
        datas.update({"state": 'fail'})
        return jsonify(datas)

@app.route('/check_emulation_status/', methods=['POST'])
def check_emulation_status():
    data=None
    datas={}
    if request.method == 'POST':
        data=request.json
    # datas={'statistics': [{'filename': 'Network_Topology_20221108215146020078.py', 'chart': {'mp0': {'delay': {'$schema': 'https://vega.github.io/schema/vega/v5.json', 'description': 'A basic line.', 'width': 500, 'height': 200, 'padding': 5, 'signals': [{'name': 'interpolate', 'value': 'linear', 'bind': {'input': 'select', 'options': ['basis', 'cardinal', 'catmull-rom', 'linear', 'monotone', 'natural', 'step', 'step-after', 'step-before']}}], 'data': [{'name': 'table', 'values': [{'x': 0.0, 'y': -1, 'c': 'ec0'}, {'x': 3.09, 'y': 4.0895, 'c': 'ec0'}, {'x': 3.11, 'y': 1.428, 'c': 'ec0'}, {'x': 3.12, 'y': 1.412, 'c': 'ec0'}, {'x': 3.15, 'y': 1.318, 'c': 'ec0'}, {'x': 3.17, 'y': 1.095, 'c': 'ec0'}, {'x': 3.18, 'y': 1.4585, 'c': 'ec0'}, {'x': 3.2, 'y': 1.4395, 'c': 'ec0'}, {'x': 3.22, 'y': 1.4115, 'c': 'ec0'}, {'x': 3.23, 'y': 1.3055, 'c': 'ec0'}, {'x': 3.25, 'y': 1.2265, 'c': 'ec0'}, {'x': 3.27, 'y': 1.29, 'c': 'ec0'}, {'x': 3.28, 'y': 1.1935, 'c': 'ec0'}, {'x': 3.3, 'y': 1.2185, 'c': 'ec0'}, {'x': 3.31, 'y': 1.4225, 'c': 'ec0'}, {'x': 3.33, 'y': 1.5345, 'c': 'ec0'}, {'x': 3.34, 'y': 1.2775, 'c': 'ec0'}, {'x': 3.36, 'y': 1.3305, 'c': 'ec0'}, {'x': 3.37, 'y': 1.337, 'c': 'ec0'}, {'x': 3.39, 'y': 1.511, 'c': 'ec0'}, {'x': 3.4, 'y': 1.4635, 'c': 'ec0'}, {'x': 3.42, 'y': 1.485, 'c': 'ec0'}, {'x': 3.43, 'y': 1.1445, 'c': 'ec0'}, {'x': 3.44, 'y': 1.2635, 'c': 'ec0'}, {'x': 3.46, 'y': 1.3005, 'c': 'ec0'}, {'x': 3.47, 'y': 1.3795, 'c': 'ec0'}, {'x': 3.49, 'y': 1.354, 'c': 'ec0'}, {'x': 3.51, 'y': 1.379, 'c': 'ec0'}, {'x': 3.53, 'y': 1.276, 'c': 'ec0'}, {'x': 3.54, 'y': 1.1045, 'c': 'ec0'}, {'x': 3.56, 'y': 1.5295, 'c': 'ec0'}, {'x': 3.57, 'y': 1.457, 'c': 'ec0'}, {'x': 3.59, 'y': 1.4945, 'c': 'ec0'}, {'x': 3.6, 'y': 1.3615, 'c': 'ec0'}, {'x': 3.61, 'y': 1.3585, 'c': 'ec0'}, {'x': 3.63, 'y': 1.304, 'c': 'ec0'}, {'x': 3.65, 'y': 1.2705, 'c': 'ec0'}, {'x': 3.67, 'y': 1.4115, 'c': 'ec0'}, {'x': 3.69, 'y': 1.1365, 'c': 'ec0'}, {'x': 3.71, 'y': 1.5325, 'c': 'ec0'}, {'x': 3.72, 'y': 1.31, 'c': 'ec0'}, {'x': 3.74, 'y': 1.2465, 'c': 'ec0'}, {'x': 3.75, 'y': 1.53, 'c': 'ec0'}, {'x': 3.76, 'y': 1.346, 'c': 'ec0'}, {'x': 3.78, 'y': 1.344, 'c': 'ec0'}, {'x': 3.79, 'y': 1.1775, 'c': 'ec0'}, {'x': 3.81, 'y': 1.3985, 'c': 'ec0'}, {'x': 3.83, 'y': 1.3275, 'c': 'ec0'}, {'x': 3.84, 'y': 1.5065, 'c': 'ec0'}, {'x': 3.86, 'y': 1.3605, 'c': 'ec0'}, {'x': 3.87, 'y': 1.4675, 'c': 'ec0'}, {'x': 3.89, 'y': 1.154, 'c': 'ec0'}, {'x': 3.9, 'y': 1.2365, 'c': 'ec0'}, {'x': 3.92, 'y': 1.4115, 'c': 'ec0'}, {'x': 3.94, 'y': 1.2135, 'c': 'ec0'}, {'x': 3.96, 'y': 1.213, 'c': 'ec0'}, {'x': 3.97, 'y': 1.3665, 'c': 'ec0'}, {'x': 3.99, 'y': 1.302, 'c': 'ec0'}, {'x': 4.01, 'y': 1.1685, 'c': 'ec0'}, {'x': 4.02, 'y': 1.3855, 'c': 'ec0'}, {'x': 4.04, 'y': 1.383, 'c': 'ec0'}, {'x': 4.05, 'y': 1.272, 'c': 'ec0'}, {'x': 4.06, 'y': 1.473, 'c': 'ec0'}, {'x': 4.08, 'y': 1.3285, 'c': 'ec0'}, {'x': 4.09, 'y': 1.426, 'c': 'ec0'}, {'x': 4.11, 'y': 1.308, 'c': 'ec0'}, {'x': 4.12, 'y': 1.4585, 'c': 'ec0'}, {'x': 4.13, 'y': 1.422, 'c': 'ec0'}, {'x': 4.15, 'y': 1.3675, 'c': 'ec0'}, {'x': 4.18, 'y': 1.3525, 'c': 'ec0'}, {'x': 4.2, 'y': 1.133, 'c': 'ec0'}, {'x': 4.21, 'y': 1.3445, 'c': 'ec0'}, {'x': 4.23, 'y': 1.529, 'c': 'ec0'}, {'x': 4.24, 'y': 1.3695, 'c': 'ec0'}, {'x': 4.26, 'y': 1.1675, 'c': 'ec0'}, {'x': 4.27, 'y': 1.3595, 'c': 'ec0'}, {'x': 4.29, 'y': 1.3105, 'c': 'ec0'}, {'x': 4.3, 'y': 1.3685, 'c': 'ec0'}, {'x': 4.32, 'y': 1.3795, 'c': 'ec0'}, {'x': 4.34, 'y': 1.112, 'c': 'ec0'}, {'x': 4.35, 'y': 1.5105, 'c': 'ec0'}, {'x': 4.36, 'y': 1.5105, 'c': 'ec0'}, {'x': 4.38, 'y': 1.4465, 'c': 'ec0'}, {'x': 4.39, 'y': 1.1815, 'c': 'ec0'}, {'x': 4.41, 'y': 1.2755, 'c': 'ec0'}, {'x': 4.43, 'y': 1.471, 'c': 'ec0'}, {'x': 4.44, 'y': 1.488, 'c': 'ec0'}, {'x': 4.45, 'y': 1.4575, 'c': 'ec0'}, {'x': 4.47, 'y': 1.1665, 'c': 'ec0'}, {'x': 4.48, 'y': 1.145, 'c': 'ec0'}, {'x': 4.5, 'y': 1.1795, 'c': 'ec0'}, {'x': 4.51, 'y': 1.345, 'c': 'ec0'}, {'x': 4.53, 'y': 1.1035, 'c': 'ec0'}, {'x': 4.55, 'y': 1.3435, 'c': 'ec0'}, {'x': 4.56, 'y': 1.2115, 'c': 'ec0'}, {'x': 4.58, 'y': 1.247, 'c': 'ec0'}, {'x': 4.6, 'y': 1.418, 'c': 'ec0'}, {'x': 4.61, 'y': 1.379, 'c': 'ec0'}, {'x': 4.63, 'y': 1.431, 'c': 'ec0'}, {'x': 4.64, 'y': 1.1795, 'c': 'ec0'}, {'x': 4.65, 'y': 1.5335, 'c': 'ec0'}, {'x': 4.67, 'y': 1.4585, 'c': 'ec0'}, {'x': 4.68, 'y': 1.208, 'c': 'ec0'}, {'x': 4.7, 'y': 1.318, 'c': 'ec0'}, {'x': 4.71, 'y': 1.245, 'c': 'ec0'}, {'x': 4.73, 'y': 1.2225, 'c': 'ec0'}, {'x': 4.75, 'y': 1.477, 'c': 'ec0'}, {'x': 4.76, 'y': 1.234, 'c': 'ec0'}, {'x': 4.77, 'y': 1.094, 'c': 'ec0'}, {'x': 4.79, 'y': 1.405, 'c': 'ec0'}, {'x': 4.8, 'y': 1.219, 'c': 'ec0'}, {'x': 4.82, 'y': 1.433, 'c': 'ec0'}, {'x': 4.84, 'y': 1.4605, 'c': 'ec0'}, {'x': 4.85, 'y': 1.5405, 'c': 'ec0'}, {'x': 4.86, 'y': 1.484, 'c': 'ec0'}, {'x': 4.88, 'y': 1.142, 'c': 'ec0'}, {'x': 4.89, 'y': 1.451, 'c': 'ec0'}, {'x': 4.91, 'y': 1.106, 'c': 'ec0'}, {'x': 4.92, 'y': 1.372, 'c': 'ec0'}, {'x': 4.93, 'y': 1.265, 'c': 'ec0'}, {'x': 4.95, 'y': 1.524, 'c': 'ec0'}, {'x': 4.97, 'y': 1.23, 'c': 'ec0'}, {'x': 4.98, 'y': 1.3185, 'c': 'ec0'}, {'x': 5.0, 'y': 1.35, 'c': 'ec0'}, {'x': 5.01, 'y': 1.1335, 'c': 'ec0'}, {'x': 5.03, 'y': 1.2185, 'c': 'ec0'}, {'x': 5.05, 'y': 1.3565, 'c': 'ec0'}, {'x': 5.06, 'y': 1.439, 'c': 'ec0'}, {'x': 5.08, 'y': 1.3025, 'c': 'ec0'}, {'x': 5.09, 'y': 1.3765, 'c': 'ec0'}, {'x': 5.1, 'y': 1.416, 'c': 'ec0'}, {'x': 5.12, 'y': 1.475, 'c': 'ec0'}, {'x': 5.13, 'y': 1.491, 'c': 'ec0'}, {'x': 5.15, 'y': 1.321, 'c': 'ec0'}, {'x': 5.16, 'y': 1.338, 'c': 'ec0'}, {'x': 5.18, 'y': 1.1995, 'c': 'ec0'}, {'x': 5.19, 'y': 1.19, 'c': 'ec0'}, {'x': 5.21, 'y': 1.1815, 'c': 'ec0'}, {'x': 5.23, 'y': 1.1895, 'c': 'ec0'}, {'x': 5.24, 'y': 1.3995, 'c': 'ec0'}, {'x': 5.26, 'y': 1.4615, 'c': 'ec0'}, {'x': 5.27, 'y': 1.3145, 'c': 'ec0'}, {'x': 5.29, 'y': 1.184, 'c': 'ec0'}, {'x': 5.3, 'y': 1.1325, 'c': 'ec0'}, {'x': 5.31, 'y': 1.4715, 'c': 'ec0'}, {'x': 5.33, 'y': 1.185, 'c': 'ec0'}, {'x': 5.35, 'y': 1.276, 'c': 'ec0'}, {'x': 5.37, 'y': 1.3545, 'c': 'ec0'}, {'x': 5.38, 'y': 1.4965, 'c': 'ec0'}, {'x': 5.4, 'y': 1.341, 'c': 'ec0'}, {'x': 5.41, 'y': 1.432, 'c': 'ec0'}, {'x': 5.42, 'y': 1.4095, 'c': 'ec0'}, {'x': 5.44, 'y': 1.4585, 'c': 'ec0'}, {'x': 5.45, 'y': 1.4435, 'c': 'ec0'}, {'x': 5.47, 'y': 1.283, 'c': 'ec0'}, {'x': 5.48, 'y': 1.4625, 'c': 'ec0'}, {'x': 5.5, 'y': 1.2245, 'c': 'ec0'}, {'x': 5.51, 'y': 1.3725, 'c': 'ec0'}, {'x': 5.53, 'y': 1.49, 'c': 'ec0'}, {'x': 5.55, 'y': 1.2105, 'c': 'ec0'}, {'x': 5.56, 'y': 1.2075, 'c': 'ec0'}, {'x': 5.58, 'y': 1.2795, 'c': 'ec0'}, {'x': 5.59, 'y': 1.1635, 'c': 'ec0'}, {'x': 5.61, 'y': 1.244, 'c': 'ec0'}, {'x': 5.62, 'y': 1.4795, 'c': 'ec0'}, {'x': 5.64, 'y': 1.4935, 'c': 'ec0'}, {'x': 5.65, 'y': 1.464, 'c': 'ec0'}, {'x': 5.67, 'y': 1.3555, 'c': 'ec0'}, {'x': 5.68, 'y': 1.296, 'c': 'ec0'}, {'x': 5.7, 'y': 1.232, 'c': 'ec0'}, {'x': 5.71, 'y': 1.4885, 'c': 'ec0'}, {'x': 5.72, 'y': 1.123, 'c': 'ec0'}, {'x': 5.74, 'y': 1.319, 'c': 'ec0'}, {'x': 5.75, 'y': 1.5095, 'c': 'ec0'}, {'x': 5.77, 'y': 1.482, 'c': 'ec0'}, {'x': 5.78, 'y': 1.5375, 'c': 'ec0'}, {'x': 5.8, 'y': 1.3255, 'c': 'ec0'}, {'x': 5.81, 'y': 1.1685, 'c': 'ec0'}, {'x': 5.82, 'y': 1.325, 'c': 'ec0'}, {'x': 5.84, 'y': 1.1345, 'c': 'ec0'}, {'x': 5.85, 'y': 1.116, 'c': 'ec0'}, {'x': 5.87, 'y': 1.4235, 'c': 'ec0'}, {'x': 5.88, 'y': 1.4895, 'c': 'ec0'}, {'x': 5.9, 'y': 1.1935, 'c': 'ec0'}, {'x': 5.91, 'y': 1.178, 'c': 'ec0'}, {'x': 5.92, 'y': 1.235, 'c': 'ec0'}, {'x': 5.94, 'y': 1.494, 'c': 'ec0'}, {'x': 5.96, 'y': 1.1365, 'c': 'ec0'}, {'x': 5.98, 'y': 1.1435, 'c': 'ec0'}, {'x': 5.99, 'y': 1.3315, 'c': 'ec0'}, {'x': 6.01, 'y': 1.27, 'c': 'ec0'}, {'x': 6.02, 'y': 1.3525, 'c': 'ec0'}, {'x': 6.04, 'y': 1.4145, 'c': 'ec0'}, {'x': 6.05, 'y': 1.3325, 'c': 'ec0'}, {'x': 6.07, 'y': 1.2015, 'c': 'ec0'}, {'x': 6.09, 'y': 1.0925, 'c': 'ec0'}, {'x': 6.1, 'y': 1.1905, 'c': 'ec0'}, {'x': 6.12, 'y': 1.499, 'c': 'ec0'}, {'x': 6.14, 'y': 1.1655, 'c': 'ec0'}, {'x': 6.15, 'y': 1.318, 'c': 'ec0'}, {'x': 6.17, 'y': 1.316, 'c': 'ec0'}, {'x': 6.18, 'y': 1.397, 'c': 'ec0'}, {'x': 6.19, 'y': 1.534, 'c': 'ec0'}, {'x': 6.21, 'y': 1.243, 'c': 'ec0'}, {'x': 6.22, 'y': 1.19, 'c': 'ec0'}, {'x': 6.24, 'y': 1.218, 'c': 'ec0'}, {'x': 6.25, 'y': 1.132, 'c': 'ec0'}, {'x': 6.27, 'y': 1.2295, 'c': 'ec0'}, {'x': 6.28, 'y': 1.3625, 'c': 'ec0'}, {'x': 6.3, 'y': 1.4325, 'c': 'ec0'}, {'x': 6.31, 'y': 1.354, 'c': 'ec0'}, {'x': 6.33, 'y': 1.2225, 'c': 'ec0'}, {'x': 6.34, 'y': 1.3665, 'c': 'ec0'}, {'x': 6.35, 'y': 1.2715, 'c': 'ec0'}, {'x': 6.37, 'y': 1.3255, 'c': 'ec0'}, {'x': 6.38, 'y': 1.4115, 'c': 'ec0'}, {'x': 6.4, 'y': 1.1725, 'c': 'ec0'}, {'x': 6.41, 'y': 1.5125, 'c': 'ec0'}, {'x': 6.43, 'y': 1.4445, 'c': 'ec0'}, {'x': 6.44, 'y': 1.432, 'c': 'ec0'}, {'x': 6.46, 'y': 1.26, 'c': 'ec0'}, {'x': 6.47, 'y': 1.42, 'c': 'ec0'}, {'x': 6.49, 'y': 1.4265, 'c': 'ec0'}, {'x': 6.5, 'y': 1.254, 'c': 'ec0'}, {'x': 6.52, 'y': 1.441, 'c': 'ec0'}, {'x': 6.54, 'y': 1.128, 'c': 'ec0'}, {'x': 6.55, 'y': 1.385, 'c': 'ec0'}, {'x': 6.57, 'y': 1.23, 'c': 'ec0'}, {'x': 6.58, 'y': 1.113, 'c': 'ec0'}, {'x': 6.6, 'y': 1.3435, 'c': 'ec0'}, {'x': 6.62, 'y': 1.1015, 'c': 'ec0'}, {'x': 6.63, 'y': 1.4425, 'c': 'ec0'}, {'x': 6.64, 'y': 1.3025, 'c': 'ec0'}, {'x': 6.66, 'y': 1.4855, 'c': 'ec0'}, {'x': 6.68, 'y': 1.274, 'c': 'ec0'}, {'x': 6.69, 'y': 1.1485, 'c': 'ec0'}, {'x': 6.71, 'y': 1.4385, 'c': 'ec0'}, {'x': 6.72, 'y': 1.367, 'c': 'ec0'}, {'x': 6.74, 'y': 1.4, 'c': 'ec0'}, {'x': 6.75, 'y': 1.5045, 'c': 'ec0'}, {'x': 6.78, 'y': 1.0965, 'c': 'ec0'}, {'x': 6.79, 'y': 1.5165, 'c': 'ec0'}, {'x': 6.81, 'y': 1.429, 'c': 'ec0'}, {'x': 6.82, 'y': 1.406, 'c': 'ec0'}, {'x': 6.84, 'y': 1.361, 'c': 'ec0'}, {'x': 6.85, 'y': 1.3155, 'c': 'ec0'}, {'x': 6.86, 'y': 1.1855, 'c': 'ec0'}, {'x': 6.88, 'y': 1.3665, 'c': 'ec0'}, {'x': 6.9, 'y': 1.2605, 'c': 'ec0'}, {'x': 6.91, 'y': 1.3265, 'c': 'ec0'}, {'x': 6.93, 'y': 1.2975, 'c': 'ec0'}, {'x': 6.94, 'y': 1.283, 'c': 'ec0'}, {'x': 6.96, 'y': 1.2155, 'c': 'ec0'}, {'x': 6.97, 'y': 1.116, 'c': 'ec0'}, {'x': 6.99, 'y': 1.2125, 'c': 'ec0'}, {'x': 7.0, 'y': 1.1545, 'c': 'ec0'}, {'x': 7.02, 'y': 1.1475, 'c': 'ec0'}, {'x': 7.04, 'y': 1.2055, 'c': 'ec0'}, {'x': 7.06, 'y': 1.1875, 'c': 'ec0'}, {'x': 7.08, 'y': 1.5045, 'c': 'ec0'}, {'x': 7.1, 'y': 1.3105, 'c': 'ec0'}, {'x': 7.12, 'y': 1.366, 'c': 'ec0'}, {'x': 7.13, 'y': 1.243, 'c': 'ec0'}, {'x': 7.15, 'y': 1.5465, 'c': 'ec0'}, {'x': 7.17, 'y': 1.5415, 'c': 'ec0'}, {'x': 7.18, 'y': 1.277, 'c': 'ec0'}, {'x': 7.2, 'y': 1.408, 'c': 'ec0'}, {'x': 7.22, 'y': 1.445, 'c': 'ec0'}, {'x': 7.23, 'y': 1.276, 'c': 'ec0'}, {'x': 7.25, 'y': 1.1335, 'c': 'ec0'}, {'x': 7.26, 'y': 1.497, 'c': 'ec0'}, {'x': 7.28, 'y': 1.1695, 'c': 'ec0'}, {'x': 7.3, 'y': 1.451, 'c': 'ec0'}, {'x': 7.31, 'y': 1.5015, 'c': 'ec0'}, {'x': 7.33, 'y': 1.3945, 'c': 'ec0'}, {'x': 7.35, 'y': 1.4505, 'c': 'ec0'}, {'x': 7.37, 'y': 1.153, 'c': 'ec0'}, {'x': 7.38, 'y': 1.3105, 'c': 'ec0'}, {'x': 7.39, 'y': 1.105, 'c': 'ec0'}, {'x': 7.41, 'y': 1.4085, 'c': 'ec0'}, {'x': 7.43, 'y': 1.2885, 'c': 'ec0'}, {'x': 7.44, 'y': 1.485, 'c': 'ec0'}, {'x': 7.45, 'y': 1.539, 'c': 'ec0'}, {'x': 7.47, 'y': 1.2915, 'c': 'ec0'}, {'x': 7.48, 'y': 1.1445, 'c': 'ec0'}, {'x': 7.5, 'y': 1.439, 'c': 'ec0'}, {'x': 7.51, 'y': 1.3355, 'c': 'ec0'}, {'x': 7.53, 'y': 1.3035, 'c': 'ec0'}, {'x': 7.54, 'y': 1.5395, 'c': 'ec0'}, {'x': 7.56, 'y': 1.5405, 'c': 'ec0'}, {'x': 7.58, 'y': 1.3755, 'c': 'ec0'}, {'x': 7.59, 'y': 1.2465, 'c': 'ec0'}, {'x': 7.62, 'y': 1.188, 'c': 'ec0'}, {'x': 7.64, 'y': 1.352, 'c': 'ec0'}, {'x': 7.66, 'y': 1.2405, 'c': 'ec0'}, {'x': 7.68, 'y': 1.529, 'c': 'ec0'}, {'x': 7.69, 'y': 1.531, 'c': 'ec0'}, {'x': 7.72, 'y': 1.1615, 'c': 'ec0'}, {'x': 7.73, 'y': 1.295, 'c': 'ec0'}, {'x': 7.75, 'y': 1.1135, 'c': 'ec0'}, {'x': 7.76, 'y': 1.152, 'c': 'ec0'}, {'x': 7.78, 'y': 1.2935, 'c': 'ec0'}, {'x': 7.79, 'y': 1.12, 'c': 'ec0'}, {'x': 7.81, 'y': 1.346, 'c': 'ec0'}, {'x': 7.83, 'y': 1.4455, 'c': 'ec0'}, {'x': 7.84, 'y': 1.4185, 'c': 'ec0'}, {'x': 7.86, 'y': 1.479, 'c': 'ec0'}, {'x': 7.88, 'y': 1.4595, 'c': 'ec0'}, {'x': 7.89, 'y': 1.2175, 'c': 'ec0'}, {'x': 7.91, 'y': 1.4055, 'c': 'ec0'}, {'x': 7.92, 'y': 1.12, 'c': 'ec0'}, {'x': 7.94, 'y': 1.4355, 'c': 'ec0'}, {'x': 7.95, 'y': 1.303, 'c': 'ec0'}, {'x': 7.97, 'y': 1.141, 'c': 'ec0'}, {'x': 7.98, 'y': 1.334, 'c': 'ec0'}, {'x': 8.0, 'y': 1.2805, 'c': 'ec0'}, {'x': 8.01, 'y': 1.102, 'c': 'ec0'}, {'x': 8.03, 'y': 1.3775, 'c': 'ec0'}, {'x': 8.05, 'y': 1.2265, 'c': 'ec0'}, {'x': 8.07, 'y': 1.157, 'c': 'ec0'}, {'x': 8.09, 'y': 1.405, 'c': 'ec0'}, {'x': 8.11, 'y': 1.31, 'c': 'ec0'}, {'x': 8.13, 'y': 1.152, 'c': 'ec0'}, {'x': 8.14, 'y': 1.384, 'c': 'ec0'}, {'x': 8.16, 'y': 1.1825, 'c': 'ec0'}, {'x': 8.17, 'y': 1.2925, 'c': 'ec0'}, {'x': 8.18, 'y': 1.4005, 'c': 'ec0'}, {'x': 8.2, 'y': 1.411, 'c': 'ec0'}, {'x': 8.21, 'y': 1.445, 'c': 'ec0'}, {'x': 8.22, 'y': 1.4905, 'c': 'ec0'}, {'x': 8.24, 'y': 1.144, 'c': 'ec0'}, {'x': 8.26, 'y': 1.11, 'c': 'ec0'}, {'x': 8.28, 'y': 1.3305, 'c': 'ec0'}, {'x': 8.29, 'y': 1.206, 'c': 'ec0'}, {'x': 8.32, 'y': 1.127, 'c': 'ec0'}, {'x': 8.33, 'y': 1.187, 'c': 'ec0'}, {'x': 8.35, 'y': 1.2495, 'c': 'ec0'}, {'x': 8.38, 'y': 1.392, 'c': 'ec0'}, {'x': 8.39, 'y': 1.2695, 'c': 'ec0'}, {'x': 8.41, 'y': 1.2775, 'c': 'ec0'}, {'x': 8.43, 'y': 1.2995, 'c': 'ec0'}, {'x': 8.45, 'y': 1.212, 'c': 'ec0'}, {'x': 8.47, 'y': 1.229, 'c': 'ec0'}, {'x': 8.49, 'y': 1.2885, 'c': 'ec0'}, {'x': 8.5, 'y': 1.2295, 'c': 'ec0'}, {'x': 8.52, 'y': 1.1845, 'c': 'ec0'}, {'x': 8.54, 'y': 1.32, 'c': 'ec0'}, {'x': 8.55, 'y': 1.453, 'c': 'ec0'}, {'x': 8.57, 'y': 1.344, 'c': 'ec0'}, {'x': 8.58, 'y': 1.4015, 'c': 'ec0'}, {'x': 8.6, 'y': 1.429, 'c': 'ec0'}, {'x': 8.62, 'y': 1.408, 'c': 'ec0'}, {'x': 8.63, 'y': 1.275, 'c': 'ec0'}, {'x': 8.65, 'y': 1.122, 'c': 'ec0'}, {'x': 8.67, 'y': 1.3555, 'c': 'ec0'}, {'x': 8.68, 'y': 1.1865, 'c': 'ec0'}, {'x': 8.7, 'y': 1.2565, 'c': 'ec0'}, {'x': 8.72, 'y': 1.24, 'c': 'ec0'}, {'x': 8.74, 'y': 1.391, 'c': 'ec0'}, {'x': 8.75, 'y': 1.148, 'c': 'ec0'}, {'x': 8.77, 'y': 1.177, 'c': 'ec0'}, {'x': 8.78, 'y': 1.3475, 'c': 'ec0'}, {'x': 8.8, 'y': 1.495, 'c': 'ec0'}, {'x': 8.81, 'y': 1.188, 'c': 'ec0'}, {'x': 8.84, 'y': 1.3845, 'c': 'ec0'}, {'x': 8.85, 'y': 1.399, 'c': 'ec0'}, {'x': 8.87, 'y': 1.3375, 'c': 'ec0'}, {'x': 8.88, 'y': 1.238, 'c': 'ec0'}, {'x': 8.9, 'y': 1.455, 'c': 'ec0'}, {'x': 8.92, 'y': 1.234, 'c': 'ec0'}, {'x': 8.94, 'y': 1.2705, 'c': 'ec0'}, {'x': 8.95, 'y': 1.5245, 'c': 'ec0'}, {'x': 8.97, 'y': 1.391, 'c': 'ec0'}, {'x': 8.99, 'y': 1.439, 'c': 'ec0'}, {'x': 9.01, 'y': 1.423, 'c': 'ec0'}, {'x': 9.02, 'y': 1.44, 'c': 'ec0'}, {'x': 9.04, 'y': 1.3095, 'c': 'ec0'}, {'x': 9.05, 'y': 1.2875, 'c': 'ec0'}, {'x': 9.07, 'y': 1.4165, 'c': 'ec0'}, {'x': 9.09, 'y': 1.195, 'c': 'ec0'}, {'x': 9.12, 'y': 1.146, 'c': 'ec0'}, {'x': 9.13, 'y': 1.1645, 'c': 'ec0'}, {'x': 9.15, 'y': 1.394, 'c': 'ec0'}, {'x': 9.17, 'y': 1.3885, 'c': 'ec0'}, {'x': 9.19, 'y': 1.122, 'c': 'ec0'}, {'x': 9.2, 'y': 1.297, 'c': 'ec0'}, {'x': 9.22, 'y': 1.537, 'c': 'ec0'}, {'x': 9.23, 'y': 1.3365, 'c': 'ec0'}, {'x': 9.24, 'y': 1.299, 'c': 'ec0'}, {'x': 9.26, 'y': 1.2905, 'c': 'ec0'}, {'x': 9.27, 'y': 1.355, 'c': 'ec0'}, {'x': 9.29, 'y': 1.2225, 'c': 'ec0'}, {'x': 9.31, 'y': 1.2715, 'c': 'ec0'}, {'x': 9.32, 'y': 1.1115, 'c': 'ec0'}, {'x': 9.34, 'y': 1.452, 'c': 'ec0'}, {'x': 9.35, 'y': 1.372, 'c': 'ec0'}, {'x': 9.37, 'y': 1.24, 'c': 'ec0'}, {'x': 9.39, 'y': 1.39, 'c': 'ec0'}, {'x': 9.4, 'y': 1.3085, 'c': 'ec0'}, {'x': 9.41, 'y': 1.2785, 'c': 'ec0'}, {'x': 9.43, 'y': 1.372, 'c': 'ec0'}, {'x': 9.45, 'y': 1.1825, 'c': 'ec0'}, {'x': 9.47, 'y': 1.3715, 'c': 'ec0'}, {'x': 9.48, 'y': 1.384, 'c': 'ec0'}, {'x': 9.5, 'y': 1.3665, 'c': 'ec0'}, {'x': 9.51, 'y': 1.3405, 'c': 'ec0'}, {'x': 9.53, 'y': 1.4485, 'c': 'ec0'}, {'x': 9.55, 'y': 1.337, 'c': 'ec0'}, {'x': 9.56, 'y': 1.3365, 'c': 'ec0'}, {'x': 9.57, 'y': 1.362, 'c': 'ec0'}, {'x': 9.59, 'y': 1.1535, 'c': 'ec0'}, {'x': 9.6, 'y': 1.191, 'c': 'ec0'}, {'x': 9.62, 'y': 1.4035, 'c': 'ec0'}, {'x': 9.63, 'y': 1.3705, 'c': 'ec0'}, {'x': 9.65, 'y': 1.528, 'c': 'ec0'}, {'x': 9.66, 'y': 1.411, 'c': 'ec0'}, {'x': 9.71, 'y': 1.554, 'c': 'ec0'}, {'x': 9.77, 'y': 1.3365, 'c': 'ec0'}, {'x': 9.84, 'y': 1.3965, 'c': 'ec0'}, {'x': 9.91, 'y': 1.374, 'c': 'ec0'}]}], 'scales': [{'name': 'x', 'type': 'point', 'range': 'width', 'domain': {'data': 'table', 'field': 'x'}}, {'name': 'y', 'type': 'linear', 'range': 'height', 'nice': True, 'zero': True, 'domain': {'data': 'table', 'field': 'y'}}, {'name': 'color', 'type': 'ordinal', 'range': 'category', 'domain': {'data': 'table', 'field': 'c'}}], 'axes': [{'orient': 'bottom', 'scale': 'x'}, {'orient': 'left', 'scale': 'y'}], 'marks': [{'type': 'group', 'from': {'facet': {'name': 'series', 'data': 'table', 'groupby': 'c'}}, 'marks': [{'type': 'line', 'from': {'data': 'series'}, 'encode': {'enter': {'x': {'scale': 'x', 'field': 'x'}, 'y': {'scale': 'y', 'field': 'y'}, 'stroke': {'scale': 'color', 'field': 'c'}, 'strokeWidth': {'value': 2}}, 'update': {'interpolate': {'signal': 'interpolate'}, 'strokeOpacity': {'value': 1}}, 'hover': {'strokeOpacity': {'value': 0.5}}}}]}]}}}}], 'state': 'success'}
    # datas={'statistics': [{'filename': 'Network_Topology_20221110152731698733.py', 'chart': {'mp0': {'delay': {'$schema': 'https://vega.github.io/schema/vega/v5.json', 'description': 'A basic line chart example.', 'width': 500, 'height': 200, 'padding': 5, 'signals': [{'name': 'interpolate', 'value': 'linear', 'bind': {'input': 'select', 'options': ['basis', 'cardinal', 'catmull-rom', 'linear', 'monotone', 'natural', 'step', 'step-after', 'step-before']}}], 'data': [{'name': 'table', 'values': [{'x': 0.0, 'y': -1, 'c': 'ec0'}, {'x': 3.27, 'y': 2.104, 'c': 'ec0'}, {'x': 3.35, 'y': 1.489, 'c': 'ec0'}, {'x': 3.43, 'y': 1.36, 'c': 'ec0'}, {'x': 3.51, 'y': 1.4, 'c': 'ec0'}, {'x': 3.58, 'y': 1.457, 'c': 'ec0'}, {'x': 3.66, 'y': 1.343, 'c': 'ec0'}, {'x': 3.73, 'y': 1.336, 'c': 'ec0'}, {'x': 3.88, 'y': 1.249, 'c': 'ec0'}, {'x': 3.97, 'y': 1.327, 'c': 'ec0'}]}], 'scales': [{'name': 'x', 'type': 'point', 'range': 'width', 'domain': {'data': 'table', 'field': 'x'}}, {'name': 'y', 'type': 'linear', 'range': 'height', 'nice': True, 'zero': True, 'domain': {'data': 'table', 'field': 'y'}}, {'name': 'color', 'type': 'ordinal', 'range': 'category', 'domain': {'data': 'table', 'field': 'c'}}], 'axes': [{'orient': 'bottom', 'scale': 'x'}, {'orient': 'left', 'scale': 'y'}], 'marks': [{'type': 'group', 'from': {'facet': {'name': 'series', 'data': 'table', 'groupby': 'c'}}, 'marks': [{'type': 'line', 'from': {'data': 'series'}, 'encode': {'enter': {'x': {'scale': 'x', 'field': 'x'}, 'y': {'scale': 'y', 'field': 'y'}, 'stroke': {'scale': 'color', 'field': 'c'}, 'strokeWidth': {'value': 2}}, 'update': {'interpolate': {'signal': 'interpolate'}, 'strokeOpacity': {'value': 1}}, 'hover': {'strokeOpacity': {'value': 0.5}}}}]}]}}}}], 'state': 'success'}
    # print(datas)
    # return jsonify(datas)
    if data:
        print(data)
        file=data['filename']
        aggregation=data['aggregation']
        qos=QoS_Statistics_Generator()
        datas.update({"statistics": []})
        for d in file:
            pe = Perform_Emulation(filename=d)
            status,filename=pe.check_status()
            if status:
                chart=qos.generate(filename=filename,precision=aggregation)
                datas["statistics"].append({"filename":d,'chart':chart})
                datas.update({"state": 'success'})
            else:
                datas.update({"state": 'fail'})
                break
        # print(datas)
        return jsonify(datas)
    else:
        datas.update({"state": 'fail'})
        return jsonify(datas)

@app.route('/map/',methods=['GET','POST'])
def map():  # put application's code here
    # name=request.form.get('name')
    # origin=request.form.get('origin')
    # destination=request.form.get('destination')
    # origin=ox.geocode(origin)
    # destination = ox.geocode(destination)
    # G = ox.graph_from_address(name, dist=10000)
    # G_84 = ox.project_graph(G , to_crs='EPSG:4326')
    # origin=ox.nearest_nodes(G_84,origin[1],origin[0])
    # destination= ox.nearest_nodes(G_84,destination[1], destination[0])
    # rou = ox.shortest_path(G_84, origin, destination)
    # m=ox.plot_graph_folium(G_84, tiles='openstreetmap',kwargs={'width':0.1})
    # m=ox.plot_route_folium(G_84,rou,route_map=m,weight=2, color="#8b0000")
    # m.save("templates/1.html")
    # return name
    return render_template('1.html')

@app.route('/test/',methods=['GET','POST'])
def test():
    return render_template("test.html")

if __name__ == '__main__':
    # app.debug = True
    app.run(debug=False,host='0.0.0.0',port=9000,processes=True)
