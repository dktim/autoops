
from autoops.oracle import OracleDb
from autoops.settings import oracle_conn
def get_lsn_ip_list(start,end,reg):
    db=OracleDb()
    sql_cmd="select distinct host from monitor.lsnstat where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and regname='%s'"%(start,end,reg)
    result=db.execute(sql_cmd)
    ip_list=[]
    for item in result:
        ip_list.append(item.strip())
    return ip_list

def get_lsn_ajax_count(ip_list,start,end,reg):
    db=OracleDb()
    dic={}
    name=['name','data']
    highchart_ret=[]
    for ip in ip_list:
         sql_cmd="select CURRACTIVETHREADCOUNT from monitor.lsnstat where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s' and regname='%s'" %(start,end,ip,reg)
         ret=db.execute(sql_cmd)
         count=[]
         for item in ret:
            count.append(item)
         s=[ip,count]
         dic=dict(zip(name,s))
         highchart_ret.append(dic)
    return highchart_ret
