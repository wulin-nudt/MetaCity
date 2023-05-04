import datetime
import shutil
import os
import folium
import json
import copy
from pathlib import Path

class Template_Parse(object):

    type="linechart"

    def __init__(self,template='linechart.json',template_path=r'Mininet_WIFI/QoS_Index_Templates/'):

        self.template_data=None
        self.template=template

        template_file=template_path+template
        try:

            with open(template_file,"r") as f:
                self.template_data=json.load(f)

        except FileNotFoundError:
            print("the file " + template_file + " does not exist.")

    def configurate_sources(self,template=None,template_path=r'Mininet_WIFI/QoS_Index_Templates/'):
        self.template_data=None
        if template:
            self.template=template

        template_file=template_path+self.template

        with open(template_file,"r") as f:
            self.template_data=json.load(f)

    def store_chart(self,chart=None,x_title=None,y_title=None,path=r'datas/'):
        if not chart and not isinstance(chart,dict):
            return
        for k,v in chart.items():
            for k1,v1 in v.items():
                signals=v1.get('signals',None)
                Xtitle=''
                Ytitle = ''
                if signals and y_title and x_title:
                    for s in signals:
                        if s.get('name','')==y_title:
                            Ytitle=s.get('value','')
                        if s.get('name', '') == x_title:
                            Xtitle = s.get('value', '')
                values= v1.get('data',[])[0] if v1.get('data',[]) else {}
                values= values.get('values',[])
                data={'client':k,'type':k1,'x_title':Xtitle,'y_title':Ytitle,'data':values}
                data=json.dumps(data,indent=2)
                date = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
                filename=str(k)+"_"+str(k1)+"_"+date+'.json'
                if path:
                    filename=path+filename
                with open(filename,'w',newline='\n') as f:
                    f.write(data)

    # def parse(self,filename,flag='QoS',precision=1):
    #
    #     statistic_data=None
    #     template_data = self.template_data
    #
    #     if filename:
    #         try:
    #             with open(filename,'r') as f:
    #                 statistic_data = json.load(f).get(flag,None)
    #         except FileNotFoundError:
    #             print("the file " + filename + " does not exist.")
    #
    #     chart = {}
    #     if template_data and statistic_data:
    #         for client,servers in statistic_data.items():
    #             chart[client] = {}
    #             for server,datas in servers.items():
    #                 type_num = {}
    #                 for data in datas:
    #                     for t in data.get("type",None):
    #                         chart[client].setdefault(t,[])
    #                         type_num.setdefault(t,-1)
    #                         type_num[t]+=1
    #                         ditems=[]
    #                         for d in data.get("data",None):
    #                             if d.get(t,None):
    #                                 y=d[t].get("value",None)
    #                                 x=d.get("begin_time",None)
    #                                 times= "" if type_num[t]<=0 else "_"+str(type_num[t])
    #                                 c=server + times
    #                                 item={"x": x, "y": y, "c":c}
    #                                 ditems.append(item)
    #                                 # chart[client][t].append(item)
    #                                 # print(item)
    #                         # chart[client][t]=self.optimize(chart[client][t],precision=precision)
    #                         ditems = self.optimize(ditems, precision=precision)
    #                         chart[client][t].extend(ditems)
    #
    #             for index in chart[client].keys():
    #                 v=template_data
    #                 if v.get("data",None):
    #                     # print(chart[client][index])
    #                     chart[client][index].sort(key=lambda k: k['x'])
    #                     # print(chart[client][index])
    #                     v['data'][0]['values']=chart[client][index]
    #                     # print(chart[client][index])
    #                     # print(len(chart[client][index]))
    #                 chart[client][index]=v
    #     return chart

    def optimize(self,data,precision=1):
        x=None
        y=0
        c=None
        newdata=[]
        count=0
        for index,d in enumerate(data):
            if d['y']<0:
                if count:
                    newdata.append({"x": x, "y": round(y/count,3), "c": c})
                count=0
                newdata.append({"x": d['x'], "y": d['y'], "c": d['c']})
            else:
                if count<precision:
                    if count==0:
                        y = 0
                        y += d['y']
                        x = d['x']
                        c = d['c']
                    else:
                        y += d['y']
                    count+=1
                    if index==len(data)-1:
                        newdata.append({"x": x, "y": round(y / count, 3), "c": c})
                else:
                    newdata.append({"x": x, "y": round(y/count,3), "c":c})
                    y=0
                    y += d['y']
                    x  = d['x']
                    c = d['c']
                    count = 1
                    if index==len(data)-1:
                        newdata.append({"x": x, "y": round(y / count, 3), "c": c})
        print(data)
        print(newdata)
        print(len(data))
        print(len(newdata))
        return newdata

class Vega_Template_Parse(Template_Parse):

    type = "linechart"

    def __init__(self):
        super(Vega_Template_Parse, self).__init__(template='linechart4.json')

    def parse(self,filename,flag='QoS',precision=1,store=True):
        static_data = None
        template_data = self.template_data
        if filename:
            try:
                with open(filename, 'r') as f:
                    static_data = json.load(f).get(flag, None)
            except FileNotFoundError:
                print("the file " + filename + " does not exist.")

        chart = {}
        if template_data and static_data:
            for client, servers in static_data.items():
                chart[client] = {}
                for server, datas in servers.items():
                    type_num = {}
                    for data in datas:
                        for t in data.get("type", None):
                            chart[client].setdefault(t, {'data': {'table':{'values':[]}},
                                                         'signals': {'end': {'value':{}},'x_title':{'value':''},'y_title':{'value':''}}})
                            type_num.setdefault(t, -1)
                            type_num[t] += 1
                            ditems = []
                            x_title=None
                            y_title=None
                            for d in data.get("data", None):
                                if d.get(t, None):

                                    y = d[t].get("value", None)
                                    if not y_title:
                                        y_title=d[t].get("name", "")+'  (%s)'%(d[t].get("measure", ""))

                                    x = d.get("begin_time", None)
                                    if not x_title and x:
                                        x_title = x.get("name", "") + '  (%s)' % (x.get("measure", ""))
                                    if x:
                                        x=x.get("value", None)

                                    times = "" if type_num[t] <= 0 else "_" + str(type_num[t])
                                    c = server + times
                                    item = {"x": x, "y": y, "c": c}
                                    ditems.append(item)
                                    # chart[client][t].append(item)
                                    # print(item)
                            # chart[client][t]=self.optimize(chart[client][t],precision=precision)
                            ditems = self.optimize(ditems, precision=precision)
                            chart[client][t]['data']['table']['values'].extend(ditems)
                            chart[client][t]['data']['table']['values'].sort(key=lambda k: k['x'])
                            chart[client][t]['signals']['end']['value'].update({ditems[-1]['c']: ditems[-1]})
                            chart[client][t]['signals']['x_title']['value']= x_title if x_title else ""
                            chart[client][t]['signals']['y_title']['value']= y_title if y_title else ""

                # for index in chart[client].keys():
                #     v = template_data
                #     if v.get("data", None):
                #         # print(chart[client][index])
                #         chart[client][index].sort(key=lambda k: k['x'])
                #         # print(chart[client][index])
                #         v['data'][0]['values'] = chart[client][index]
                #         # print(chart[client][index])
                #         # print(len(chart[client][index]))
                #     chart[client][index] = v
        chart=self.statisticToVega(chart=chart)
        if store:
            self.store_chart(chart=chart,x_title='x_title',y_title='y_title')
        return chart

    def statisticToVega(self,chart):

        for client,data in chart.items():
            for index,qos in data.items():
                template_data = copy.deepcopy(self.template_data)
                for item,value in qos.items():
                    for k,v in value.items():
                        if template_data.get(item,None):
                            if isinstance(template_data[item],list):
                                find=False
                                for d in template_data[item]:
                                    if isinstance(d,dict) and d['name'] == k:
                                        d.update(v)
                                        find=True
                                if not find:
                                    newdata={'name':k}
                                    newdata.update(v)
                                    template_data[item].append(newdata)

                            elif isinstance(template_data[item],dict):
                                if template_data[item].get(k,None):
                                    if isinstance(template_data[item][k],dict):
                                        template_data[item][k].update(v)
                                    else:
                                        template_data[item].update({k: v})
                                else:
                                    template_data[item].update({k:v})
                        else:
                            template_data.update({item:value})

                chart[client][index]=template_data
        return chart

class QoS_Statistics_Generator(object):

    template_types={'linechart':Vega_Template_Parse()}

    def __init__(self,template_path=None):
        # if not path:
        #     self.path = os.path.split(os.path.realpath(__file__))[0]+'/'
        # else:
        #     self.path=path
        self.template_path=template_path
        if self.template_path:
            for k,v in QoS_Statistics_Generator.template_types.items():
                QoS_Statistics_Generator.template_types[k].configurate_sources(template_path=template_path)


    def configurate_template_types(self,type={}):
        if type:
            QoS_Statistics_Generator.template_types.update(type)

    @classmethod
    def generate(cls,filename,chart_type='linechart',precision=1):

        if isinstance(precision,str):
            precision=int(precision)

        chart_parser=QoS_Statistics_Generator.template_types.get(chart_type,None)

        chart=chart_parser.parse(filename,precision=precision)

        return chart

# qos=QoS_Statistics_Generator(template_path=r'QoS_Index_Templates/')
# qos.generate(filename=r'Network_Topology/Network_Topology_20230310204355324533.json')