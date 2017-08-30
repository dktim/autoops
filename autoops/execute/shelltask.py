from task import TASK
import paramiko
import time
import logging
from celery import Task
from autoops.settings import oracle_conn
from autoops.oracle import OracleDb
def para_conn(ip,user,passwd): 
        try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, 22, user, passwd,timeout=2)
                return ssh
        except:
                return None
                logging.info('Error')
        ssh.close()


class shelltask():
    
    def __init__(self,task_name,tgt,_cmd):
        self.task_id=str(time.time()) + task_name
        self.task_name=task_name
        self.tgt=tgt
        self._cmd=_cmd
        
    def save(self):
        db=OracleDb()
        sql="""
        insert into JOBINFO(job_id,target,action,state,begin_tm,end_tm) 
        values('%s','%s','%s','%s','%s','%s')
    
    """%('sdfsfs111',self.tgt,self._cmd,'sucsf','sfds','sfsd')
        db.execute_update(sql)
    def execute(self):
        ssh=para_conn(self.tgt,'root','Root15()')
        if ssh!=None:
            stdin,stdout,stderr=ssh.exec_command(self._cmd,10)
            return stdout.read()
           
        else:
            return 'exec Error'
     
     
      
        