#coding:utf-8
#import cx_Oracle
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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
import sys    
if __name__ == '__main__':
    #oracle_db=cx_Oracle.connect('monopr/ayo#1234@172.16.49.200:1521/uatsrv1')
    #print oracle_db
    #oracle_cur=oracle_db.cursor(
    print sys.path
    sql_query_max_seq="select max(SEQNUM) as max from asset_jdbcstat"
    
    ret=mysql_command(conn, sql_query_max_seq)
   # data=mysql_cur.fetchone()
    print ret
    #oracle_cur.execute(sql)
    #print oracle_cur.fetchone()
    #for line in oracle_cur.fetchall():
      #  print line
