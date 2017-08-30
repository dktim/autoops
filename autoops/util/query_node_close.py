def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
minion2ip=[



{'ip':'172.16.49.100','salt_name':'172.16.49.100_uat-wangguang'},

{'ip':'172.16.49.103','salt_name':'172.16.49.103_sit1-centos'},
{'ip':'172.16.49.104','salt_name':'172.16.49.104_sit2-centos'},
{'ip':'172.16.49.107','salt_name':'172.16.49.107_localhost.localdomain'},
{'ip':'172.16.49.108','salt_name':'172.16.49.108_testapp'},
{'ip':'172.16.49.110','salt_name':'172.16.49.110_uat-yxmg'},
{'ip':'172.16.49.111','salt_name':'172.16.49.111_uat-yxmg2'},
{'ip':'172.16.49.112','salt_name':'172.16.49.112_uat-yxmg3'},
{'ip':'172.16.49.114','salt_name':'172.16.49.114_uat-ptc'},
{'ip':'172.16.49.115','salt_name':'172.16.49.115_uat-weixin'},
{'ip':'172.16.49.117','salt_name':'172.16.49.117_hejb-sybase'},
{'ip':'172.16.49.120','salt_name':'172.16.49.120_RHEL'},
{'ip':'172.16.49.123','salt_name':'172.16.49.123_hykf'},
{'ip':'172.16.49.126','salt_name':'172.16.49.126_uat-jiufu'},
{'ip':'172.16.49.127','salt_name':'172.16.49.127_uat-yhksd'},
{'ip':'172.16.49.133','salt_name':'172.16.49.133_localhost.localdomain'},
{'ip':'172.16.49.135','salt_name':'172.16.49.135_redisapp1'},
{'ip':'172.16.49.136','salt_name':'172.16.49.136_redisapp2'},
{'ip':'172.16.49.137','salt_name':'172.16.49.137_localhost.localdomain'},
{'ip':'172.16.49.138','salt_name':'172.16.49.138_UATRACDG'},
{'ip':'172.16.49.140','salt_name':'172.16.49.140_sit-txyzm'},
{'ip':'172.16.49.148','salt_name':'172.16.49.148_PTCF'},
{'ip':'172.16.49.149','salt_name':'172.16.49.149_app1'},
{'ip':'172.16.49.152','salt_name':'172.16.49.152_dyy-uat'},
{'ip':'172.16.49.159','salt_name':'172.16.49.159_qing_js'},
{'ip':'172.16.49.176','salt_name':'172.16.49.176_RHEL'},
{'ip':'172.16.49.177','salt_name':'172.16.49.177_RHEL'},
{'ip':'172.16.49.178','salt_name':'172.16.49.178_RHEL'},
{'ip':'172.16.49.179','salt_name':'172.16.49.179_uat-weixinH5'},
{'ip':'172.16.49.180','salt_name':'172.16.49.180_ylcspay'},
{'ip':'172.16.49.181','salt_name':'172.16.49.181_localhost.localdomain'},
{'ip':'172.16.49.182','salt_name':'172.16.49.182_ylcsfun'},
{'ip':'172.16.49.183','salt_name':'172.16.49.183_localhost.localdomain'},
{'ip':'172.16.49.184','salt_name':'172.16.49.184_localhost.localdomain'},
{'ip':'172.16.49.185','salt_name':'172.16.49.185_localhost.localdomain'},
{'ip':'172.16.49.186','salt_name':'172.16.49.186_localhost.localdomain'},
{'ip':'172.16.49.187','salt_name':'172.16.49.187_ylcsdb'},
{'ip':'172.16.49.188','salt_name':'172.16.49.188_cdp'},
{'ip':'172.16.49.189','salt_name':'172.16.49.189_TestMemcache'},
{'ip':'172.16.49.191','salt_name':'172.16.49.191_uatdbrac1'},
{'ip':'172.16.49.193','salt_name':'172.16.49.193_uatdbrac2'},
{'ip':'172.16.49.197','salt_name':'172.16.49.197_RHEL'},
{'ip':'172.16.49.19','salt_name':'172.16.49.19_versionsvr'},
{'ip':'172.16.49.201','salt_name':'172.16.49.201_uat-trackuser1'},
{'ip':'172.16.49.202','salt_name':'172.16.49.202_uat-trackuser2'},
{'ip':'172.16.49.206','salt_name':'172.16.49.206_uat-yuebao'},
{'ip':'172.16.49.207','salt_name':'172.16.49.207_uat-messaqueue1'},
{'ip':'172.16.49.208','salt_name':'172.16.49.208_uat-messaqueue2'},
{'ip':'172.16.49.210','salt_name':'172.16.49.210_puppetmaster'},
{'ip':'172.16.49.211','salt_name':'172.16.49.211_mdlsvr_uat'},
{'ip':'172.16.49.224','salt_name':'172.16.49.224_RHEL'},
{'ip':'172.16.49.233','salt_name':'172.16.49.233_rhel'},
{'ip':'172.16.49.240','salt_name':'172.16.49.240_uat-txyzm'},
{'ip':'172.16.49.241','salt_name':'172.16.49.241_master1'},
{'ip':'172.16.49.242','salt_name':'172.16.49.242_master2'},
{'ip':'172.16.49.243','salt_name':'172.16.49.243_data1'},
{'ip':'172.16.49.244','salt_name':'172.16.49.244_data2'},
{'ip':'172.16.49.245','salt_name':'172.16.49.245_data3'},
{'ip':'172.16.49.35','salt_name':'172.16.49.35_master1'},
{'ip':'172.16.49.38','salt_name':'172.16.49.38_master2'},
{'ip':'172.16.49.39','salt_name':'172.16.49.39_data1'},
{'ip':'172.16.49.40','salt_name':'172.16.49.40_data2'},
{'ip':'172.16.49.41','salt_name':'172.16.49.41_data3'},
{'ip':'172.16.49.43','salt_name':'172.16.49.43_uat-ptkj'},
{'ip':'172.16.49.45','salt_name':'172.16.49.45_sit-ptc'},
{'ip':'172.16.49.46','salt_name':'172.16.49.46_RHEL'},
{'ip':'172.16.49.47','salt_name':'172.16.49.47_RHEL'},
{'ip':'172.16.49.48','salt_name':'172.16.49.48_RHEL'},
{'ip':'172.16.49.50','salt_name':'172.16.49.50_RHEL'},
{'ip':'172.16.49.57','salt_name':'172.16.49.57_sit-arp'},
{'ip':'172.16.49.62','salt_name':'172.16.49.62_rhel'},
{'ip':'172.16.49.63','salt_name':'172.16.49.63_uat-eticket'},
{'ip':'172.16.49.68','salt_name':'172.16.49.68_RHEL'},
{'ip':'172.16.49.69','salt_name':'172.16.49.69_RHEL'},
{'ip':'172.16.49.71','salt_name':'172.16.49.71_SFRAC1'},
{'ip':'172.16.49.72','salt_name':'172.16.49.72_SFRAC2'},
{'ip':'172.16.49.76','salt_name':'172.16.49.76_rhel'},
{'ip':'172.16.49.77','salt_name':'172.16.49.77_RHEL'},
{'ip':'172.16.49.78','salt_name':'172.16.49.78_RHEL'},
{'ip':'172.16.49.79','salt_name':'172.16.49.79_test'},
{'ip':'172.16.49.81','salt_name':'172.16.49.81_uat-yhmk'},
{'ip':'172.16.49.82','salt_name':'172.16.49.82_uat-czcf'},
{'ip':'172.16.49.83','salt_name':'172.16.49.83_uat-dxmk'},
{'ip':'172.16.49.84','salt_name':'172.16.49.84_uat-syt'},
{'ip':'172.16.49.86','salt_name':'172.16.49.86_sword-sit'},
{'ip':'172.16.49.87','salt_name':'172.16.49.87_RHEL'},
{'ip':'172.16.49.88','salt_name':'172.16.49.88_kafka1'},

{'ip':'172.16.49.89','salt_name':'172.16.49.89_kafka2'},

{'ip':'172.16.49.91','salt_name':'172.16.49.91_sit-yhmk'},
{'ip':'172.16.49.92','salt_name':'172.16.49.92_sit-czcf'},
{'ip':'172.16.49.93','salt_name':'172.16.49.93_sit-dxcf'},
{'ip':'172.16.49.94','salt_name':'172.16.49.94_rrs-sit'},

{'ip':'172.16.49.95','salt_name':'172.16.49.95_sit-syt'},

{'ip':'172.16.49.96','salt_name':'172.16.49.96_RHEL'},
{'ip':'172.16.49.97','salt_name':'172.16.49.97_RHEL'},
{'ip':'172.16.50.241','salt_name':'172.16.50.241_EVC_TEST_02'},
{'ip':'172.16.50.242','salt_name':'172.16.50.242_EVC_TEST_03'},

{'ip':'172.16.50.243','salt_name':'172.16.50.243_JNKY_TEST'},

{'ip':'172.16.50.244','salt_name':'172.16.50.244_dazongapp'},
{'ip':'172.16.50.245','salt_name':'172.16.50.245_dazongdb'},
{'ip':'172.16.49.171','salt_name':'salt-minion-171'},
{'ip':'172.16.49.172','salt_name':'salt-minion-172'},

{'ip':'172.16.49.173','salt_name':'salt-minion-173'}


]
conn={
      
         'ENGINE': 'django.db.backends.mysql',
        'name': 'autoops',
        'host':'172.16.49.170',
        'user':'root',
        'passwd':'Root15()',
        'port':'3306'
      }
from salt.client import LocalClient
import MySQLdb
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
          #  for row in cursor.fetchall():
          #      for i in row:
          #          ret.append(i)

        except MySQLdb.Error,e:
            ret.append(e)

def mysql_command_update(conn,sql_cmd):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["passwd"],db=conn["name"],port=int(conn["port"]),charset="utf8")
            cursor = conn.cursor()
           
            cursor.execute(sql_cmd)
            conn.commit()
            cursor.close()
            conn.close()
        except MySQLdb.Error,e:
            ret.append(e)
import re
if __name__ == '__main__':
    
    loc=LocalClient()
    sql='select IpAddress,UpdUser, IpAddress from asset_appregioninfo'
    ret=mysql_command(conn,sql)
    
    for item in ret:
        tgt=''
        ip=item['IpAddress']
        for l in minion2ip:
            if ip==l['ip']:
                tgt=l['salt_name']
        if tgt:
            user=item['UpdUser']
            str="su - %s -c 'sh ~/bin/close.sh'" %user
            salt_ret=loc.cmd(tgt,'cmd.run',[str])
            print salt_ret
            if salt_ret[tgt]=='':
                print tgt+'@'+user+'@'+'success'
            else:
                if re.search(r'No such',salt_ret[tgt]):
                    print tgt+'@'+user+'@'+'no such file'
                else:
                    print tgt+'@'+user+'@'+'fail'
        
        
        
        