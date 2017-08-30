#coding:utf-8
from autoops.settings import oracle_conn
from autoops.oracle import OracleDb
from salt.client import LocalClient
import time
"""
输入ip，返回saltstack的客户端名称；
"""
def parse_saltstack_name(ip):
    db=OracleDb()
    sql="select salt_name from salt_ip where ip='%s'"%(ip)
    try:
        ret=db.execute(sql)[0]
	return ret 
    except:
        return None
    


class salttask(object):
    def __init__(self,task_name,ip,cmd):
        self.task_name=task_name
        self.tgt=parse_saltstack_name(ip)
        self.cmd=cmd
    def execute(self):
        client=LocalClient()
	t=0
	str=""
        jid=client.cmd_async(self.tgt,'cmd.run',[self.cmd])
	while not client.get_cache_returns(jid):
		time.sleep(1)
		if t==10:
			str= "connection timeout"
			break
		else:
			t=t+1
			
	return client.get_cache_returns(jid)		 
			
    def save(self):
        pass
    

import time
class saltModuleTask(object):
    
    def __init__(self,task_name,ip,module,args):
        self.task_name=task_name
        self.tgt=parse_saltstack_name(ip)
        self.module=module
        self.args=args
    def execute(self):
        #return "ok"
        print "executeing"
        client=LocalClient()
	module_cmd=self.module+'.'+self.args
	print module_cmd
        jid=client.cmd_async(self.tgt,module_cmd)
	t=0
	while not client.get_cache_returns(jid):
		time.sleep(1)
		if t==10:
			print "timeout"
			break
		else:
			t=t+1
			print "job is on...."
	try:
		return client.get_cache_returns(jid)
	except:
		return {}


    def save(self):
        pass

