# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields.related import ForeignKey

class user(models.Model):
    u_id = models.CharField(max_length=20, verbose_name=u'id')
    username = models.CharField(max_length=30, verbose_name=u'名词')
   
    user_priority = models.CharField(max_length=20, verbose_name=u'用户的等级')
    user_belong_to_asset = models.CharField(max_length=10,ForeignKey='' verbose_name=u'用户属于的资产')#用户属于哪个资产。哪个服务器

    remark = models.TextField(max_length=50, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return u'%s - %s - %s' %(self.ip, self.hostname, self.application )
   
    class Meta:
        verbose_name = u'主机列表'
        verbose_name = u'主机列表管理'

class platform(models.Model):
    p_id = models.IntegerField(verbose_name=u'平台id')
    p_name = models.CharField(max_length=30, verbose_name=u'平台名词')
    p_system = models.CharField(max_length=200, unique=False, verbose_name=u'平台所属业务系统')
    p_type = models.TimeField(auto_now=True, verbose_name=u'平台类型')
    p_desc=models.CharField(max_length=100,verbose_name=u'平台描述')

    def __unicode__(self):
        return u'%s - %s' %(self.id, self.user ,self.content)

    class Meta:
        verbose_name = u'用户输入历史记录'
        verbose_name_plural = u'输入历史记录管理'
        
class user_platform(models.Model):
    up_id=p_id = models.IntegerField(verbose_name=u'关联id')
    u_id = models.ForeignKey(user,related_name='u_id')
    u_id = models.ForeignKey(platform,related_name='p_id')
    