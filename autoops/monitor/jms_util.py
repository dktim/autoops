#/usr/bin/python
# -*- coding: utf-8 -*-

from autoops.settings import oracle_conn
from autoops.oracle import OracleDb

def get_jms_ip_list(start,end,reg):
    db=OracleDb()
    sql_cmd="select distinct HOST from monitor_jms where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and RegName='%s'" %(start,end,reg)
    result=db.execute(sql_cmd)
    ip_list=[]
    for item in result:
        ip_list.append(item)
    return ip_list



def get_jms_ajax_count(ip_list,start,end,reg):
    db=OracleDb()
    name=['name','data']
    dic={}
    highchart_ret=[]
    for ip in ip_list:
         sql_cmd="select MessagesCurrentCount from monitor.monitor_jms where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s' and NAME in(select DEFAULTJMSQUEUE from appregioninfo where regname='%s')order by TM_SMP" %(start,end,ip,reg)
         sql_cmd="""
 select c.MESSAGESCURRENTCOUNT
  from appregioninfo a,machineinfo b, monitor_jms c
 where c.regname ='{0}'
   and c.host='{1}'
   and c.host=b.ipaddress
   and c.regname=b.regname
   and c.regname=a.regname
   and c.name = a.DEFAULTJMSQUEUE
   and c.tm_smp > to_date('{2}', 'yyyy-mm-dd hh24:mi:ss')
   and c.tm_smp < to_date('{3}', 'yyyy-mm-dd hh24:mi:ss')
   order by c.seqnum asc
"""
	 sql_cmd=sql_cmd.format(reg,ip,start,end)
         ret=db.execute(sql_cmd)
         count=[]
         
         for item in ret:
            count.append(item)
         s=[ip,count]
         dic=dict(zip(name,s))
         highchart_ret.append(dic)
    
    return highchart_ret
