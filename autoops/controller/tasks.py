
from celery import task
from controller.action import Action
#from execute.task import TASK

@task
def restart(tgt,user,path,cmd):
    _salt_Action_object=Action(tgt,user,path,cmd)
    str=_salt_Action_object.restart() 
    return str
    

@task
def aix_restart(tgt,user,path,cmd):
     _aix_Action_object=Action(tgt,user,path,cmd)
     str=_aix_Action_object.aix_restart() 
     return str
     
def open():
    pass

@task
def close():
    pass
