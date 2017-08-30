import cx_Oracle
import MySQLdb


if __name__ == '__main__':
    oracle_db=cx_Oracle.connect('monopr/ayo#1234@172.16.49.200:1521/uatsrv1')
    print oracle_db
    oracle_cur=oracle_db.cursor()
    mysql_db=MySQLdb.connect('172.16.49.170','root','Root15()','autoops',3306,'utf-8')
    mysql_cur=mysql_db.cursor()
    
    sql_query_max_seq="select max(SEQNUM) from asset_jdbc"
    
    mysql_cur.execute(sql_query_max_seq)
    data=mysql_cur.fetchone()
    print data
    #oracle_cur.execute(sql)
    #print oracle_cur.fetchone()
    #for line in oracle_cur.fetchall():
      #  print line
