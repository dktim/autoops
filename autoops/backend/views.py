
from django.http.response import HttpResponse
import time
# Create your views here.
from django.views.decorators.csrf import csrf_exempt , csrf_protect
import json
#from django.http.sh
from backend.backendUtil import MachineInfo
from django.shortcuts import render_to_response, render
from backend.util import reg_host_user
from autoops.oracle import oracle_conn, OracleDb
from salt.client import LocalClient
import paramiko
def query_machine(request):
	list=['sfs','sfs','sss']
	return HttpResponse(json.dumps(list))


@csrf_exempt
def update_machine_info(request):
	hostname=request.POST.get('hostname')
	ostype=request.POST.get('ostype')
	version=request.POST.get('version')
	bit=request.POST.get('bit')
	ipaddress=request.POST.get('ipaddress')
	regname=request.POST.get('regname')
	desc=request.POST.get('desc')
	list=[hostname,ostype,version,bit,ipaddress,regname,desc]
	m=MachineInfo('','')
	data={}
	try:
		m.alert_machine(list,"add")
		data['flag']="success"
	except:
		data['flag']="fail"
	return HttpResponse(json.dumps(data),content_type="applicaiton/json")


def add_machine_info(request):
	return render_to_response('backend/machine_add.html',locals())

import autoops.oracle
import backend.util
def multi_host(request):
	sql="select a.regname,a.upduser,b.ipaddress from machineinfo b,appregioninfo a where a.regname=b.regname"
	db_instance=OracleDb(oracle_conn,'query_multi_item',sql)
	ret=db_instance.execute()
	hosts=[]
	for item in ret:
		dic={}
		dic['regname']=item[0]
		dic['username']=item[1]
		dic['ipaddress']=item[2]
		hosts.append(dic)
	count=len(hosts)
	recent_tasks={}
	return render_to_response("controller/hosts_multi.html",{'bind_host':hosts,'count':count})


def aa(request):
	return HttpResponse(aa)

import host_mgr
@csrf_exempt
def multitask_cmd(request):
	multi_task = host_mgr.MultiTask('run_cmd',request)
	re=multi_task.run()
	return HttpResponse(re)


def multitask_res(request):
	print "geting@@@"
	multi_task = host_mgr.MultiTask('get_task_result',request)
	task_result=multi_task.run()
	
	return HttpResponse(task_result)
	


def query_file_h(request):
    sql_parse_ip_user="select a.ipaddress,a.ostype,a.regname,b.appuser,b.appuser from machineinfo a,appregioninfo b where a.regname=b.regname"

    db_instance=OracleDb(oracle_conn,'query_multi_item',sql_parse_ip_user)
    ret=db_instance.execute()
    f=file('/opt/list_restart.txt','a+')
    list=[]
    for item in ret:
        dic={}
        dic['ip']=item[0]
        dic['os']=item[1]
	dic['reg']=item[2]
        dic['upduser']=item[3]
        dic['appuser']=item[4]
        list.append(dic)
    for item in list:
        salt_name_ip="select salt_name from salt_ip where ip='%s'"%item['ip']
        db_instance=OracleDb(oracle_conn,'query_single_item',salt_name_ip)
        ret=db_instance.execute()
	if ret:
            salt_name=ret[0]
        else:
            salt_name='None'
        if item['os']=='AIX':
		print "writing AIX",item['ip']
            	ssh=paramiko.SSHClient()
            	pkey="/root/.ssh/id_rsa"
            	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            	key=paramiko.RSAKey.from_private_key_file(pkey)
		try:
            		ssh.connect(item['ip'],22,item['appuser'],pkey=key)
            		command="ls ~/bin/ | grep h_restart "
            		stdin,stdout,stderr = ssh.exec_command(command,timeout=20)
		except:
			print "excepting"
		if stderr:
			f.write(item['ip']+':'+item['reg']+':'+item['appuser']+':'+stderr.read()+'\n')
		else:
        		f.write(item['ip']+':'+item['reg']+':'+item['appuser']+':'+stdout.read()+'\n')
	elif item['os']=='REDHAT':
		print 'writing REDHAT',item['ip']
	 	salt_name_ip="select salt_name from salt_ip where ip='%s'"%item['ip']
        	db_instance=OracleDb(oracle_conn,'query_single_item',salt_name_ip)
        	ret=db_instance.execute()
        	if ret:
            		salt_name=ret[0]
        	else:
            		salt_name='None'

            	client=LocalClient()
           	str="su - %s -c 'ls ~/bin | grep h_restart'"%(item['appuser'])

            	jid=client.cmd_async(salt_name,'cmd.run',[str])
            	#time.sleep(5)
            	ret_list=client.get_cache_returns(jid)
	    	time.sleep(20)
            	try:
                	ret_list=client.get_cache_returns(jid)
			ret_content=ret_list[salt_name]['ret']
			print "start print content:REDHAT"
			f.write(item['ip']+':'+item['reg']+':'+item['appuser']+':'+ret_content+'\n')
	    	except:
			ret_content="None data"
			print "start print REDHAT:Error"
                	f.write(item['ip']+':'+item['reg']+':'+item['appuser']+':'+ret_content+'\n')
		 
    f.close()
    return HttpResponse("ok")
   
   
   
def test(request):
 	context={}
 	return render(request,'test.html',context)
