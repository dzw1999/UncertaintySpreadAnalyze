import pprint
from data import Nl
Nl=[
    '项目打开时间功能能够支持打开模型数小于150个的项目的时间小于3秒。',
    '5.5.4	单视图结构下模型数量要求\n单个视图结构下可支持管理的模型数不少于40个。',
    '通用性能指标如表22所示。\n5.5.1	响应时间指标功能\n响应时间指标功能，用户页面响应时间一般不超过3秒。\n5.5.2	项目打开时间功能\n项目打开时间功能能够支持打开模型数小于150个的项目的时间小于3秒。',    
]

result=[]

for i in range(0,len(Nl)):
    temList = {'id': None, 'description': None}
    temList['id']=str(i)
    temList['description']=Nl[i]
    result.append(temList)
pprint.pprint(result)
