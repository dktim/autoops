# -*- coding: utf-8 -*-
#import MySQLdb
from DBUtils.PooledDB import PooledDB
import cx_Oracle
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
print os.environ['NLS_LANG']
from autoops.settings import oracle_conn
dns="{0}:{1}/{2}".format(oracle_conn['HOST'],oracle_conn['PORT'],oracle_conn['NAME'])
print dns
pool = PooledDB(cx_Oracle,mincached=20,maxcached=200,user = oracle_conn['USER'], password = oracle_conn['PASSWD'], dsn = dns)  
 
class OracleDb:
  #  def __init__(self,conn):
   #     pass
    def execute(self,sql_cmd):
        try:
            result = []
            conn=pool.connection()
            cursor = conn.cursor()
            cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                    result.append(row[0])
        except cx_Oracle.Error,e:
            pass
        return result
    def executemany(self,sql_cmd):
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
    """   
    def query_single(self,conn,sql_cmd):
        try:
            ret = []
            conn_str="{0}/{1}@{2}:{3}/{4}".format(conn['USER'],conn['PASSWD'],conn['HOST'],conn['PORT'],conn['NAME'])
            #conn=cx_Oracle.connect(conn_str)
            conn=pool.connection()
            cursor = conn.cursor()
            cursor.execute(sql_cmd)
            for row in cursor.fetchone():
                ret.append(row[0])
        except cx_Oracle.Error,e:
            ret.append(e)
        return ret
    """   
    
    
    def execute_update(self,sql_cmd):
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
           


if __name__ == '__main__':
    pass
    
