from autoops.oracle import OracleDb
from autoops.settings import oracle_conn
from salt.client import LocalClient
import datetime
import time
def reg_host_user(conn,sql):
    db=OracleDb()
    ret=db.executemany(sql)
    list=[]
    for item in ret:
        dic={}
        dic['regname']=item[0]
        dic['ipaddress']=item[1]
        dic['username']=item[2]
        list.append(dic)
    return list
        
        
        
def exe_salt_command(target,cmd_type,cmd):
    salt_client=LocalClient()
    start_time=get_current_time()
    jid=salt_client.cmd_async(target, cmd_type, [cmd])
    time.sleep(10)
    ret=salt_client.get_cache_returns(jid)
    if ret:
        result=ret[target]['ret']
    else:
        result='error'
    return result,jid
        
        

def get_current_time():
    cur_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return cur_time
