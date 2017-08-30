import time
import datetime
import json
from autoops.oracle import OracleDb,oracle_conn
from backend.util import exe_salt_command, get_current_time
class MultiTask(object):
    def __init__(self,task_type,request_ins):
        self.request = request_ins
        self.task_type = task_type

    def run(self):
        return self.parse_args()
    def parse_args(self):
        task_func = getattr(self,self.task_type)
        return task_func()
    def run_cmd(self):
        cmd=self.request.POST.get('cmd')
        hosts=self.request.POST.get('selected_hosts')
        cur_time=get_current_time()
        task_id=time.time()*1000
        hosts=['172.29.73.70_MavenDB','172.29.74.11_hbd11']
        for host in hosts:
            result,jid=exe_salt_command(host,'cmd.run',cmd)
            sql="insert into multitask(t_id,host,j_id,success,ret,starttime,endtime) values('%s','%s','%s',%d,'%s','%s','%s')"%(task_id,host,jid,1,result,get_current_time(),get_current_time())
            db=OracleDb(oracle_conn,'update_multi_item',sql)
            db.execute()
        return task_id
    

    
    def get_task_result(self,detail=True):
        '''get multi run task result'''
        task_id = self.request.GET.get('task_id')
        log_dic ={}
        sql="select host,t_id,success,ret,j_id from multitask where t_id='%s'"%(task_id)
        db=OracleDb(oracle_conn,"query_multi_item",sql)
        result=db.execute()
        list=[]
        for item in result:
            dic={
            'id':item[1] ,
            'host':item[0],
            'success':item[2],
            'ret': item[3],
            'j_id': item[4]
          }
            list.append(dic)
        return json.dumps(list)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def update_task_exec_db(self):
        pass
