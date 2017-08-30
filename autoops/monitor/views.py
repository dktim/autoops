#!coding=utf-8
from django.shortcuts import render, render_to_response,HttpResponseRedirect
from django.template.context import RequestContext
import time
import json
from django.core.paginator import Paginator
from autoops import settings
from django.template import RequestContext
from autoops import settings
from salt.client import LocalClient
import os
from django.http.response import HttpResponse
from autoops.oracle import OracleDb
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from _elementtree import parse
import logging
log=logging.getLogger("django")


def longToInt(value):
    if value > 2147483647 :
        return (value & (2 ** 31 - 1))
    else :
        return value
       

def login(request):
	return render_to_response("common_service/login.html",locals())
from account.models import *
@login_required
def production_index(request):
    log.error('production_index')
    log.info('info----------------')
    log.debug('debug----------------')
    log.error('error----------------')
    
    _user=request.user
    print _user
    userprofile = UserProfiles.objects.get(user=_user)
    _b = userprofile.business.all()
    print _b
    db=OracleDb()
    sql="""
select a.regname,b.wide as wide,b.high as high,sum(a.status) as bad,count(a.status) as xx \
from machineinfo a,appregioninfo b where a.regname=b.regname and  a.in_use=1   group by \
a.regname,b.wide,b.high
""" 
    ret=db.executemany(sql)
    ret_list=[]
    for item in ret:
            reg=item[0]
            wide=item[1]
            high=item[2]
            bad=int(item[3])
            good=int(item[4]-item[3])
            sum=int(item[4])
            dic={
					'reg':reg,
					'wide':wide,
					'high':high,
					'bad':bad,
					'good':good,
					'sum':sum
					}
            ret_list.append(dic)
    print len(ret_list)
    return HttpResponse(json.dumps(ret_list),content_type="application/json")


@login_required
def yutouchan_index(request):
    db=OracleDb()
    sql="""
select a.regname,b.wide as wide,b.high as high,sum(a.status) as bad,count(a.status) as xx from machineinfo a,appregioninfo b where a.regname=b.regname and a.in_use=2 group by a.regname,b.wide,b.high

"""
    ret=db.executemany(sql)
    ret_list=[]
    for item in ret:
        dic={
                                        'reg':item[0],
                                        'wide':item[1],
                                        'high':item[2],
                                        'bad':int(item[3]),
                                        'good':int(item[4]-item[3]),
                                        'sum':int(item[4])
            }
        ret_list.append(dic)
    print len(ret_list)
    return HttpResponse(json.dumps(ret_list),content_type="application/json")



@login_required
def wls_monitor(request):
	_client=LocalClient()
	jid=_client.cmd_async('*','wls_monitor.wls_moni')
	time.sleep(5)
	lst=[]
	ret=_client.get_cache_returns(jid)
	for key in ret.keys():
		dic={}
		aa=key.split('_')
		if isinstance(ret[key]['ret'],str):
			value=ret[key]['ret']
		else:
			value=int(ret[key]['ret'][0])
		dic['ip']=aa[0]
		dic['logstash']=value
		lst.append(dic)
	paginator = Paginator(lst,20)
	try:
        	page = int(request.GET.get('page','1'))
    	except ValueError:
        	page = 1
	
    	try:
        	server_list = paginator.page(page)
    	except :
        	server_list = paginator.page(1)
	return render_to_response('monitor/wls_monitor.html',locals())

@login_required
def logstash_monitor(request):
    start=time.time()
    _client=LocalClient()
    jid=_client.cmd_async('*','logstash_monitor.logstash_monitor')
    time.sleep(5)
    ret=_client.get_cache_returns(jid)
    lst=[]
    for key in ret.keys():
        dic={}
        aa=key.split('_')
        if isinstance(ret[key]['ret'],list):
            value=int(ret[key]['ret'][0])
        else:
            value=ret[key]['ret']
        dic['ip']=aa[0]
        dic['logstash']=value
        lst.append(dic)
    paginator = Paginator(lst,50)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        server_list = paginator.page(page)
    except :
        server_list = paginator.page(1)
    end=time.time()
    print end-start
    return render_to_response('monitor/logstash_monitor.html',locals())

import time
@login_required
def query_all_server_port_status(request):
	client=LocalClient()
	jid=client.cmd_async('*','thread_check.port_check')
	time.sleep(20)
	ret=client.get_cache_returns(jid)
	lst=[]
	sql_list=[]
	for key,value in ret.items():
		dic={}
		dic['ip']=key.split("_")[0]
		ff=value['ret']
		ora_ret=[]
		for item in ff:
			ora_ret.append(item)
		dic['content']=ora_ret
		lst.append(dic)
	for item in lst:
		list=[]
		ip=item['ip']
		for i in item['content']:
			list=[]
			list.append(ip)
			xx_list=i.split("|")
			for j in xx_list:
				list.append(j)
			sql_list.append(list)
	db=OracleDb()
	rk_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	f_list=[]	
	for item in sql_list:
		try:
			print item[0]
		except:
			item.insert(0,'')
		try:
			print item[1]
		except:
			item.insert(1,'')
		try:
			print item[2]
		except: 
                        item.insert(2,'')
		try:
			print item[3]
		except: 
                        item.insert(3,'')
		try:
			print item[4]
		except: 
                        item.insert(4,'')
		sql="insert into securi_port(ip,port,status,p_user,p_name,p_path,rk_date) values('%s','%s','%d','%s','%s','%s','%s')"%(item[0],item[1],0,item[2],item[3],item[4],rk_time)
		db.execute_update(sql)
	clean_command="delete from SECURI_PORT where p_path is null "
	db.execute_update(sql)
	return render_to_response("monitor/port_monitor.html",{'ret':sql_list})

@login_required
def get_hub_ajax_state(request):
    if request.GET:
        _start_time=request.GET.get('start')
        _reg=request.GET.get('reg')
        _ip=request.GET.get('ip')
        _end_time=request.GET.get('stop')
        ip_list=[_ip]
        dic={}
        time_list1=get_time_with_ajax(ip_list,_start_time,_end_time,'hub',_reg)
        highchart_data_list=get_hub_ajax_count(ip_list,_start_time,_end_time,_reg)
        dic['count']=highchart_data_list
        dic['time']=time_list1
    return HttpResponse(json.dumps(dic))


@login_required
def thread_monitor(request):
	ret_list=[]
	db=OracleDb()
	sql="select distinct regname from machineinfo"
	reg_ret=db.executemany(sql)
	for item in reg_ret:
		dic={}
		dic['reg']=item[0]
		sql_1="select IPADDRESS from machineinfo where regname='%s'"%item[0]
		ip_ret=db.executemany(sql_1)
		ip_list=[]
		for item in ip_ret:
			ip_list.append(item[0])
		dic['ip']=ip_list
		ret_list.append(dic)
	return render_to_response('monitor/thread_monitor.html',{'list':ret_list})

@login_required
def index(request,id):
    user=request.user
    print user
    ret_list=[]
    if int(id)==1:
    	return render_to_response('index.html',{'reg_list':ret_list,'user':user})
    else:
		return render_to_response('index_1.html',{'reg_list':ret_list,'user':user})

from django.views.decorators.csrf import csrf_exempt , csrf_protect

import datetime
@csrf_exempt
@login_required
def jdbc_status2(request):
    db=OracleDb()
    if request.GET:
        reg=request.GET.get('reg')
        sql="select distinct b.IpAddress from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName"%reg
        ret=db.execute(sql)
    return render_to_response( 'monitor/jdbc_status.html',{'regname':reg,'ret':ret}) 

@login_required
def jdbc_status3(request):
    count=[]
    content=[]
    start_time='2016-07-27 09:58:41'
    end_time='2016-07-27 09:59:41'
    ip_list=get_ip_list(start_time, end_time)
    dic=get_count_with_ip(ip_list,start_time,end_time)
    count,content,ip_list1,time_list=parse_ip_count(dic)
    data=[1,2,2,4,5]
    list=[]
    cn_json={'title': {'text': '',},
             'xAxis': {'categories': time_list,'tickInterval': 1 },
             'yAxis': {'title': {'text': 'Missing SLA Silo number'},
                       'min':0,
                       'max':60,
                       'plotLines': [{'value': 0,'width': 1,'color': '#808080',}]},
             'legend': {'layout': 'vertical','align': 'right','verticalAlign': 'middle','borderWidth': 0},
             'series': {'name':'cc','data':[1,2,3,4,5]}
                         }
    cn_json = json.dumps(cn_json)
    return HttpResponse(cn_json,content_type='application/json')
   

@login_required 
def get_jms_state_by_hour(request):
    start=time.time()
    reg=request.GET.get('reg')
    list=[]
    time_list=[]
    db=OracleDb()
    request_time=request.GET.get('time')
    default_pool_sql="select distinct defaultjmsqueue from appregioninfo where regname='%s'"%reg
    default_pool=db.execute(default_pool_sql)
    if not request_time:
		end_time=datetime.datetime.now()
		tag_str=str(end_time.time()).split(':')[0]
		tag=int(tag_str)
  		start_time = end_time+datetime.timedelta(hours=-tag)
  		start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
  		end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
  		for i in range(tag):
  			time_list.append('{0}:00:01'.format(i))
    else:
  		start_time=request_time+'00:00:01'
  		end_time=request_time+'23:59:59' 
  		for i in range(23):
  			time_list.append("{0}:00:01".format(i))
  	
    ip_list=get_ip_list(reg,start_time, end_time)
    for ip in ip_list:
  		sql="""
  select host,

       regname,

       NAME,

       trunc(tm_smp, 'hh24'),

       max(MESSAGESCURRENTCOUNT) max

  from monitor_jms
 where host = '{0}'

   and regname = '{1}'

   and NAME = '{2}'

   and tm_smp between to_date('{3}', 'yyyy-mm-dd hh24:mi:ss') and

       to_date('{4}', 'yyyy-mm-dd hh24:mi:ss')

 group by host, regname, name, trunc(tm_smp, 'hh24')

 order by 1, 2, 3, 4
  """.format(ip,reg,default_pool[0],start_time,end_time,ip)
		ret=db.executemany(sql)
		dic={}
		ret_list=[]
		for item in ret:
			ret_list.append(item[4])
		dic['name']=ip
		dic['data']=ret_list
		list.append(dic)
    var={'name','data'}
    dic_totle={}
    dic_totle['count']=list
    dic_totle['time']=time_list
    end=time.time()
    print "jms_hourly:",end-start
    return HttpResponse(json.dumps(dic_totle))
 
 
@login_required  
def get_jdbc_state_by_hour(request):
    start=time.time()
    reg=request.GET.get('reg')
    list=[]
    time_list=[]
    db=OracleDb()
    request_time=request.GET.get('time')
    if not request_time:
		end_time=datetime.datetime.now()
		tag_str=str(end_time.time()).split(':')[0]
		tag=int(tag_str)
  		start_time = end_time+datetime.timedelta(hours=-tag)
  		start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
  		end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
  		for i in range(tag):
  			time_list.append('{0}:00:01'.format(i))
    else:
  		start_time=request_time+'00:00:01'
  		end_time=request_time+'23:59:59' 
  		for i in range(23):
  			time_list.append("{0}:00:01".format(i))
  	
    ip_list=get_ip_list(reg,start_time, end_time)
    for ip in ip_list:
  		sql="""
  		select host, 
      		 regname,
       		jdbcpoolname,
       trunc(tm_smp, 'hh24'),
       
       max(activecurrent) max

  from monitor_jdbc

 where 
      
regname = '{0}'
and host='{3}'
      
   and jdbcpoolname = 'mprac_ds_01'
      
   and tm_smp between to_date('{1}', 'yyyy-mm-dd hh24:mi:ss') and
      
       to_date('{2}', 'yyyy-mm-dd hh24:mi:ss')

 group by host, regname, jdbcpoolname, trunc(tm_smp, 'hh24')

 order by 1, 2, 3, 4
  """.format(reg,start_time,end_time,ip)
		ret=db.executemany(sql)
		dic={}
		ret_list=[]
		for item in ret:
			ret_list.append(item[4])
		dic['name']=ip
		dic['data']=ret_list
		list.append(dic)
    var={'name','data'}
    dic_totle={}
    dic_totle['count']=list
    dic_totle['time']=time_list
    end=time.time()
    print 'jdbc_hourly:',end-start
    return HttpResponse(json.dumps(dic_totle))



@login_required
def get_hub_state_by_hour(request):
    start=time.time()
    reg=request.GET.get('reg')
    list=[]
    time_list=[]
    db=OracleDb()
    request_time=request.GET.get('time')
    if not request_time:
		end_time=datetime.datetime.now()
		tag_str=str(end_time.time()).split(':')[0]
		tag=int(tag_str)
  		start_time = end_time+datetime.timedelta(hours=-tag)
  		start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
  		end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
  		for i in range(tag):
  			time_list.append('{0}:00:01'.format(i))
    else:
  		start_time=request_time+'00:00:01'
  		end_time=request_time+'23:59:59' 
  		for i in range(23):
  			time_list.append("{0}:00:01".format(i))
  	
    ip_list=get_ip_list(reg,start_time, end_time)
    for ip in ip_list:
  		sql="""
select host,

       regname,

       trunc(tm_smp, 'hh24'),

       max(curractivethreadcount) max

  from hubstat
 where host = '{0}'

   and regname = '{1}'

   and tm_smp between to_date('{2}', 'yyyy-mm-dd hh24:mi:ss') and

       to_date('{3}', 'yyyy-mm-dd hh24:mi:ss')

 group by host, regname, trunc(tm_smp, 'hh24')

 order by 1, 2, 3
  """.format(ip,reg,start_time,end_time)
		ret=db.execute(sql)
		dic={}
		ret_list=[]
		for item in ret:
			ret_list.append(item[3])
		dic['name']=ip
		dic['data']=ret_list
		list.append(dic)
    var={'name','data'}
    dic_totle={}
    dic_totle['count']=list
    dic_totle['time']=time_list
    end=time.time()
    print 'hub_hourly:',end-start
    return HttpResponse(json.dumps(dic_totle))



@login_required	
def get_lsn_state_by_hour(request):
    start=time.time()
    reg=request.GET.get('reg')
    list=[]
    time_list=[]
    db=OracleDb()
    request_time=request.GET.get('time')
    if not request_time:
		end_time=datetime.datetime.now()
		tag_str=str(end_time.time()).split(':')[0]
		tag=int(tag_str)
  		start_time = end_time+datetime.timedelta(hours=-tag)
  		start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
  		end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
  		for i in range(tag):
  			time_list.append('{0}:00:01'.format(i))
    else:
  		start_time=request_time+'00:00:01'
  		end_time=request_time+'23:59:59' 
  		for i in range(23):
  			time_list.append("{0}:00:01".format(i))
  	
    ip_list=get_ip_list(reg,start_time, end_time)
    for ip in ip_list:
  		sql="""
  		select host,

       regname,

       trunc(tm_smp, 'hh24'),

       max(curractivethreadcount) max

  from lsnstat
 where host = '{0}'

   and regname = '{1}'

   and tm_smp between to_date('{2}', 'yyyy-mm-dd hh24:mi:ss') and

       to_date('{3}', 'yyyy-mm-dd hh24:mi:ss')

 group by host, regname, trunc(tm_smp, 'hh24')

 order by 1, 2, 3
  """.format(ip,reg,start_time,end_time)
		ret=db.execute(sql)
		dic={}
		ret_list=[]
		for item in ret:
			ret_list.append(item[3])
		dic['name']=ip
		dic['data']=ret_list
		list.append(dic)
    var={'name','data'}
    dic_totle={}
    dic_totle['count']=list
    dic_totle['time']=time_list
    end=time.time()
    print end-start
    return HttpResponse(json.dumps(dic_totle))


from controller.util import dictfetchall

@login_required
def server_list(request,ip=None):
    _type=request.GET.get('type')
    sql=""
    print _type
    print _type=='production'
    regName=request.GET.get('reg')
    print regName
    db=OracleDb()
    if _type=='production':
    	sql="select b.IpAddress,b.description,b.regname from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName and b.in_use in(1,3,0)" % (regName)
    	print sql
    elif _type=='yutouchan':
	sql="select b.IpAddress,b.description ,b.regname from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName and b.in_use=2" % (regName)
	print sql
    ret=db.executemany(sql)
    ip_list=[]
    for item in ret:
        dic={}
        dic['regname']=item[2]
        dic['ip']=item[0].strip()
        dic['desc']=unicode(item[1],'gbk').strip()
        ip_list.append(dic)
    print ip_list
    return render_to_response('monitor/server_list.html',{'list':ip_list,'regname':regName})



@login_required
def get_reg_info(request):
    db=OracleDb()
    ip=request.GET.get('ip')
    reg=request.GET.get('reg')
    sql="select a.regname,a.ipaddress,b.appuser,b.upduser,a.status,b.httpport,a.description from machineinfo a,appregioninfo b where a.ipaddress='%s' and b.regname='%s' and a.regname=b.regname"%(ip,reg)
    re=db.executemany(sql)
    list=[]
    for item in re:
        dic={}
        dic['regname']=item[0]
        dic['IpAddress']=item[1]
        dic['AppUser']=item[2]
        dic['UpdUser']=item[3]
        dic['status']=item[4]
        dic['HttpPort']=item[5]
	dic['desc']=unicode(item[6],'gbk')
        list.append(dic)
    return render_to_response('monitor/server_list_detail.html',{'list':list})

from django.http import JsonResponse
from monitor.jms_util import get_jms_ip_list
from monitor.util import get_count_with_ip


@login_required
def get_jms_state(request):
    _reg=request.GET.get('reg')
    db=OracleDb()
    sql="select distinct b.IpAddress from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName"%_reg
    ret=db.execute(sql)
    return render_to_response("monitor/jms_status.html",{'regname':_reg,'ret':ret})



@login_required
def single_machine(request):
    ip=request.GET.get('ip')	
    return render_to_response('monitor/11.html',{'ip':ip})
from monitor.jms_util import get_jms_ajax_count

@login_required
def get_jms_state_ajax(request):
    start_time=request.GET.get('start')
    end_time=request.GET.get('stop')
    if end_time=="":
        end_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if start_time=='':
        start_time=datetime.datetime.now()+datetime.timedelta(days=-1)
        start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    reg=request.GET.get('reg')
    type=request.GET.get('type')
    ip=request.GET.get('ip')
    ip_list=[]
    ip_list.append(ip)
    dic={}
    time_list=get_time_with_ajax(ip_list,start_time,end_time,type,reg)
    highchart_data_list=get_jms_ajax_count(ip_list,start_time,end_time,reg)
    dic['count']=highchart_data_list
    dic['time']=time_list
    return HttpResponse(json.dumps(dic))


@login_required
def get_listener_state(request):
    reg=request.GET.get('reg')
    
    return render_to_response('monitor/listener_state.html',{'regname':reg})

@login_required
def lsn_status(request):
    end_time=datetime.datetime.now()
    start_time=end_time+datetime.timedelta(hours=-1)
    start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
    reg=request.GET.get('reg')
    db=OracleDb()
    sql="select b.IpAddress from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName"%reg
    ret=db.execute(sql)
    return render_to_response("monitor/lsn_status.html",{"regname":reg,'ret':ret})

from monitor.lsn_util import get_lsn_ip_list,get_lsn_ajax_count
from monitor.hub_util import get_hub_ip_list,get_hub_ajax_count


@login_required
def start_page_with_hub_state(request):
    start=time.time()
    reg=request.GET.get('reg')
    end_time=datetime.datetime.now()
    start_time =end_time+datetime.timedelta(hours=-0.5)
    start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
    ip_list=get_hub_ip_list(start_time,end_time,reg)
    dic={}
    time_list1=get_time_with_ajax(ip_list,start_time,end_time,'hub',reg)
    highchart_data_list=get_hub_ajax_count(ip_list,start_time,end_time,reg)
    dic['count']=highchart_data_list
    dic['time']=time_list1
    end=time.time()
    print 'get_hub_status:',end-start
    return HttpResponse(json.dumps(dic))

from monitor.util import *

@login_required
def start_page_with_jms_state(request):
    start=time.time()
    reg=request.GET.get('reg')
    end_time=datetime.datetime.now()
    start_time = end_time+datetime.timedelta(hours=-0.5)
    start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
    ip_list=get_jms_ip_list(start_time,end_time,reg)
    dic={}
    jms_time_list=get_time_with_ajax(ip_list,start_time,end_time,'jms',reg)
    highchart_data=get_jms_ajax_count(ip_list,start_time,end_time,reg)
    dic['count']=highchart_data
    dic['time']=jms_time_list
    end=time.time()
    print end-start
    return HttpResponse(json.dumps(dic))


@login_required
def start_page_with_lsn_state(request):
    start=time.time()
    reg=request.GET.get('reg')
    end_time=datetime.datetime.now()
    start_time=end_time+datetime.timedelta(hours=-0.5)
    start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
    ip_list=get_lsn_ip_list(start_time,end_time,reg)
    dic={}
    time_list=get_time_with_ajax(ip_list,start_time,end_time,'lsn',reg)
    highchart_data_list=get_lsn_ajax_count(ip_list, start_time, end_time,reg)
    dic['count']=highchart_data_list
    dic['time']=time_list
    end=time.time()
    print end-start
    return HttpResponse(json.dumps(dic))



@login_required
def get_lsn_ajax_state(request):
    start_time=request.GET.get('start')
    reg=request.GET.get('reg')
    ip=request.GET.get('ip')
    end_time=request.GET.get('stop')
    ip_list=[ip]
    dic={}
    time_list1=get_time_with_ajax(ip_list,start_time,end_time,'lsn',reg)
    highchart_data_list=get_lsn_ajax_count(ip_list,start_time,end_time,reg)
    dic['count']=highchart_data_list
    dic['time']=time_list1
    return HttpResponse(json.dumps(dic))


@login_required
def get_hub_state(request):
    reg=request.GET.get('reg') 
    db=OracleDb()
    sql="select distinct b.IpAddress from appregioninfo a,machineinfo b where a.RegName='%s' and a.RegName=b.RegName"%reg
    ret=db.execute(sql)
    
    end_time=datetime.datetime.now()
    start_time=datetime.datetime.now()+datetime.timedelta(hours=-1)
    end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
    start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    return render_to_response('monitor/hub_status.html',{'regname':reg,'ret':ret})



@login_required
def get_jdbc_state(request):
    start_time=request.GET.get('start')
    end_time=request.GET.get('stop')
    if end_time=="":
        end_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if start_time=='':
        start_time=datetime.datetime.now()+datetime.timedelta(days=-1)
        start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
  

    ip=request.GET.get('ip')
    reg=request.GET.get('reg')
    type=request.GET.get('type')
    dic={}
    ip_list=[]
    ip_list.append(ip)
    ip_count_dic=get_count_with_ip(ip_list,start_time,end_time,reg)
    time_list1=get_time_with_ajax(ip_list,start_time,end_time,type,reg)
    dic['count']=ip_count_dic
    dic['time']=time_list1
    return HttpResponse(json.dumps(dic))


@login_required
def get_jdbc_state_at_start(request):
    ip=request.GET.get("ip")
    end_time=datetime.datetime.now()
    start_time = end_time+datetime.timedelta(hours=-0.5)
    start_time=start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time=end_time.strftime("%Y-%m-%d %H:%M:%S")
    reg=request.GET.get('reg')
    dic={}
    ip_list=get_ip_list(reg,start_time, end_time)
    ip_count_dic=get_count_with_ip(ip_list,start_time,end_time,reg)
    time_list1=get_time_with_ajax(ip_list,start_time,end_time,'jdbc',reg)
    dic['count']=ip_count_dic
    dic['time']=time_list1
    return HttpResponse(json.dumps(dic))



@login_required
def single_machine_jdbc_state(request):
	ip=request.GET.get('ip')
	reg=request.GET.get('reg')
	end=datetime.datetime.now()
	start=end+datetime.timedelta(hours=-1)
	end=end.strftime("%Y-%m-%d %H:%M:%S")
	start=start.strftime("%Y-%m-%d %H:%M:%S")
	sql="select TM_SMP,ACTIVECURRENT from monitor.monitor_jdbc where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s' and REGNAME='%s' and jdbcpoolname in(select defaultjdbcpool from appregioninfo where regname='%s')" %(start,end,ip,reg,reg)
	print sql
	db=OracleDb()
	ret=db.executemany(sql)
	#print ret
	dic={}
	dic1={}
	count=[]
	time=[]
	for item in ret:
		count.append(item[1])
		time.append(item[0].strftime("%Y-%m-%d %H:%M:%S"))
	name=['name','data']
	s=[ip,count]
	dic1=dict(zip(name,s))
	#dic1['name']="jdbc"
	dic['time']=time
	dic['count']=[dic1]
	return HttpResponse(json.dumps(dic))	



@login_required
def single_machine_lsn_state(request):
        ip=request.GET.get('ip')
        end=datetime.datetime.now()
        start=end+datetime.timedelta(hours=-0.05)
        end=end.strftime("%Y-%m-%d %H:%M:%S")
        start=start.strftime("%Y-%m-%d %H:%M:%S")
        sql="select TM_SMP,CURRACTIVETHREADCOUNT from monitor.LSNSTAT where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s'" %(start,end,ip)
        db=OracleDb()
        ret=db.executemany(sql)
        dic={}
        dic1={}
        count=[]
        time=[]
        for item in ret:
                count.append(item[1])
                time.append(item[0].strftime("%Y-%m-%d %H:%M:%S"))
        #dic1['data']=count
        name=['name','data']
        s=[ip,count]
        dic1=dict(zip(name,s))
        #dic1['name']="jdbc"
        dic['time']=time
        dic['count']=[dic1]
        return HttpResponse(json.dumps(dic))




@login_required
def single_machine_hub_state(request):
        ip=request.GET.get('ip')
        end=datetime.datetime.now()
        start=end+datetime.timedelta(hours=-0.05)
        end=end.strftime("%Y-%m-%d %H:%M:%S")
        start=start.strftime("%Y-%m-%d %H:%M:%S")
        sql="select TM_SMP,CURRACTIVETHREADCOUNT from monitor.HUBSTAT where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s'" %(start,end,ip)
        db=OracleDb()
        ret=db.oexecutemany(sql)
        dic={}
        dic1={}
        count=[]
        time=[]
        for item in ret:
                count.append(item[1])
                time.append(item[0].strftime("%Y-%m-%d %H:%M:%S"))
        #dic1['data']=count
        name=['name','data']
        s=[ip,count]
        dic1=dict(zip(name,s))
        #dic1['name']="jdbc"
        dic['time']=time
        dic['count']=[dic1]
        return HttpResponse(json.dumps(dic))







@login_required
def single_machine_jms_state(request):
        ip=request.GET.get('ip')
        reg=request.GET.get('reg')
        end=datetime.datetime.now()
        start=end+datetime.timedelta(hours=-1)
        end=end.strftime("%Y-%m-%d %H:%M:%S")
        start=start.strftime("%Y-%m-%d %H:%M:%S")
        sql="select TM_SMP,MESSAGESCURRENTCOUNT from monitor.monitor_jms where TM_SMP between to_date('%s','yyyy-mm-dd hh24:mi:ss') and to_date('%s','yyyy-mm-dd hh24:mi:ss') and HOST='%s' and regname='%s' and name in(select defaultjmsqueue from appregioninfo where regname='%s')" %(start,end,ip,reg,reg)
        print sql
        db=OracleDb()
        ret=db.executemany(sql)
        #print ret
        dic={}
        dic1={}
        count=[]
        time=[]
        for item in ret:
                count.append(item[1])
                time.append(item[0].strftime("%Y-%m-%d %H:%M:%S"))
        #dic1['data']=count
        name=['name','data']
        s=[ip,count]
        dic1=dict(zip(name,s))
        #dic1['name']="jdbc"
        dic['time']=time
        dic['count']=[dic1]
        print dic
        return HttpResponse(json.dumps(dic))


@login_required
def host_restart(request):
	db=OracleDb()
    	ip=request.GET.get('ip')
	reg=request.GET.get('regname')
   	sql="select a.regname,a.ipaddress,b.appuser,b.upduser,a.status,b.httpport,a.description from machineinfo a,appregioninfo b where a.ipaddress='%s' and b.regname='%s' and a.regname=b.regname"%(ip,reg)
    	print sql
    	sql="select a.regname,a.ipaddress,b.appuser,b.upduser,a.status,b.httpport,a.description from machineinfo a,appregioninfo b where a.ipaddress='172.16.6.44' and b.regname='PAY' and a.regname=b.regname"
    	re=db.executemany(sql)
    	print re
    	list=[]
	for item in re:
		d1={'regname':item[0],
			'IpAddress':item[1],
			'AppUser':item[2],
			'UpdUser':item[3],
			'status':item[4],
			'HttpPort':item[5],
			'desc':unicode(item[6],'gbk')
			}
		list.append(d1)	
	return render(request,"monitor/aa1.html",{'list':list})


@login_required
def get_reg_action_history(request):
    ip=request.GET.get('ip')
    regname=request.GET.get('reg')
    sql="select username,regname,cmd,cmd_time from cmd_history where regname='%s' and ipaddress='%s' and rownum<10"%(regname,ip)
    db=OracleDb()
    parse_result=db.executemany(sql)
    cmd_history_list=[]
    for re in parse_result:
        dic={
            'username':re[0],
            'regname':re[1],
            'cmd':re[2],
            'cmd_time':re[3]
            }
        cmd_history_list.append(dic)
	return HttpResponse(json.dumps(cmd_history_list),content_type="application/json")
