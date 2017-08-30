from __future__ import unicode_literals
from django.db import models

# Create your models here.

class ASSETINFO(models.Model):
    AST_NUM = models.CharField(max_length=20, primary_key=True)
    SR_NUM = models.CharField(max_length=20,unique=True)
    DEV_NAME = models.CharField(max_length=20,null=False)
    DEV_ALS = models.CharField(max_length=20, null=False)
    DEV_TYP = models.CharField(max_length=20, null=False)
    DEV_MOD = models.CharField(max_length=20, null=False)
    OS_TYP = models.CharField(max_length=20, null=True)
    ADMIN = models.CharField(max_length=20, null=False)
    OWN_DPT = models.CharField(max_length=20, null=False)
    MAN_STE = models.CharField(max_length=20, null=False)
    MAN_BGN = models.CharField(max_length=20, null=False)
    MAN_END = models.CharField(max_length=20, null=False)
    UP_TME = models.CharField(max_length=20, null=True)
    AST_LAB = models.CharField(max_length=20,unique=True)
    BUS_DES = models.CharField(max_length=20, null=True)
    Location = models.CharField(max_length=20, null=False)
    Area = models.CharField(max_length=20, null=False)
    CAB_LCA = models.CharField(max_length=20, null=False)
    DEV_BGN = models.CharField(max_length=4, null=False)
    DEV_END = models.CharField(max_length=4, null=False)
    DEV_IP = models.CharField(max_length=15, null=False)
    REMARK = models.CharField(max_length=120, null=False)
    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s ' % (self.AST_NUM,self.SR_NUM, self.DEV_NAME, self.DEV_ALS, self.DEV_TYP,self.DEV_MOD,self.OS_TYP,
                self.ADMIN, self.OWN_DPT,  self.MAN_STE,self.MAN_BGN, self.MAN_END,self.UP_TME, self.AST_LAB, self.BUS_DES, self.Location,   self.Area, self.CAB_LCA ,self.DEV_BGN, self.DEV_END,self.DEV_IP,self.REMARK)
