#/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from salt.client import LocalClient

def tick(): 
    print 'tick.....and time is %s'% (datetime.now())
    cli=LocalClient()
    re=cli.cmd('*','cmd.run',["cd /opt -c 'cat aa.py"])
    print re
    f=open('aa.txt','w')
    f.write(str(re))
    f.close()
   # print re
import time
if __name__ == '__main__':
   sche=BackgroundScheduler()
   sche.add_job(tick, 'interval', seconds=3,max_instances=100)
   sche.start()
   #print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
   
  

   sche.shutdown() 