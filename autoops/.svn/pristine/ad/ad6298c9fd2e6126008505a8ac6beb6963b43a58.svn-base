import logging
from salt.client import LocalClient
logging.basicConfig()
import urllib2, MySQLdb,httplib2,re
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
import cx_Oracle
oracle_conn={
     'ENGINE': 'django.db.backends.oracle',
        'name': 'monitor',
        'host':'172.16.21.71',
        'user':'monitor',
        'passwd':'M0#ni#tor',
        'port':'1521'
    }
def oracle_command_direct(conn,sql_cmd):
        try:
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
            print e
            print 'error'
        return ret
def oracle_command(conn,sql_cmd):
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
def oracle_command_update(conn,sql_cmd):
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


def get_script_state(script_type):
	sql_query_appuser="select b.ipaddress,a.upduser,a.httpport from appregioninfo a,machineinfo b where a.regname in(select distinct regname from machineinfo) and a.regname=b.regname"
	ret=oracle_command(oracle_conn,sql_query_appuser)
	print ret
	ret_list=[]
	#f=open('/opt/aa.txt','wr+')
	for item in ret:
		sql="select salt_name from salt_ip where ip='{0}'".format(item[0])
		print sql
		salt_name=oracle_command_direct(oracle_conn,sql)
		command="su - {0} -c 'ls ~/bin |grep {1}'".format(item[1],script_type)
		list=[]
		if salt_name:
			#f=open('/opt/aa.txt','wr+')
			list.append(salt_name[0])
			list.append(command)
			ret_list.append(list)
			str="salt '%s' cmd.run '%s'"%(salt_name,command)
			#f.write(str.join('\n'))
			#f.close()
		else:
			print 'no target matched.'
	#f.close()
	return ret_list




if __name__=="__main__":
	list=get_script_state('open')
	for item in list:
		cmd="salt '%s' cmd.run '%s'"%(item[0],item[1])
		print cmd
