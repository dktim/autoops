#coding:utf-8
from django.shortcuts import render

# Create your views here.





def cron_deploy(request):
	context={

	"success":True,
	'msg':u"期待更新中。。。"
		}
	return render(request,'deploy/cron_deploy.html',context)


def regular_deploy(request):
        context={

        "success":True,
	'msg':u"期待更新中...",

                }
        return render(request,'deploy/regular_deploy.html',context)
