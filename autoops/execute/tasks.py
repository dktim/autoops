
from celery import task
import time
from shelltask import shelltask,para_conn
from execute.salttask import salttask
from execute.salttask import saltModuleTask
@task
def file_task(a,b):    
    time.sleep(10)
    c=a+b
    return c

@task
def shell_task_by_celery(task_name,tgt,cmd):
    t=shelltask(task_name,tgt,cmd)    
    return t.execute()
    
@task
def save_db(task_name,tgt,cmd):
    t=shelltask(task_name,tgt,cmd)
    t.save()


@task
def shell_task_by_celery_with_salt(task_name,tgt,cmd):
    t=salttask(task_name,tgt,cmd)
    return t.execute()
    
@task
def salt_task_by_celery_with_salt(task_name,tgt,module_name,args):
    t=saltModuleTask(task_name,tgt,module_name,args)
    return t.execute()
