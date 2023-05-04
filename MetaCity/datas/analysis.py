import json
import numpy as np
def get_datas(filename): #从json文件中提取出数据，然后将此数据分为原始数据、正常数据，非正常数据(存在小于0的值)进行返回
    data=[]
    data_abnormal=[]
    data_normal=[]
    with open(filename,'r') as f:
        data=json.load(f)
    if data:
        data=data.get('data',[])
        for d in data:
            if d['x']<0 or d['y']<0:
                data_abnormal.append(d)
            else:
                data_normal.append(d)
    print(data)
    print(data_normal)
    print(data_abnormal)
    return data,data_normal,data_abnormal

def analysis(data): #分析数据，求平均数，中位数
    if not data:
        return {}

    c={}
    for d in data:
        if d['c'] in c:
            c[d['c']].append(d)
        else:
            c.update({d['c']:[]})
            c[d['c']].append(d)
    result={}
    for k ,v in c.items():
        x=[]
        y=[]
        for v1 in v:
            x.append(v1['x'])
            y.append(v1['y'])
        mean=np.mean(y)
        median=np.median(y)
        result.update({k:{'mean':mean,'median':median,'count':len(v)}})
    return result

def segment_data(data,index=[0]): #将数据根据时间分成路由切换前，切换中，切换后三部分
    index.sort()
    segment=data
    result=[]
    for i in index:
        seg1=[]
        seg2=[]
        for d in segment:
            if d['x'] <= i:
                seg1.append(d)
            else:
                seg2.append(d)
        segment=seg2
        result.append(seg1)
    result.append(segment)
    return result


def analysis_delay(filename,handover=[0]): #分析延迟相关信息

    data, data_normal, data_abnormal = get_datas(filename)

    result_normal = segment_data(data_normal, handover)
    print('original delay data:'+str(result_normal))
    result_abnormal = segment_data(data_abnormal, handover)
    print('original packet_loss data:' + str(result_abnormal))

    delay=[]
    for i in range(len(handover)+1):
        if i%2==0:
            delay_result=analysis(result_normal[i])
            packet_loss_result = analysis(result_abnormal[i])
            for k ,v in delay_result.items():
                packet_loss=packet_loss_result.get(k,None)
                if packet_loss:
                    loss = packet_loss.get('count',0)/(v.get('count',0)+packet_loss.get('count',0))
                    v.update(packet_loss=loss)
                else:
                    v.update(packet_loss=None)

                v.update(num=int(i/2))
            delay.append(delay_result)
            print("delay statistics:"+str(delay_result))

#analysis_delay(filename=r'moving point-to-cloud data/1/json data/mp0_delay_20230310204622326524.json',handover=[-1,4.1,75.83,80.21]) #handover 发生路由切换的时间段,即根据时间点对数据进行分段处理。
#handover=[75.83,80.21]
#handover=[75.15,79.54]

analysis_delay(filename=r'SDN controller/1/json data/mp0_delay_20230312143947444527.json',handover=[-1,2.14,37.97,42.38]) #handover 发生路由切换的时间段,即根据时间点对数据进行分段处理。

analysis_delay(filename=r'SDN controller/ryu/json data/mp0_delay_20230312152806777630.json',handover=[-1,4.22,37.96,42.44]) #handover 发生路由切换的时间段,即根据时间点对数据进行分段处理。
