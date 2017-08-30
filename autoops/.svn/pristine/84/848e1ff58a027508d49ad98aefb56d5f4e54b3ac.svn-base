#/usr/bin/python
# -*- coding: utf-8 -*-
#/usr/bin/env python
#coding:utf-8

import json
import time
try:
    import MySQLdb
    HAS_MYSQL=True
except ImportError:
    HAS_MYSQL=False
__virtualname__='test_mysql'
def __virtual__():
    if not HAS_MYSQL:
        return False
    else:
        return  __virtualname__
def returner(ret):
    conn=MySQLdb.connect(host='192.168.92.128',user='root',passwd='admin',db='salt',port=3306)
    cursor=conn.cursor()
    sql='INSERT INTO salt_returns(`fun`,`jid`,`return`,`id`,`success`,`full_ret`) VALUES(%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql % (str(json.dumps(ret['fun'])),str(json.dumps(ret['jid'])),
    str(json.dumps(ret['return'])),str(json.dumps(ret['id'])),
    '"'+str(ret['success'])+'"',"'"+json.dumps(ret)+"'"))
    conn.commit()
    cursor.close()
    conn.close()