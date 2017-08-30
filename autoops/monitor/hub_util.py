
#/usr/bin/python
# -*- coding: utf-8 -*-

from autoops.settings import oracle_conn
from autoops.oracle import OracleDb
def get_hub_ip_list(start,end,reg):
    db=OracleDb()
    sql_cmd="select distinct HOST from MONITOR.hubstat where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and RegName='%s'"%(start,end,reg)
    result=db.execute(sql_cmd)
    ip_list=[]
    for item in result:
        ip_list.append(item)    
    return ip_list



def get_hub_ajax_count(ip_list,start,end,reg):
    db=OracleDb()
    name=['name','data']
    dic={}
    highchart_ret=[]
    for ip in ip_list:
         sql_cmd="select CURRACTIVETHREADCOUNT from MONITOR.hubstat where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s' and RegName='%s'" %(start,end,ip,reg)
         ret=db.execute(sql_cmd)
         count=[]
         for item in ret:
            count.append(item)
         s=[ip,count]
         dic=dict(zip(name,s))
         highchart_ret.append(dic)
    return highchart_ret
