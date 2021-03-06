import logging
logging.basicConfig()
import urllib2,httplib2,re
from apscheduler.schedulers.background import BackgroundScheduler
import os
conn={
      
         'ENGINE': 'django.db.backends.mysql',
        'name': 'autoops',
        'host':'172.16.21.60',
        'user':'root',
        'passwd':'Root#15',
        'port':'3306'
      }
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
            print 'entering@!'
            ret = []
            conn_str="{0}/{1}@{2}:{3}/{4}".format(conn['user'],conn['passwd'],conn['host'],conn['port'],conn['name'])


            conn=cx_Oracle.connect(conn_str)
            #print conn
            cursor = conn.cursor()
            #print cursor
            cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                   # print row
                    ret.append(row[0])
        except cx_Oracle.Error,e:
            #print e
            print 'error'
        return ret
def exexutemany(sql_cmd):
        try:
            ret = []
            conn_str="{0}/{1}@{2}:{3}/{4}".format(conn['user'],conn['passwd'],conn['host'],conn['port'],conn['name'])
            conn=cx_Oracle.connect(conn_str)
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
            conn_str="{0}/{1}@{2}:{3}/{4}".format(conn['user'],conn['passwd'],conn['host'],conn['port'],conn['name'])
            conn=cx_Oracle.connect(conn_str)
            cursor = conn.cursor()

            cursor.execute(sql_cmd)
            conn.commit()
            cursor.close()
            conn.close()
        except cx_Oracle.Error,e:
            ret.append(e)
import time
def get_http_request_list():
    #import httplib2
    #count_1=0
    #count_0=0
    http_request_list=[]
    #htt=httplib2.Http(".cache",timeout=10)
    query_reg_list_sql="select DISTINCT RegName from machineinfo"
    reg_list=execute(oracle_conn,query_reg_list_sql)
    #print reg_list
    #file_suc=open('/opt/suc.txt','wd')
    #file_fail=open('/opt/fail.txt','wd')
    for item in reg_list:
        #status=0
        reg=item
        sql_query_ip_port="select b.IpAddress,a.HttpPort,a.HealthPage from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName" %reg
        #print sql_query_ip_port
        ip_port_object=execute(sql_query_ip_port)
       # print ip_port_object
        for item in ip_port_object:
            dic={}
            url="http://{0}:{1}/{2}".format(item[0].strip(),item[1],item[2])
 	    ipaddress=item[0].strip()
            httpport=item[1]
            dic['url']=url
            dic['ipaddress']=ipaddress
            dic['httpport']=httpport
            http_request_list.append(dic)
    #print http_request_list
    return http_request_list

def update(dic):
	htt=httplib2.Http(".cache",timeout=10)
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
	
	execute_update(oracle_conn,sql)


from multiprocessing import Pool
def update_status(list):
	p=Pool(20)
	for item in list:
		p.apply_async(update,args=(item,))
	p.close()
	p.join()
def main():
	import time
	start=time.time()
	list=get_http_request_list()
	update_status(list)
	end=time.time()
	print "total",end-start
if __name__ == '__main__':
     print 'start reg statue!'
     scheduler = BackgroundScheduler()
     scheduler.add_job(main, 'interval', seconds=20)
     scheduler.start()

     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

     try:
        # This is here to simulate application activity (which keeps the main thread alive).
     	while True:
      		time.sleep(2)
     except (KeyboardInterrupt, SystemExit):
     	scheduler.shutdown()
