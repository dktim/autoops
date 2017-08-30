#coding:utf-8
from account.models import *


privi=['restart_node','stop_node','start_node','view_monitor_status']

def can_restart_node(request,*args,**kwargs):
    _user=request.user
    
    return __name__
    userprofile = UserProfiles.objects.get(user=_user)
    _b = userprofile.business.all()
    print _b
    p=0
    for business in _b:
        if business.name=='node_stop':
            p=1
            break
        else:
            p=0
    if p==1:
        return True
    else:
        return False
