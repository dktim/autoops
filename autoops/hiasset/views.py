#coding:utf-8
import sys
#sys.setdefaultencoding('utf8')
aa=sys.getdefaultencoding()
reload(sys)
from django.shortcuts import render
from django.shortcuts import HttpResponse
from hiasset import models
from hiasset.models import ASSETINFO


# Create your views here.

def asset_manage(request,*args,**kw):
    import sys
#sys.setdefaultencoding('utf8')
    aa=sys.getdefaultencoding()
    sys.setdefaultencoding('utf8')
    try:
        _assetinfo = ASSETINFO.objects.all()
    except Exception as e:
        _error = "name already exists or too long!"
    _businesses = [
        "Linux",
        "Windows",
        "Unix",
    ]
    _success = kw.get("success", False)
    _error = kw.get("error", False)

    context = {
        "assetinfo": _assetinfo,
        "businesses": _businesses,
        "success": _success,
        "error": _error,
    }
    return render(request, "hiasset/asset_manage.html", context)

def add_asset(request):
    context = {}
    _success = False
    _error = False
    if request.method == "POST":
        _AST_NUM = request.POST.get("AST_NUM")
        _SR_NUM = request.POST.get("SR_NUM")
        _DEV_NAME = request.POST.get("DEV_NAME")
        _DEV_ALS = request.POST.get("DEV_ALS")
        _DEV_TYP = request.POST.get("DEV_TYP")
        _DEV_MOD = request.POST.get("DEV_MOD")
        _OS_TYP = request.POST.get("OS_TYP")
        _ADMIN = request.POST.get("ADMIN")
        _OWN_DPT = request.POST.get("OWN_DPT")
        _MAN_STE = request.POST.get("MAN_STE")
        _MAN_BGN = request.POST.get("MAN_BGN")
        _MAN_END = request.POST.get("MAN_END")
        _UP_TME = request.POST.get("UP_TME")
        _AST_LAB = request.POST.get("AST_LAB")
        _BUS_DES = request.POST.get("BUS_DES")
        _Location = request.POST.get("Location")
        _Area = request.POST.get("Area")
        _CAB_LCA = request.POST.get("CAB_LCA")
        _DEV_BGN = request.POST.get("DEV_BGN")
        _DEV_END = request.POST.get("DEV_END")
        _DEV_IP = request.POST.get("DEV_IP")
        _REMARK = request.POST.get("REMARK")
        try:
            print _AST_NUM,_SR_NUM,_DEV_NAME,_DEV_ALS,_DEV_TYP,_DEV_MOD,_OS_TYP,_ADMIN,_OWN_DPT,_MAN_STE,_MAN_BGN,_MAN_END,_UP_TME,_AST_LAB,_BUS_DES,_Location,_Area,_CAB_LCA,_DEV_BGN,_DEV_END,_DEV_IP,_REMARK
            _ASSETINFO = ASSETINFO(AST_NUM=_AST_NUM,SR_NUM=_SR_NUM,DEV_NAME=_DEV_NAME,DEV_ALS=_DEV_ALS,DEV_TYP=_DEV_TYP,DEV_MOD=_DEV_MOD,OS_TYP=_OS_TYP,ADMIN=_ADMIN,OWN_DPT=_OWN_DPT,MAN_STE=_MAN_STE,MAN_BGN=_MAN_BGN,MAN_END=_MAN_END,UP_TME=_UP_TME,AST_LAB=_AST_LAB,BUS_DES=_BUS_DES,Location=_Location,Area=_Area,CAB_LCA=_CAB_LCA,DEV_BGN=_DEV_BGN,DEV_END=_DEV_END,DEV_IP=_DEV_IP,REMARK=_REMARK)
            _ASSETINFO.save()
            _success = "Add Group " + _AST_NUM + " OK!!"
        except Exception as e:
            _error = "name already exists or too long!"
    else:
        pass
    return asset_manage(request, success=_success, error=_error)

def mod_asset(request):
    _success = False
    _error = False
    if request.method == "POST":
        _AST_NUM = request.POST.get("AST_NUM")
        _SR_NUM = request.POST.get("SR_NUM")
        _DEV_NAME = request.POST.get("DEV_NAME")
        _DEV_ALS = request.POST.get("DEV_ALS")
        _DEV_TYP = request.POST.get("DEV_TYP")
        _DEV_MOD = request.POST.get("DEV_MOD")
        _OS_TYP = request.POST.get("OS_TYP")
        _ADMIN = request.POST.get("ADMIN")
        _OWN_DPT = request.POST.get("OWN_DPT")
        _MAN_STE = request.POST.get("MAN_STE")
        _MAN_BGN = request.POST.get("MAN_BGN")
        _MAN_END = request.POST.get("MAN_END")
        _UP_TME = request.POST.get("UP_TME")
        _AST_LAB = request.POST.get("AST_LAB")
        _BUS_DES = request.POST.get("BUS_DES")
        _Location = request.POST.get("Location")
        _Area = request.POST.get("Area")
        _CAB_LCA = request.POST.get("CAB_LCA")
        _DEV_BGN = request.POST.get("DEV_BGN")
        _DEV_END = request.POST.get("DEV_END")
        _DEV_IP = request.POST.get("DEV_IP")
        _REMARK = request.POST.get("REMARK")
        try:
            _ASSETINFO = ASSETINFO.objects.get(AST_NUM=_AST_NUM)
            _name_before = _ASSETINFO.AST_NUM
            _ASSETINFO.SR_NUM = _SR_NUM
            _ASSETINFO.DEV_NAME = _DEV_NAME
            _ASSETINFO.DEV_ALS = _DEV_ALS
            _ASSETINFO.DEV_TYP = _DEV_TYP
            _ASSETINFO.DEV_MOD = _DEV_MOD
            _ASSETINFO.OS_TYP = _OS_TYP
            _ASSETINFO.ADMIN = _ADMIN
            _ASSETINFO.OWN_DPT = _OWN_DPT
            _ASSETINFO.MAN_STE = _MAN_STE
            _ASSETINFO.MAN_BGN = _MAN_BGN
            _ASSETINFO.MAN_END = _MAN_END
            _ASSETINFO.UP_TME = _UP_TME
            _ASSETINFO.AST_LAB = _AST_LAB
            _ASSETINFO.BUS_DES = _BUS_DES
            _ASSETINFO.Location = _Location
            _ASSETINFO.Area = _Area
            _ASSETINFO.CAB_LCA = _CAB_LCA
            _ASSETINFO.DEV_BGN = _DEV_BGN
            _ASSETINFO.DEV_END = _DEV_END
            _ASSETINFO.DEV_IP = _DEV_IP
            _ASSETINFO.REMARK = _REMARK
            _ASSETINFO.save()
            _success = "Modify Group " + _AST_NUM + " OK"
        except Exception as e:
            _error = "Modify Group " + _AST_NUM + " failed"

    return asset_manage(request, success=_success, error=_error)

def del_asset(request):
    context = {
    }
    _success = False
    _error = False
    _AST_NUMS = request.POST.getlist("AST_NUM")
    try:
        _filter = ASSETINFO.objects.filter(AST_NUM__in=_AST_NUMS)
        _filter.delete()
        _success = "Delete opearation success!"
    except Exception as e:
        _error = "Delete error!"
    # return render_to_response("groups/manage_group.html",context)
    # return HttpResponseRedirect("/groups/manage_group/",context)
    return asset_manage(request, success=_success, error=_error)
