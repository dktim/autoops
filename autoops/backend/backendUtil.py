
from autoops.oracle import OracleDb
from autoops.settings import oracle_conn

class MachineInfo():
    def __init__(self,db,conn):
        self.db=OracleDb
        self.conn=oracle_conn
    def alert_machine(self,list,aciton):
        if aciton=="add":
            sql="insert into machineinfo(hostname,ostype,version,bit,ipaddress,regname,status,description) values('%s','%s','%s','%s','%s','%s',%d,'%s')"%(list[0],
                                                                                                                                                            
            list[1],list[2],list[3],list[4],list[5],0,list[6])
            try:    
                print sql
                self.db.execute_update(sql)
            except:                 
                print "add error"                                                                  
            