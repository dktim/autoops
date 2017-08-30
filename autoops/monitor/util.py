#coding:utf-8

from autoops.settings import oracle_conn
from __builtin__ import list
from autoops.oracle import OracleDb

def get_ip_list(reg,start_time,end_time):
    
    db=OracleDb()
    sql_cmd="select distinct HOST from monitor_jdbc where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and RegName='%s'" %(start_time,end_time,reg)
    result=db.execute(sql_cmd)
    ip_list=[]
    for i in result:
        ip_list.append(i)
    return ip_list

def get_count_with_ip(ip_list,start_time,end_time,reg):
     db=OracleDb()
     name=['name','data']
     dic={}
     ret=[]
     for ip in ip_list:
        sql_cmd="""
select c.activecurrent
  from appregioninfo a,machineinfo b, monitor_jdbc c
 where c.regname = '{0}'
   and c.host='{1}'
   and c.host=b.ipaddress
   and c.regname=b.regname
   and c.regname=a.regname
   and c.jdbcpoolname = a.defaultjdbcpool   
   and c.tm_smp > to_date('{2}', 'yyyy-mm-dd hh24:mi:ss')
   and c.tm_smp < to_date('{3}', 'yyyy-mm-dd hh24:mi:ss')
   order by c.seqnum asc
"""
	sql_cmd=sql_cmd.format(reg,ip,start_time,end_time)
	result=db.execute(sql_cmd)
        count=[]
        for item in result:
            count.append(item)
        s=[ip,count]
        dic=dict(zip(name,s))
        ret.append(dic)
     return ret
 
def parse_ip_count(dic):
    count_list=[]
    desc_list=[]
    ip_list=[]
    time_list=[]
    for key,value in dic.items():
        for item in value:
            count_list.append(int(item['ActiveCurrent']))
    return count_list
               
def get_time_with_ajax(ip_list,start_time,end_time,type,reg):
    oracle_db=OracleDb()
    list=[]    
    if type=='jms':      
        for ip in ip_list:
            sql_cmd="""
 select c.time
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
            sql_cmd=sql_cmd.format(reg,ip,start_time,end_time)
            result=oracle_db.execute(sql_cmd)
            for item in result:
                list.append(item)
        return list
    
    elif type=='jdbc':
        for ip in ip_list:
            sql_cmd="""
      
  select c.time
  from appregioninfo a,machineinfo b, monitor_jdbc c
 where c.regname ='{0}'
   and c.host='{1}'
   and c.host=b.ipaddress
   and c.regname=b.regname
   and c.regname=a.regname
   and c.jdbcpoolname = a.defaultjdbcpool   
   and c.tm_smp > to_date('{2}', 'yyyy-mm-dd hh24:mi:ss')
   and c.tm_smp < to_date('{3}', 'yyyy-mm-dd hh24:mi:ss')
   order by c.seqnum asc
   """
            sql_cmd=sql_cmd.format(reg,ip,start_time,end_time)
            result=oracle_db.execute(sql_cmd)
            
            for item in result:
                list.append(item)
        return list
    elif type=='lsn':
        for ip in ip_list:
            sql_cmd="select TM_SMP from monitor.lsnstat where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s' and RegName='%s'" %(start_time,end_time,ip,reg)
            result=oracle_db.execute(sql_cmd)
            for item in result:
                list.append(item.strftime('%Y-%m-%d:%H:%M:%S'))
        return list
    elif type=='hub':
        for ip in ip_list:
            sql_cmd="select TM_SMP from monitor.hubstat where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s'" %(start_time,end_time,ip)
            result=oracle_db.execute(sql_cmd)
            for item in result:
                list.append(item.strftime('%Y-%m-%d:%H:%M:%S'))
        return list
               
               

               
               
         

               

if __name__ == '__main__':
   
    pass