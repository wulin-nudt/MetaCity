import datetime
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import threading
from mininet.log import info, setLogLevel,error
from threading import Thread as thread
from time import sleep, time
import re
from Monitor.Parser import PingParser,MonitorType,IperfParser
from mininet.log import info, error, debug, output, warn
from mininet.util import BaseString
from six import string_types
from pathlib import Path
import json



class NetworkMonitor(object):
    aps = []
    stations = []
    thread_ = ''
    Network_QoS_Statistic={}
    filelock = threading.Lock()
    def __init__(self,client,server,monitor_tool,client_monitor_args,server_monitor_args,parser,monitor_type,*args,**kwargs):
        self.client=client
        self.server=server
        self.monitor_tool = monitor_tool
        self.client_monitor_args=client_monitor_args
        self.server_monitor_args=server_monitor_args
        self.MonitorType = []
        self.StrToMonitorType=dict([(m.value,m) for m in MonitorType])
        self.Parser=parser
        self.draw = False
        for i in monitor_type:
            if isinstance(i,str):
                if self.StrToMonitorType.get(i,None):
                    self.MonitorType.append(self.StrToMonitorType.get(i,None))
            elif isinstance(i,MonitorType):
                self.MonitorType.append(i)
        # self.statistic=[]
    #monitoring_nodes_pair=[]

    def plotGraph(self,min_x=0, min_y=0,max_x=0, max_y=0):
        self.draw = True
        if min_x or max_x:
            self.xlim=(min_x,max_x)
        if min_y or max_y:
            self.ylim=(min_y, max_y)

    def Network_QoS(self, type=[], client_result=None,server_result=None):
        if not type:
            return None
        outcome = self.Parser.Parse(client_result,server_result)
        QoS={}
        for ty in type:
            if ty.value not in outcome:
                QoS.update({ty.value:None})
            else:
                QoS_index = outcome.get(ty.value, None)
                value=QoS_index.get('value',-1)
                measure=QoS_index.get('measure','')
                name=QoS_index.get('name','')
                QoS.update({ty.value:{'value':value,'measure':measure,'name':name}})
        QoS.update({'outcome':outcome})
        return QoS

    def extend_monitor_type(self,type=None):
        types=[]
        types.append(type)
        for t in types:
            if t not in self.MonitorType:
                self.MonitorType.append(t)

    #plot画图
    @staticmethod
    def draw_statistic(x,y,title,x_label,y_label,linetype='b-',*args,**kwargs):
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if kwargs.get('xlim'):
            plt.xlim(kwargs.get('xlim'))
        if kwargs.get('ylim'):
            plt.ylim(kwargs.get('ylim'))
        plt.plot(x, y, linetype)
        plt.pause(0.01)

    #判断某个网络监控器工具是否可用
    @classmethod
    def isAvailable(cls,node,monitor_tool):
        "Is NetworkMonitor available?"
        if node.cmd("which",monitor_tool):
            return True
        else:
            return False
    @staticmethod
    def isDirectoryExist(node,directory):
        if 'No such file or directory' in node.cmd('find '+directory):
            return False
        else:
            return True

    @staticmethod
    def CreateDirectory(node,directory):
        if not NetworkMonitor.isDirectoryExist(node,directory):
            node.cmd('mkdir -p '+directory)

    @classmethod
    def update_QoS_Statistic(cls,node,type,Directory):
        QoS=cls.Network_QoS_Statistic.get(node,None)
        if QoS:
            for ty in type:
                if QoS.get(ty.value,None):
                    cls.Network_QoS_Statistic[node][ty.value].append(Directory)
                else:
                    cls.Network_QoS_Statistic[node][ty.value]=[Directory]
        else:
            cls.Network_QoS_Statistic[node]={}
            for ty in type:
                cls.Network_QoS_Statistic[node].update({ty.value:[Directory]})

    def client_run(self,start_time,client_statistic_Directory,extra_args=''):
        result = None
        begin_time = round(time() - start_time, 2)
        if self.client_monitor_args:
            self.client.cmd("echo begin time: " + str(begin_time) + ">>" + client_statistic_Directory+ '.out' + ' &')
            result = self.client.cmd(self.monitor_tool + ' ' + self.client_monitor_args + ' ' + self.server.IP() +' '+extra_args +' '+ " | tee -a " + client_statistic_Directory+ '.out')
        # self.client.cmd('wait %' + self.monitor_tool)
        end_time = round(time() - start_time, 2)
        if self.client_monitor_args:
            self.client.cmd("echo end time: " + str(end_time) + ">>" + client_statistic_Directory + '.out' + ' &')

        output(result+' '+str(threading.current_thread())+' '+self.server.name+'\n')
        output(str(self.server.getxyz()) + '\n')
        output(str(self.client.getxyz()) + '\n')
        output(str(self.client.wintfs[0].associatedTo)+'\n')
        if self.client.wintfs[0].associatedTo:
            output(self.client.wintfs[0].node.get_distance_to(self.client.wintfs[0].associatedTo.node))
            output('\n')

        begin_time={'name':'time','value':begin_time,'measure':'s'}
        end_time= {'name': 'time', 'value': end_time, 'measure': 's'}

        return (begin_time,end_time,result)

    def server_run(self, start_time, server_statistic_Directory,extra_args=''):
        result=None
        begin_time = round(time() - start_time, 2)
        if self.server_monitor_args:
            self.server.cmd('killall -9 '+self.monitor_tool)
            result=self.server.cmd(self.monitor_tool + ' ' + self.server_monitor_args +' '+extra_args +' '+ " > " + server_statistic_Directory + self.monitor_tool + '.out'+" &")
        end_time = round(time() - start_time, 2)

        begin_time={'name':'time','value':begin_time,'measure':'s'}
        end_time= {'name': 'time', 'value': end_time, 'measure': 's'}

        return (begin_time,end_time,result)

    def monitoring(self,start_time,client_statistic_Directory,server_statistic_Directory,index=0):
        threadingname=threading.current_thread().getName()
        server_result = self.server_run(start_time, server_statistic_Directory)
        client_result = self.client_run(start_time, client_statistic_Directory + str(index)+'_'+threadingname)
        return client_result,server_result

    @staticmethod
    def statistic_collection(QoS,begin_time,end_time,client_pos,server_pos,counts,*args,**kwargs):
        statistic={}
        for k,v in QoS.items():
            statistic.update({k:v})
        statistic.update(begin_time=begin_time)
        statistic.update(end_time=end_time)
        statistic.update(client_pos=client_pos)
        statistic.update(server_pos=server_pos)
        statistic.update(counts=counts)
        return statistic

    @staticmethod
    def extract_data(data,type,x,y,z=None,**kwargs):
        x_lable=[]
        y_lable=[]
        z_lable=[]

        if not isinstance(x,BaseString):
            x=x.value
        if not isinstance(y, BaseString):
            y = y.value
        if not isinstance(x, BaseString):
            z = z.value

        type=[t.value for t in type]

        for v in data:
            x1=v.get(x,None)
            y1=v.get(y,None)
            if x in type and x1 is not None:
                x1=x1.get('value',-1)
            if y in type and y1 is not None:
                y1=y1.get('value',-1)
            # x1 = x1 if x1 is not None else -1
            # y1 = y1 if y1 is not None else -1
            x_lable.append(x1)
            y_lable.append(y1)
            if z:
                z1 = v.get(z, None)
                if z in type and z1 is not None:
                    z1 = z1.get('value', -1)
                # z1 = z1 if z1 is not None else -1
                z_lable.append(z1)
        return x_lable,y_lable,z_lable

    @staticmethod
    def statistic_Directory_init(client,server,client_Directory,server_Directory,type):
        date = datetime.datetime.now().strftime("/%Y_%m_%d/%H_%M_%S/")
        client_Directory=client_Directory+date
        server_Directory=server_Directory+date
        NetworkMonitor.CreateDirectory(client,client_Directory)
        NetworkMonitor.CreateDirectory(server,server_Directory)
        client_statistic_Directory = client_Directory
        server_statistic_Directory = server_Directory
        NetworkMonitor.update_QoS_Statistic(client,type,client_statistic_Directory)
        NetworkMonitor.update_QoS_Statistic(server,type,server_statistic_Directory)
        return client_statistic_Directory,server_statistic_Directory

    def monitoring_for_period(self,period,client_Directory,server_Directory,type):
        client_statistic_Directory,server_statistic_Directory=NetworkMonitor.statistic_Directory_init(self.client,self.server,client_Directory,server_Directory,type)
        start_time=time()
        # server_result=self.server_run(start_time,server_statistic_Directory)

        i = 0
        statistic=[]
        start_time = time()
        while time()-start_time<=period:
            client_pos={'name':'client Position','value':self.client.getxyz(),'measure':''}
            server_pos={'name':'server Position','value':self.server.getxyz(),'measure':''}
            # server_result = self.server_run(start_time, server_statistic_Directory)
            # client_result=self.client_run(start_time,client_statistic_Directory + str(i))
            # output('1' + str(threading.current_thread()) + '\n')
            client_result, server_result = self.monitoring(start_time, client_statistic_Directory,server_statistic_Directory, index=i)
            # output('2' + str(threading.current_thread()) + '\n')
            # print(client_result)
            QoS = self.Network_QoS(type=type, client_result=client_result[2],server_result=server_result[2])
            tb=client_result[0]
            te=client_result[1]
            data=NetworkMonitor.statistic_collection(QoS,tb,te,client_pos,server_pos,counts=i)
            statistic.append(data)
            # print(data)
            if self.draw:
                xlim= self.xlim if hasattr(self,'xlim') else None
                ylim = self.ylim if hasattr(self, 'ylim') else None
                x, y, z = NetworkMonitor.extract_data(statistic, type, 'begin_time', MonitorType.Delay)
                self.draw_statistic(x, y, title='Network QoS for  ' + MonitorType.Delay.value, x_label='time s',y_label=MonitorType.Delay.value,xlim=xlim,ylim=ylim)
            i+=1
            sleep(0.0001)
        statistic.append({'start_time':start_time,'stop_time':time(),'real_period':time()-start_time})
        return statistic

    def monitoring_for_times(self,times,client_Directory,server_Directory,type):
        client_statistic_Directory,server_statistic_Directory=NetworkMonitor.statistic_Directory_init(self.client,self.server,client_Directory,server_Directory,type)
        start_time=time()
        # server_result=self.server_run(start_time,server_statistic_Directory)

        statistic=[]
        start_time = time()

        for i in range(times):
            client_pos={'name':'client Position','value':self.client.getxyz(),'measure':''}
            server_pos={'name':'server Position','value':self.server.getxyz(),'measure':''}
            # server_result = self.server_run(start_time, server_statistic_Directory)
            # client_result = self.client_run(start_time, client_statistic_Directory + str(i))
            client_result,server_result=self.monitoring(start_time,client_statistic_Directory,server_statistic_Directory,index=i)
            QoS = self.Network_QoS(type=type, client_result=client_result[2],server_result=server_result[2])
            tb = client_result[0]
            te = client_result[1]
            data = NetworkMonitor.statistic_collection(QoS, tb, te, client_pos, server_pos,counts=i)
            statistic.append(data)
            x, y, z = NetworkMonitor.extract_data(statistic, type, 'begin_time', MonitorType.Packet_Loss)
            if self.draw:
                xlim= self.xlim if hasattr(self,'xlim') else None
                ylim = self.ylim if hasattr(self, 'ylim') else None
                self.draw_statistic(x, y, title='Network QoS for  ' + MonitorType.Packet_Loss.value, x_label='time s', y_label=MonitorType.Packet_Loss.value,xlim=xlim,ylim=ylim)

            sleep(0.0001)
        statistic.append({'start_time': start_time, 'stop_time': time(), 'real_period': time() - start_time})

        return statistic

    def clean(self,*args,**kwargs):
        data_storage_Directory=kwargs.get("data_storage_Directory",None)
        if data_storage_Directory:
            file=Path(data_storage_Directory)
            if file.exists():
                file.unlink()

    def store_data(self,data=None,data_storage_Directory=None):

        datas = {'QoS':{self.client.name: {self.server.name: [{'type': [t.value for t in self.MonitorType],'data':data}]}}}
        if data_storage_Directory and data:
            with self.filelock:
                with open(data_storage_Directory,'a+') as f:
                    f.seek(0)
                    exist_data=f.read()
                    if len(exist_data)>0:
                        exist_data=json.loads(exist_data)
                    else:
                        exist_data={}
                    if exist_data.get('QoS',None) and exist_data['QoS'].get(self.client.name,None):
                        if exist_data['QoS'][self.client.name].get(self.server.name,None):
                            exist_data['QoS'][self.client.name][self.server.name].append(datas['QoS'][self.client.name][self.server.name][0])
                        else:
                            exist_data['QoS'][self.client.name].update(datas['QoS'][self.client.name])
                    else:
                        if exist_data.get('QoS',None):
                            exist_data['QoS'].update(datas['QoS'])
                        else:
                            exist_data.update(datas)
                    f.seek(0)
                    f.truncate()
                    d=json.dumps(exist_data,indent=2)
                    f.write(d)
                    # json.dump(exist_data,f)

class NetworkDelayMonitor(NetworkMonitor):

    def __init__(self,client,server,net,monitor_tool='ping',client_monitor_args='-c 1 -w 1',server_monitor_args=None,parser=PingParser(),monitor_type=[MonitorType.Delay],*args,**kwargs):
        client = client if not isinstance(client, string_types) else net[client]
        server = server if not isinstance(server, string_types) else net[server]
        NetworkMonitor.__init__(self,client,server,monitor_tool,client_monitor_args,server_monitor_args,parser,monitor_type,*args,**kwargs)

        # print(self.MonitorType)
        # print(self.StrToMonitorType)


        # sleep(5)


    def start(self,cleanMode=True,*args,**kwargs):
        if cleanMode:
            self.clean(*args,**kwargs)

        if self.isAvailable(self.client,self.monitor_tool) and self.isAvailable(self.server,self.monitor_tool):
            self.start_thread(*args,**kwargs)
        else:
            error('monitor_tool {}  not available'.format(self.monitor_tool))

        return self

    def start_thread(self, *args,**kwargs):
        NetworkMonitor.thread_ = thread(target=self.configure,args=args,kwargs=kwargs)
        NetworkMonitor.thread_.daemon = True
        NetworkMonitor.thread_._keep_alive = True
        NetworkMonitor.thread_.start()

    def configure(self,client_Directory=None,server_Directory=None,*args,**kwargs):
        Directory=[t.value for t in self.MonitorType]
        if not client_Directory:
            client_Directory='/home/'+'_AND_'.join(Directory)+'/'
        if not server_Directory:
            server_Directory='/home/'+'_AND_'.join(Directory)+'/'
        self.run(client_Directory=client_Directory,server_Directory=server_Directory,*args,**kwargs)

    def run(self,client_Directory,server_Directory,period=None,times=1,data_storage_Directory=None,*args,**kwargs):

        data=None

        if period:
            data=self.monitoring_for_period(period,client_Directory,server_Directory,self.MonitorType)
        else:
            data=self.monitoring_for_times(times,client_Directory,server_Directory,self.MonitorType)

        self.store_data(data=data,data_storage_Directory=data_storage_Directory)

        # datas = {'QoS':{self.client.name: {self.server.name: [{'type': [t.value for t in self.MonitorType],'data':data}]}}}
        # if data_storage_Directory and data:
        #     with self.filelock:
        #         with open(data_storage_Directory,'a+') as f:
        #             f.seek(0)
        #             exist_data=f.read()
        #             if len(exist_data)>0:
        #                 exist_data=json.loads(exist_data)
        #             else:
        #                 exist_data={}
        #             if exist_data.get('QoS',None) and exist_data['QoS'].get(self.client.name,None):
        #                 if exist_data['QoS'][self.client.name].get(self.server.name,None):
        #                     exist_data['QoS'][self.client.name][self.server.name].append(datas['QoS'][self.client.name][self.server.name][0])
        #                 else:
        #                     exist_data['QoS'][self.client.name].update(datas['QoS'][self.client.name])
        #             else:
        #                 exist_data.update(datas)
        #             f.seek(0)
        #             f.truncate()
        #             json.dump(exist_data,f)
                    # f.write("%s"%(json.dumps(exist_data)))





#test
# ne=NetworkDelayMonitor()
# print(ne.isAvailable('ping'))
# print(datetime.datetime.now().strftime("%Y_%m_%d/%H_%M_%S"))
# nn=NetworkMonitor(1,1,'ping','1')
# result="""PING www.a.shifen.com (14.215.177.38) 56(84) bytes of data.
# 64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=1 ttl=128 time=19.8 ms /
# 64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=2 ttl=128 time=42.3 ms
# 64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=3 ttl=128 time=24.8 ms
# 64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=4 ttl=128 time=26.1 ms
# 64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=5 ttl=128 time=45.3 ms
#
# --- www.a.shifen.com ping statistics ---
# 5 packets transmitted, 5 received, 0% packet loss, time 4006ms
# rtt min/avg/max/mdev = 19.846/31.676/45.295/10.165 ms"""
# print(nn.prase(result))

class NetworkBandWidthMonitor(NetworkMonitor):

    def __init__(self,client,server,net,monitor_tool='iperf',client_monitor_args='-t 2 -i 1 -f m -c',server_monitor_args='-s -f m',parser=IperfParser(),monitor_type=[MonitorType.Band_Width],
                 port_args='-p {}',default_port=5001,running_flags={'server':{'sucess':['Server listening'],'fail':['Address already in use']},'client':{'sucess':['Client connecting'],'fail':['connect failed']}},*args,**kwargs):
        client = client if not isinstance(client, string_types) else net[client]
        server = server if not isinstance(server, string_types) else net[server]
        NetworkMonitor.__init__(self,client,server,monitor_tool,client_monitor_args,server_monitor_args,parser,monitor_type,*args,**kwargs)
        self.default_port=default_port
        self.port_args = port_args
        self.running_flags=running_flags

    def start(self,cleanMode=True,*args,**kwargs):
        if cleanMode:
            self.clean(*args,**kwargs)

        if self.isAvailable(self.client,self.monitor_tool) and self.isAvailable(self.server,self.monitor_tool):
            self.start_thread(*args,**kwargs)
        else:
            error('monitor_tool {}  not available'.format(self.monitor_tool))

        return self

    def start_thread(self, *args,**kwargs):
        NetworkMonitor.thread_ = thread(target=self.configure,args=args,kwargs=kwargs)
        NetworkMonitor.thread_.daemon = True
        NetworkMonitor.thread_._keep_alive = True
        NetworkMonitor.thread_.start()

    def configure(self,client_Directory=None,server_Directory=None,*args,**kwargs):

        Directory=[t.value for t in self.MonitorType]
        if not client_Directory:
            client_Directory='/home/'+'_AND_'.join(Directory)+'/'
        if not server_Directory:
            server_Directory='/home/'+'_AND_'.join(Directory)+'/'
        self.run(client_Directory=client_Directory,server_Directory=server_Directory,*args,**kwargs)

    def run(self,client_Directory,server_Directory,period=None,times=1,data_storage_Directory=None,*args,**kwargs):

        data=None

        if period:
            data=self.monitoring_for_period(period,client_Directory,server_Directory,self.MonitorType)
        else:
            data=self.monitoring_for_times(times,client_Directory,server_Directory,self.MonitorType)

        self.store_data(data=data,data_storage_Directory=data_storage_Directory)

    def monitoring(self, start_time, client_statistic_Directory, server_statistic_Directory, index=0):

        # port=5001
        # port_args='-p '+str(port)
        threadingname=threading.current_thread().getName()
        # output(threading.current_thread().getName())
        extra_args=self.port_args.format(self.default_port)

        output('BandWidth Testing Begain\n')

        # self.server.cmd('killall -9 '+self.monitor_tool)
        server_result = ''
        # i=0
        while True:

            # i=i+1
            # output(threading.current_thread())
            # output(str(i)+'\n')
            # output(server_result  + '\n')

            self.server.sendCmd(self.monitor_tool + ' ' + self.server_monitor_args+' '+extra_args)
            sucess= False
            fail = False
            while not (sucess ^ fail):
                server_result += self.server.monitor(timeoutms=5000)
                sucess = any(s in server_result for s in self.running_flags['server']['sucess'])
                fail = any(s in server_result for s in self.running_flags['server']['fail'])
                # output(server_result  + '\n')

            if fail:
                self.default_port = self.default_port+1
                extra_args = self.port_args.format(self.default_port)
                # port_args = '-p ' + str(port)
                # self.server_monitor_args=self.server_monitor_args+' '+ port_args
                # self.client_monitor_args=port_args+' '+self.client_monitor_args
                self.server.sendInt()
                self.server.waitOutput()
                server_result = ''
            elif sucess:
                break

        # self.server.sendCmd(self.monitor_tool + ' ' + self.server_monitor_args)

        client_result = self.client_run(start_time, client_statistic_Directory + str(index)+'_'+threadingname,extra_args)

        # if 'connect failed' in client_result[2]:
        if any(c in client_result[2] for c in self.running_flags['client']['fail']):
            client_result=(client_result[0],client_result[1],None)

        # server_result=''
        while len(re.findall('/sec', server_result)) < 1 and client_result[2]:
            # output('3.5' + str(threading.current_thread()) + '\n')
            # output(server_result)
            # output(client_result[2])
            server_result += self.server.monitor(timeoutms=5000)

        self.server.sendInt()
        server_result += self.server.waitOutput()
        server_result=(client_result[0],client_result[1],server_result)

        # output(str(threading.current_thread()) + '\n')
        output('BandWidth Testing End\n')

        return client_result,server_result