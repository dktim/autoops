from django.shortcuts import render, render_to_response
from saltcore.salt_core import SaltAPI
from autoops.oracle import OracleDb
from autoops.settings import oracle_conn
import time
from job import job
from django.contrib.auth.decorators import login_required
from execute.shelltask import shelltask
from celery.result import AsyncResult
from .tasks import shell_task_by_celery,shell_task_by_celery_with_salt
from .tasks import save_db
from .tasks import salt_task_by_celery_with_salt
from django.contrib.admin.templatetags.admin_list import result_list
from controller.util import get_all_hosts_by_regname
db=OracleDb()

def get_hosts_by_reg(reg,conn):
    sql="select distinct ipaddress from machineinfo where regname='%s'" %reg
    _result=db.execute(sql)
    return {reg:_result}
    
@login_required
def shell_cmd(request):
    """
    db=OracleDb()
    _u=request.user
    query_groups="select distinct regname from machineinfo"
    regs=db.oracle_command_direct(oracle_conn, query_groups)
    reg='PAY'
    all={}
    print get_all_hosts_by_regname(reg)
    for reg in regs:
        reg_dic=get_all_hosts_by_regname(reg)
        all.update(reg_dic) 
    print all
    """
    all={'g1':['172.16.49.170','172.16.49.172','172.16.49.171'],'wch1':{'172.29.43.11','172.29.43.12','172.29.43.13','172.29.43.14','172.29.43.15','172.29.43.16','172.29.43.17','172.29.43.18'}}
    return render(request,"execute/minions_shell_runcmd.html",{"list_groups":all})


@login_required
def shell_result(request):  
    _u = request.user
    _host_list=request.POST.getlist('hosts_name')
    _cmd=request.POST.get('cmd')
    if _cmd:
        _cmd=_cmd
    result = {}
    minion_id_list = []
    line = "################################################################"
    host_count=len(_host_list)
    cmd_success=0
    cmd_failure=0
    succeed_host = []
    failure_host=[]
    result=[]
    state=""
    task_ids=[]
    for _h in _host_list:
        r=shell_task_by_celery_with_salt.apply_async(['task'+_h,_h,_cmd])
        task_ids.append({'host':_h,
                         'task_id':r})
    for task in task_ids:
        result.append({task['host']:task['task_id'].get()})
        print task['task_id'].get()
    """
    for re in task_ids:
        
        is_ready=re.ready()
        rr=re.get()
        print rr
        
        print  is_ready
        if is_ready:
            #if re.successful():
            #if re.get()=="exec Error" or re.get()==None:
            cmd_success+=1
            #else:
        else:
            cmd_failure+=1 #   cmd_failure+=1
        result.append({_h:re.result})
        r1=save_db.apply_async(['task'+_h,_h,_cmd])
        """
    #cmd = 'Command: ' + _cmd
    cmd_success=0
    cmd_failure=0
    succeed_minion = []
    return render(request, 'execute/minions_shell_result.html', {'result': result,
                                                                     'cmd': _cmd,
                                                                     'line': line,
                                                                     'minion_count': host_count,
                                                                     'cmd_succeed': cmd_success,
                                                                     'cmd_failure': cmd_failure,
                                                                     'failure_minion': failure_host,
                                                                     'succeed_host':succeed_host
                                                                     })

@login_required
def salt_runcmd(request):
	"""
    db=OracleDb()
    _u=request.user
    query_groups="select distinct regname from machineinfo"
    regs=db.oracle_command_direct(oracle_conn, query_groups)
    all={}
    for reg in regs:
        reg_dic=get_all_hosts_by_regname(reg)
        all.update(reg_dic) 
    print all
	"""
    	modindex=[{'module_name':'t_time'},{'module_name':'hi_util'}]
    	all={'wch':['172.29.43.11','172.29.43.12','172.29.43.13','172.29.43.14','172.29.43.15','172.29.43.16','172.29.43.17','172.29.43.18']}
    	return render(request,"execute/minions_salt_runcmd.html",{"list_groups":all,'modindex':modindex})
def salt_result(request):
   	_u = request.user
	result=[]
	task_ids=[]    	
	line = "################################################################"
    	if request.POST:
        	host_list = request.POST.getlist("hosts_name")
        	salt_fun = request.POST.get('salt_fun')
        	salt_arg = request.POST.get('salt_arg').strip()
	for host in host_list:
		r=salt_task_by_celery_with_salt.delay('task'+host,host,salt_fun,salt_arg)
		task_ids.append({'host':host,
                         'task_id':r})
	for task in task_ids:
		task_result=task['task_id'].get()
        	result.append({task['host']:task_result})
        minion_count = 'Total: ' + str(len(host_list))
        succeed_minion = []
	return render(request, 'execute/minions_salt_result.html', {'result': result,
                                                                     'cmd': 'cmd',
                                                                     'line': line,
                                                                     'minion_count': minion_count,
                                                                     'cmd_succeed': 1,
                                                                     'cmd_failure': 2,
                                                                     'failure_minion': 'sdfs',
                                                                     'succeed_host':'sdfs'
                                                                     })





@login_required
def jobs_his(request):
    jids={'jids':[1,2,2,3],'info':['s','d','d','g']}
    return render(request, 'execute/jobs_history.html', {'jids': jids})

from tasks import file_task
@login_required
def test_celery(request):
    c=file_task.delay(1,6)
    time.sleep(3)
    return render(request,'execute/test_celery.html',{'str':c.get()})
    
    
