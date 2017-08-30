#coding:utf-8
from salt.client import LocalClient
import re
import sys
from monitor.sshutil import ssh_connection
reload(sys)
#sys.setdefaultencoding('utf-8')
from logging import exception
from autoops.oracle import OracleDb
from autoops.settings import oracle_conn as db_conn
from datetime import datetime
import time
class Action(object):
    def __init__(self,tgt,user,path,cmd):
        self.tgt=tgt
        self.user=user
        self.path=path
        self.cmd=cmd
   
    def aix_restart(self):
        ssh=ssh_connection(self.tgt,self.user)
        _command="sh ~/bin/h_restart.sh"
        cmd_return=""
        cmd_result={}
        t=0
        stdin,stdout,stderr=ssh.exec_command(_command,timeout=500)
        while not stdout and not stderr:
            time.sleep(1)
            if t==500:
                return 'timeout'
                break
            else:
                t=t+1
                print 'not yet over'
        if stderr:
            return "execute error"
        else:
            return stdout.readlines()
            
        
    def restart(self):
        client=LocalClient()
        _command="su - %s -c 'sh ~/bin/h_restart.sh'"%(self.user)
        cmd_return=""
        cmd_result={}
        t=0
        jid=client.cmd_async(self.tgt,'cmd.run',[_command])
        while client.get_cache_returns(jid)=={}:
            time.sleep(1)
            if t==500:
                return "timeout"
                break
            else:	
                t=t+1
                print "not yet get.."
        try:
            cmd_result=client.get_cache_returns(jid)
        except:
            cmd_result={self.tgt:{'ret':""}}
        return unicode(cmd_result[self.tgt]['ret'],'gbk')
        

def parse_restart_result(str):
    if re.match('boot succeed',str):
        return 'success'
    elif re.match('fail',str):
        return 'fail'
    elif re.match('no minion',str):
        return 'no minion target found'
    elif re.match('timeout',str):
	return "timeout"
    else:
        return 'other fail' 
    
def update_restart_status(str,status,user,ip,mydate):
        _up_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db=OracleDb()
        sql_insert="insert into monitor.reg_restart_his values('%s','%s','%s','%s','%s','%s')"%(_up_time,str,unicode(status,'gbk'),user,ip,mydate)
        try:
            db.execute_update(sql_insert)
            return True
        except:
            return False    
    
