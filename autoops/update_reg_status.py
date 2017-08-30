import logging
logging.basicConfig()
import urllib2,httplib2,re
from apscheduler.schedulers.background import BackgroundScheduler
import os

#import MySQLdb
from DBUtils.PooledDB import PooledDB
import cx_Oracle
import os
oracle_conn={
    
    #uat
        'ENGINE': 'django.db.backends.oracle',
       'NAME': 'uatsrv1',
        'HOST':'172.16.49.200',
        'USER':'monitor',
        'PASSWD':'Mon#2016',
        'PORT':'1521',
        
    #downtown 
     #   """
     #'name': 'uatrac1',
     #   'host':'211.138.236.210',
     #   'user':'monitor',
     # 'passwd':'Mon#2016',
     #  'port':'41521'
    #   """

    }
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
print os.environ['NLS_LANG']
dns="{0}:{1}/{2}".format(oracle_conn['HOST'],oracle_conn['PORT'],oracle_conn['NAME'])
print dns
pool = PooledDB(cx_Oracle,mincached=20,maxcached=200,user = oracle_conn['USER'], password = oracle_conn['PASSWD'], dsn = dns)  
 
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
import cx_Oracle
oracle_conn={
     'ENGINE': 'django.db.backends.oracle',
        'name': 'monitor',
        'host':'172.16.21.71',
        'user':'monitor',
        'passwd':'M0#ni#tor',
        'port':'1521'
    }
def execute(sql_cmd):
        try:
            ret = []
            conn=pool.connection()
            cursor = conn.cursor()
            cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                    ret.append(row[0])
        except cx_Oracle.Error,e:
            print 'error'
        return ret
def executemany(sql_cmd):
        try:
            ret = []
            conn=pool.connection()
            cursor = conn.cursor()
            cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                ret.append(row)
        except cx_Oracle.Error,e:
            ret.append(e)
        return ret
def execute_update(sql_cmd):
        try:
            ret = []
            conn=pool.connection()
            cursor = conn.cursor()

            cursor.execute(sql_cmd)
            conn.commit()
            cursor.close()
            conn.close()
        except cx_Oracle.Error,e:
            ret.append(e)
import time
def get_http_request_list():
    http_request_list=[]
    query_reg_list_sql="select DISTINCT RegName from machineinfo"
    reg_list=execute(query_reg_list_sql)
    for item in reg_list:
        reg=item
        sql_query_ip_port="select b.IpAddress,a.HttpPort,a.HealthPage b.status from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName" %reg
        ip_port_object=executemany(oracle_conn,sql_query_ip_port)
        for item in ip_port_object:
            dic={}
            url="http://{0}:{1}/{2}".format(item[0].strip(),item[1],item[2])
            ipaddress=item[0].strip()
            status=item[3]
            httpport=item[1]
            dic['url']=url
            dic['ipaddress']=ipaddress
            dic['httpport']=httpport
            http_request_list.append(dic)
    return http_request_list

def update(dic):
	htt=httplib2.Http(".cache",timeout=5)
	status=0
	try:
        	response,content=htt.request(dic['url'],"GET")
        except Exception,e:
        	content='timeout'
                #print content
        if re.search(r'success',content):
                status=0
                        #sql="update machineinfo a set a.status=%d where exists(select 1 from appregioninfo b where b.HttpPort='%s' and a.IpAddress='%s' and a.regname=b.regname)" %(status,dic['httpport'],dic['ipaddress'])
        else:
            	status=1
        sql="update machineinfo a set a.status=%d where exists(select 1 from appregioninfo b where b.HttpPort='%s' and a.IpAddress='%s' and a.regname=b.regname)" %(status,dic['httpport'],dic['ipaddress'])
        #print sql
	try:
	       execute_update(sql)
        except:
            print "update Error...."

from multiprocessing import Pool
def update_status(list):
	p=Pool(20)
	for item in list:
		p.apply_async(update,args=(item,))
	p.close()
	p.join()
#	print 'end!!@'
import time
def main():
    start=time.time()
    list=get_http_request_list()
    p=Pool(20)
    for item in list:
        p.apply_async(update,args=(item,))
    p.close()
    p.join()
	#update_status(list)
    end=time.time()
    print "total",end-start
if __name__ == '__main__':
     print "==================================="
     print 'start collect regname status......'
     print "==================================="
     scheduler = BackgroundScheduler()
     scheduler.add_job(main, 'interval', seconds=40)
     scheduler.start()
     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
     try:
     	while True:
      		time.sleep(2)
     except (KeyboardInterrupt, SystemExit):
     	scheduler.shutdown()
