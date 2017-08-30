# -*- coding:utf-8 -*-
#!/bin/env python
import logging
import json
from django.shortcuts import render
from autoops.settings import oracle_conn
from execute.salttask import parse_saltstack_name
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from autoops import settings
from salt.client import  LocalClient
from logging import Logger
from account.models import Businesses,Privileges,UserProfiles
from .utility import handle_uploaded_file,walk_dir,delete_file
import os
from autoops.oracle import OracleDb
base_dir = settings.FILE_BASE_DIR
log=logging.getLogger("django")

# Create your views here.
@login_required(login_url="/account/login/")
def manage_file(request,*args,**kw):
    _u = request.user
    _user = User.objects.get(username=_u)

    _businesses = []
    _db=OracleDb()
    all = {}
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    _results = kw.get("results",False)
    sql="select distinct regname from machineinfo"
    ret=_db.executemany(sql)
    regs=[]
    for item in ret:
        regs.append(item[0])
    #all={'g1':['172.16.49.170','172.16.49.172','172.16.49.171'],'wch1':{'172.29.43.11-wch1','172.29.43.12-wch1','172.29.43.13-wch1','172.29.43.14-wch1','172.29.43.15','172.29.43.16','172.29.43.17','172.29.43.18'}}
    regs=['PAY','IPW','IPS','URMBAT','PES','WAP1','WAP1','WEB','WCH','WCH1']
    context={
        "error" : _error,
        "success" : _success,
        "results" : _results,
        "base_dir" : base_dir,
        #'list_groups':all,
        'regs':regs
        }
    log.info('info----------------')
    log.debug('debug----------------')
    log.error('error----------------')
    return render(request,'file_manage/manage_file.html',context)
base_dir = settings.FILE_BASE_DIR
from salt.client import LocalClient

@permission_required('can_restart_node')
@login_required
def upload_file(request):
    reg=[]
    files=[]
    uploaduser=[]
    ips=[]
    if request.method == "POST":
        _results = []
        files = request.FILES.getlist("myfile")
        reg=request.POST.getlist('regname')
        uploaduser=request.POST.getlist('uploaduser')
        ips=request.POST.getlist('ip')
    print reg,ips,files,uploaduser
    xx=[]
    for ip in ips:
        for file in files:
            dic={'ip':ip,
                'file':file,
		'filename':file.name,
                'reg':reg[0],
                'uploaduser':uploaduser[0]
                    }
            xx.append(dic)
    _result=[]
    for file in files:
            dest = base_dir+'/'+file.name
            logging.log()
            _r = handle_uploaded_file(f=file,dir=dest,file=file.name)
            _results.append("Upload Status "+str(_r) + ' : ' + dest)
    client=LocalClient()
    jids=[]
    for item in xx:
        tgt=parse_saltstack_name(item['ip'])
        src="salt://backup/{0}".format(item['filename'])
        dst="/tmp/{0}".format(item['filename'])
        arg="makedirs=True"
        try:
            jid=client.cmd_async(tgt, 'cp.get_file', [src,dst,arg])
        except:
            jid='error'
        jids.append(jid)
    total=len(jids)
    fail=0
    success=0  #return HttpResponse('The salt master could not be contacted. Is master running?')
    for item in jids:
        if item=='error':
            print item
            fail+=1
    success=total-fail
    return HttpResponse('success:'+str(success)+'fail:'+str(fail))


@login_required
def del_file(request):
    if request.method=='POST':
		_result=[]
		_paths=request.POST.getlist('path')
		for _path in _paths:
			_r=delete_file(path=_path)
			_result.append("delete file ok")
		return manage_file(request,result=_result)


@login_required
def get_host_by_reg(request):
    reg=request.GET.get('reg')
    print reg
    sql="select ipaddress from machineinfo where regname='%s'"%reg
    print sql
    _db=OracleDb()
    ret=_db.executemany(sql)
    hosts=[]
    for item in ret:
        hosts.append(item[0])
    print hosts
    return HttpResponse(json.dumps(hosts), content_type='application/json')
