
import urllib2, MySQLdb,httplib2,re
from apscheduler.schedulers.background import BackgroundScheduler
import os
import multiprocessing
conn={
      
         'ENGINE': 'django.db.backends.mysql',
        'name': 'autoops',
        'host':'172.16.49.170',
        'user':'root',
        'passwd':'Root15()',
        'port':'3306'
      }

def mysql_command(conn,sql_cmd):
        try:
            ret = []
            #print conn['host']
           # print conn['name']
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["passwd"],db=conn["name"],port=int(conn["port"]),charset="utf8")
            cursor = conn.cursor()
           # dictfetchall(cursor)
            cursor.execute(sql_cmd)
            return dictfetchall(cursor)
            #conn.commit()
            #cursor.close()
            #conn.close()
        except MySQLdb.Error,e:
            ret.append(e)
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    
def mysql_command_insert(conn,sql_cmd):
        try:
            ret = []
            #print conn['host']
           # print conn['name']
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["passwd"],db=conn["name"],port=int(conn["port"]),charset="utf8")
            cursor = conn.cursor()
           # dictfetchall(cursor)
            cursor.execute(sql_cmd)
            #sreturn dictfetchall(cursor)
            conn.commit()
            cursor.close()
            conn.close()
        except MySQLdb.Error,e:
            ret.append(e)
import time

def get_list():
   
    query_reg_list_sql="select DISTINCT RegName from asset_appregioninfo"
    reg_list=mysql_command(conn,query_reg_list_sql)
    list_update=[]
    for item in reg_list:
        status=0
        reg=item['RegName']
        sql_query_ip_port="select IpAddress,HttpPort,HealthPage from asset_appregioninfo where RegName='%s'" %reg
        ip_port_object=mysql_command(conn,sql_query_ip_port)
        
        for item in ip_port_object:
            list=[]
            list.append(item['IpAddress'])
            list.append(item['HttpPort'])
            list.append(item['HealthPage'])
            list_update.append(list)
    #print list_update
    return list_update
def multi_update():
    list=get_list()
    for item in list:    
        pool=multiprocessing.Pool(5)
        pool.map(update_status,(item,))
        pool.close()
        pool.join()



import httplib2
def update_status(item):
    htt=httplib2.Http(".cache",timeout=10)
    url="http://{0}:{1}/{2}".format(item['IpAddress'],item['HttpPort'],item['HealthPage'])
    print url
    try:
        resp,content=htt.request(url, "GET")
        time.sleep(1)
    except Exception,e:
        print 'connection fail'
    if re.search(r'success',content):
        status=0
        count_0+=1
    else:
        status=1
        count_1+=1
    sql="update asset_appregioninfo set status='%s' where IpAddress='%s' and HttpPort='%s'" %(status,item['IpAddress'],item['HttpPort'])
    print sql
    mysql_command_insert(conn,sql)
    print 'success'
    
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(multi_update, 'interval', seconds=10)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    update_status()