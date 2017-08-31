#coding:utf-8
import sys
from execute.salttask import parse_saltstack_name
from salt.cloud.clouds.lxc import _salt
from string import upper
from account.models import UserProfiles
reload(sys)
import re
from autoops.permission import check_permission
#sys.setdefaultencoding('utf8')
from django.shortcuts import render,render_to_response,HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from monitor.sshutil import *
from controller.util import update_restart_status,get_user_by_reg_and_ip
import datetime
from controller.util import update_node_status
from autoops import settings
from django.db import connection
from util import dictfetchall
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json,time
from autoops.oracle import OracleDb
from django.http import JsonResponse
from monitor.sshutil import ssh_connection
from regex.regex import *
from salt.client import LocalClient
import httplib2
from urllib2 import Request,urlopen,URLError,HTTPError
import logging
from autoops.celery import app
from controller.util import cmd_history
@login_required
def app_cont(request):
     cur=connection.cursor()
     cur.execute('select DISTINCT t1.HostName,t2.IpAddress,t2.RegName,t2.AppUser,t2.status,t2.`Desc` from machineinfo as t1,asset_appregioninfo as t2 where t1.IpAddress=t2.IpAddress;')
     dic=dictfetchall(cur)
    
     return render_to_response('controller/app_cont.html',{'dic':dic})

@login_required
def machineinfo_list(request,reg=None):
	db=OracleDb()
	if reg is not None:
		reg=reg
	else:
		reg="IPS"
	sql="select hostname,ostype,version,bit,ipaddress,regname,description from machineinfo where regname='%s'" %reg
	ret=db.execute(sql)
	list=[]
	for item in ret:
		dic={
            'hostname':item[0],
            'ostype':item[1],
            'version':item[2],
            'bit':item[3],
            'ipaddress':item[4],
            'regname':item[5],
            'desc':unicode(item[6],'gbk')
            }
		list.append(dic)
	paginator=Paginator(list,15)
	try:
		page=int(request.GET.get('page',1))
	except ValueError:
		page=1
	try:
		machine_list=paginator.page(page)
	except:
		machine_list=paginator.page(1)
	sql="select distinct Regname from appregioninfo";
	query_reg_ret=db.execute(sql)
	category=[]
	for item in query_reg_ret:
		category.append(item[0])
	return render_to_response("controller/machineinfo.html",locals())

@login_required
def get_node_state(request):
    ip=request.GET.get('ip')
    ip=ip.strip()
    reg=request.GET.get('reg')
    db=OracleDb()
    sql_query_ports="select a.HttpPort,a.RegName,b.status,b.in_use from appregioninfo a,machineinfo b where b.IpAddress='%s' and b.RegName='%s' and a.RegName=b.RegName"% (ip,reg)
    ret=db.executemany(sql_query_ports)
    flag=0
    _in_use=int(ret[0][3])
    _status=int(ret[0][2])
    if _in_use==3:
	flag=2
    else:
    	if _status==1:
		flag=1
	else:
		flag=0
    return HttpResponse(flag)

from .util import get_ostype_by_ip

@login_required
@permission_required('account.can_stop_node',raise_exception=True)
def node_stop(request):
    msg=""
    start_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user=request.user
    _ip=request.GET.get('ip')
    _reg=request.GET.get('reg')
    os_type=get_ostype_by_ip(_ip)[_ip]
    tgt=parse_saltstack_name(_ip)
    upduser=get_user_by_reg_and_ip(_ip,_reg)
    ret_dict={}
    salt_return=""
    rst=cmd_history(ip=_ip,regname=_reg,user=upduser,cmd='close_node',cmd_time=start_time)
    if tgt:
        client=LocalClient()
        command="su - %s -c 'sh ~/bin/close.sh'"%(upduser)
        try:
            jid=client.cmd_async(tgt,'cmd.run',[command])
        except:
            msg='salt is not running'
            return HttpResponse(msg)
        t=0
        while not client.get_cache_returns(jid):
            time.sleep(1)
            if  t==10:
                print "timeout"
                break
            else:
                t=t+1
        ret_dict=client.get_cache_returns(jid)
        salt_return=ret_dict[tgt]['ret']
        print salt_return
        if salt_return=="":
            msg="success"
        elif re.match(r"No such", salt_return):
            msg="no such file"
        else:
            msg="other error"
    elif os_type=='AIX':
        ssh=ssh_connection(_ip,upduser)
        command="sh ~/bin/open.sh'"
        try:
            stdin,stdout,stderr=ssh.exec_command(command,timeout=10)
            ret_str=stdout.readlines()
            if salt_return=="":
                msg="success"
            elif re.match(r"No such", salt_return):
                msg="no such file"
            else:
                msg="other error"
        except:
            msg='other error'
    else: 
        msg="No saltstack found in tgt %s"%_ip
    if msg=='success':
        update_node_status(_ip,_reg,1)
    else:
        pass
    return HttpResponse(msg)
@permission_required('account.can_start_node',raise_exception=True)
@login_required     
def node_start(request):
    msg=""
    start_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user=request.user
    _ip=request.GET.get('ip')
    _reg=request.GET.get('reg')
    os_type=get_ostype_by_ip(_ip)[_ip]
    tgt=parse_saltstack_name(_ip)
    upduser=get_user_by_reg_and_ip(_ip,_reg)
    ret_dict={}
    salt_return=""
    rst=cmd_history(ip=_ip,regname=_reg,user=user,cmd='close_node',cmd_time=start_time)
    if tgt:
        client=LocalClient()
        command="su - %s -c 'sh ~/bin/close.sh'"%(upduser)
        try:
            jid=client.cmd_async(tgt,'cmd.run',[command])
        except:
            msg='salt is not running'
            return HttpResponse(msg)
        t=0
        while not client.get_cache_returns(jid):
            time.sleep(1)
            if  t==10:
                print "timeout"
                break
            else:
                t=t+1
        ret_dict=client.get_cache_returns(jid)
        salt_return=ret_dict[tgt]['ret']
        print salt_return
        if salt_return=="":
            msg="success"
        elif re.match(r"No such", salt_return):
            msg="no such file"
        else:
            msg="other error"
    elif os_type=='AIX':
        ssh=ssh_connection(_ip,upduser)
        command="sh ~/bin/open.sh'"
        try:
            stdin,stdout,stderr=ssh.exec_command(command,timeout=10)
            ret_str=stdout.readlines()
            if salt_return=="":
                msg="success"
            elif re.match(r"No such", salt_return):
                msg="no such file"
            else:
                msg="other error"
        except:
            msg='other error'
    else: 
        msg="No saltstack found in tgt %s"%_ip
    if msg=='success':
        update_node_status(_ip,_reg,1)
    else:
        pass
    return HttpResponse(msg)

@permission_required("account.can_restart_node",)
@login_required
def get_server_detail(request):
    if request.GET:
        ip=request.GET.get('ip')
        reg=request.GET.get('reg')
        print ip,reg
        db=OracleDb()
        sql="select Description from machineinfo where ipaddress='%s' and regname='%s'" %(ip,reg)
        ret=db.execute(sql)
        if ret:
	           return_desc=ret[0]
        else:
	           return_desc="no desc matched"
    return render_to_response('monitor/server_detail.html',{'ip':ip,'reg':reg,'desc':unicode(return_desc,'gbk')})


@login_required
def get_server_open_status(request):
    htt=httplib2.Http(".cache",timeout=10)
    ip=request.GET.get("ip")
    port=request.GET.get("port")
    reg=request.GET.get('regname')
    content=''
    web_reg_status=0
    if reg=='WEB':
        url="http://{0}:{1}/emptywar/check_health_main.jsp".format(ip,port)
        try:
            resp,content=htt.request(url, "GET")
        except Exception,e:
            content='fail,other fail'
            
        if re.search(r'success',content):
            ret='s'
            web_reg_status=0
        else:
            ret='f'
            web_reg_status=1
    else:
        url="http://{0}:{1}/emptywar/check_health_main.jsp".format(ip,port)
        try:
            resp,content=htt.request(url, "GET")
        except Exception,e:
            print 'error'
        if re.search(r'success',content):
            ret='s'
            web_reg_status=1
        elif re.search(r'fail',content):
            ret='f'
            web_reg_status=1
        elif re.search(r'error',content):
        
            ret='f'
            web_reg_status=1
        else:
            ret='f'
            web_reg_status=1
    ret=ret+str(web_reg_status)
    return HttpResponse(ret)
from controller.util import parse_user
from controller.tasks import restart, aix_restart
from controller.action import Action
from controller.util import cmd_history
@permission_required('account.can_restart_node',raise_exception=True)
@login_required
def restart_reg(request):
    start_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip=request.GET.get('ip')
    regname=request.GET.get('reg')
    timestamp=request.GET.get('_')
    myDate=request.GET.get('mydate')
    user=parse_user(regname,ip)
    tgt=parse_saltstack_name(ip)
    os_type=get_ostype_by_ip(ip)[ip]
    dic={}
    cmd_history(ip=ip,regname=regname,user=user,cmd='restart_node',cmd_time=start_time)
    t=0
    if tgt:
        try:
            result=restart.delay(tgt,user,'','sh /tmp/h_restart.sh')
        except:
            return HttpResponse(json.dumps("celery error"), content_type='application/json')
    elif os_type=='AIX':
        try:
            result=aix_restart.delay(tgt,user,'','sh /tmp/h_restart.sh')
        except:
            return HttpResponse(json.dumps("celery error"), content_type='application/json')
    else:
	   return HttpResponse(json.dumps("no tgt found"), content_type='application/json')
    id=result.task_id
    return HttpResponse(json.dumps(id), content_type='application/json')

@login_required
def reg_restart_detail(request):
    timestamp=request.GET.get('timestamp')
    db=OracleDb()
    sql="select time,content from monitor.reg_restart_his where TM_SMP='%s'"%timestamp
    sql_ret=db.execute(sql)
    if len(sql_ret)>=1:
    	content=sql_ret[0][1]
    	time=sql_ret[0][0]
    	str='重启结束时间:',time,'<br>','任务返回结果:',content
    else:
			msg='None data matched.'   
    return HttpResponse(msg)
    
from celery.result import AsyncResult

@login_required
def restart_result(request):
    data={}
    if request.GET:
        id=request.GET.get('id')
    print "get r"
    r=AsyncResult(id)
    print r
    while not r.ready():
        data['context']='no'
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        task_result=r.result
        ret_result=""
        match_obj= re.search(r'boot succeed',task_result)
        if match_obj.group()=="boot succeed":
            if re.search(r'fail',task_result)==None:
                ret_result="success"
                
            else:    
                ret_result='fail'
        else:
            ret_result='fail'
        data['context']=ret_result
	return HttpResponse(json.dumps(),content_type='application/json')


def appStatus(request,regname=None,ipaddress=None,page=None):
    db=OracleDb()
    regname=request.GET.get('regname')
    
    if regname!=None:
        regname=regname.upper()
        sql_cmd="select regname,ipaddress,status,in_use,description from machineinfo where regname like '%s'"%(regname)
    else:
        sql_cmd="select regname,ipaddress,status,in_use,description from machineinfo"
    print sql_cmd
    result=db.executemany(sql_cmd)
    apps_shengchan=[]
    for re in result:
        dic={'regname':re[0],
             'ipaddress':re[1],
             'status':re[2],
             'in_use':re[3],
             'desc':unicode(re[4],'gbk')
             }
        apps_shengchan.append(dic)
  
    paginator=Paginator(apps_shengchan,20)
    try:
        page=int(request.GET.get('page',1))
    except ValueError:
        page=1
    try:
        app_shengchan=paginator.page(page)
    except:
        app_shengchan=paginator.page(1)
    context={
        'apps_shengchan':apps_shengchan,
        'app_shengchan':app_shengchan,
        }
    return render(request, 'controller/app_status_manage.html',locals())

def modify_app_status(request):
    db=OracleDb()
    if request.GET:
        ip=request.GET.get('ipaddress').strip()
        regname=request.GET.get('regname').strip()
        in_use=request.GET.get('in_use').strip()
        selected_in_use=request.GET.get('selected_in_use').strip()
        selected_in_use=selected_in_use[1]
        print int(selected_in_use)==int(in_use)
        if int(selected_in_use)==int(in_use):
            return HttpResponse(json.dumps('nochange'),content_type='application/json')
        else:
            sql="update machineinfo set in_use=%d where regname='%s' and ipaddress='%s'"%(int(selected_in_use),regname,ip)
            print sql
            try:
                db.execute_update(sql)
                return HttpResponse(json.dumps('success'),content_type='application/json')
            except:
                return HttpResponse(json.dumps('fail'),content_type='application/json')
    