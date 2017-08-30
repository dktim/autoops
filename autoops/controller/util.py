
from autoops.oracle import OracleDb
from autoops import settings
from autoops.settings import oracle_conn

def parse_user(regname,ip):
    db=OracleDb()
    sql_cmd="select a.upduser from appregioninfo a,machineinfo b where a.regname='%s' and b.ipaddress='%s' and a.regname=b.regname"%(regname,ip)
    try:
        ret=db.execute(sql_cmd)
        return ret[0]
    except:
        return None
    

def cmd_history(**kwargs):
    db=OracleDb()
    ipaddress=kwargs['ip']
    regname=kwargs['regname']
    cmd=kwargs['cmd']
    user=kwargs['cmd']
    cmd_time=kwargs['cmd_time']
    sql="insert into cmd_history values('%s','%s','%s','%s','%s')"%(regname,ipaddress,cmd_time,cmd,user)
    try:
        db.execute_update(sql)
    except:
        pass


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    
def update_node_status(ip,reg,status):
    db=OracleDb()
    sql="update machineinfo set status=%d where ipaddress='%s' and regname='%s'"%(status,ip,reg)
    try:
        db.execute_update(sql)
    except:
        pass

def update_restart_status(d1,str,status,user,ip,mydate):
    db=OracleDb()
    sql_insert="insert into monitor.reg_restart_his values('%s','%s','%s','%s','%s','%s')"%(d1,str,unicode(status,'gbk'),user,ip,mydate)
    try:
        db.execute_update( sql_insert)
        return True
    except:
        return False
    
def get_all_hosts_by_regname(reg):
    db=OracleDb()
    sql="select distinct ipaddress from machineinfo where regname='%s'"%(reg)
    hosts=db.execute(sql)
    return {reg:hosts}


def get_ostype_by_ip(ip):
    db=OracleDb()
    sql="select OSTYPE from machineinfo where ipadddress='%s'"%(ip)
    os_type=db.execute(sql)
    return {ip:os_type}

def get_user_by_reg_and_ip(ip,reg):
    db=OracleDb()
    sql="select a.UPDUSER from appregioninfo a,machineinfo b where b.IpAddress='%s'and a.RegName='%s' and a.regname=b.regname" %(ip,reg)
    print sql
    upuser=db.execute(sql)
    return upuser[0]

if __name__ == '__main__':
    reg="PAY"
    print get_all_hosts_by_regname(reg)
    
