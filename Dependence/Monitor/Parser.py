import re
from enum import Enum
from mininet.log import info, error, debug, output, warn

class MonitorType(Enum):
    Delay = 'delay'
    Packet_Loss ='packet_loss'
    Band_Width = 'band_width'


class NetworkMonitorParser:

    @staticmethod
    def parse(result):
        pass

class PingParser(NetworkMonitorParser):
    @staticmethod
    def Parse(result,*args,**kwargs):
        "Parse ping output and return packets sent, received."
        # Check for downed link
        # if 'connect: Network is unreachable' in result:
        #     return 1, 0
        if not result:
            return {MonitorType.Packet_Loss.value:{'measure':'%','name':MonitorType.Packet_Loss.value},MonitorType.Delay.value:{'measure':'ms','name':MonitorType.Delay.value}}
        r = r'(\d+) packets transmitted, (\d+)( packets)? received'
        packet= re.search( r, result )
        r = r'rtt min/avg/max/mdev = (\d+\.?\d+)\/(\d+\.?\d+)\/(\d+\.?\d+)\/(\d+\.?\d+)'
        rtt = re.search(r, result)
        if packet is None:
            error( '*** Error: could not parse ping output: %s\n' %
                   result )
            return {MonitorType.Packet_Loss.value:{'measure':'%','name':MonitorType.Packet_Loss.value},MonitorType.Delay.value:{'measure':'ms','name':MonitorType.Delay.value}}
        sent, received = int( packet.group( 1 ) ), int( packet.group( 2 ) )
        loss=100-100.0*received/sent
        packet_loss={'sent':sent,'received':received,'loss':loss,'value':loss,'measure':'%','name':MonitorType.Packet_Loss.value}
        if rtt is None:
            return {MonitorType.Packet_Loss.value:packet_loss,MonitorType.Delay.value:{'measure':'ms','name':MonitorType.Delay.value}}
        min,avg,max,mdev =float(rtt.group(1))/2,float(rtt.group(2))/2,float(rtt.group(3))/2,float(rtt.group(4))/2
        delay={'min':min,'avg':avg,'max':max,'mdev':mdev,'value':avg,'measure':'ms','name':MonitorType.Delay.value}
        return {MonitorType.Packet_Loss.value:packet_loss,MonitorType.Delay.value:delay}


# var = "This is a string"
# varName = 'var'
# locals()['xyz']=20
# print(xyz)

class IperfParser(NetworkMonitorParser):
    @staticmethod
    def Parse(client_result,server_result,*args,**kwargs):

        result = {MonitorType.Band_Width.value: {'measure': 'Mbps','name':MonitorType.Band_Width.value},
                  'transfer': {'measure': 'MBytes','name':'transfer'}}

        if not client_result and not server_result:
            return result
        cr=None
        if client_result:
            cr=re.findall(r'(\d+\.?\d+) MBytes  (\d+\.?\d+) \w+/sec',client_result)
        sr=None
        if server_result:
            sr = re.findall(r'(\d+\.?\d+) MBytes  (\d+\.?\d+) \w+/sec', server_result)

        # result= {MonitorType.Band_Width.value: {'measure': 'Mbps'}, 'transfer': {'measure': 'MBytes'}}
        if cr:
            result.update({'client_'+MonitorType.Band_Width.value: {'value':float(cr[-1][1]),'measure': 'Mbps','name':'client_'+MonitorType.Band_Width.value}, 'client_transfer': {'value':float(cr[-1][0]),'measure': 'MBytes','name':'client_transfer'}})
            result.update({MonitorType.Band_Width.value: {'value':float(cr[-1][1]),'measure': 'Mbps','name':MonitorType.Band_Width.value},'transfer': {'value':float(cr[-1][0]),'measure': 'MBytes','name':'transfer'}})
        if sr:
            result.update({'server_' + MonitorType.Band_Width.value: {'value': float(sr[-1][1]), 'measure': 'Mbps','name':'server_' + MonitorType.Band_Width.value},'server_transfer': {'value': float(sr[-1][0]), 'measure': 'MBytes','name':'server_transfer'}})

        return result

# r1='''
# Client connecting to 10.0.0.5, TCP port 5001
# TCP window size: 85.3 KByte (default)
# ------------------------------------------------------------
# [  1] local 10.0.0.1 port 34448 connected with 10.0.0.5 port 5001
# [ ID] Interval       Transfer     Bandwidth
# [  1] 0.0000-4.3901 sec  5.00 MBytes  9.55 Mbits/sec
# [  1] 0.0000-4.3901 sec  5.00 MBytes  9.55 Mbits/sec
# '''
# r2='''------------------------------------------------------------
# Server listening on TCP port 5001
# TCP window size: 85.3 KByte (default)
# ------------------------------------------------------------
# [  1] local 10.0.0.5 port 5001 connected with 10.0.0.1 port 34448
# [ ID] Interval       Transfer     Bandwidth
# [  1] 0.0000-4.3772 sec  5.00 MBytes  9.58 Mbits/sec
# '''
# IperfParser.Parse(r1,r2)