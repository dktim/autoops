from django.db import models
from django.contrib.auth.models import User
from autoops.privileges import *

class Businesses(models.Model):
    name          =    models.CharField(max_length=50,unique=True,default='')
    informations  =    models.CharField(max_length=200,default='')
    enabled       =    models.BooleanField(default=True)
    def __unicode__(self):
        return self.name
    class Meta:
        permissions = (
               ("can_restart_node","can_restart_node"),
               ("can_stop_node","can_stop_node"),
                ("can_start_node","can_start_node"),
                ("can_execute_cmd","can_execute_cmd"),
                ("can_upload_file","can_upload_file"),
                ("can_change_appstatus","can_change_appstatus"),
                 ("can_manage_user","can_manage_user"),
                ("can_manage_business","can_manage_business"),
                ("can_manage_privi","can_manage_privi"),
                 ("can_manage_asset","can_manage_asset"),
                           
        )

class Privileges(models.Model):
    name          =    models.CharField(max_length=50,unique=True)
    deny          =    models.CharField(max_length=250,default='')
    allow         =    models.CharField(max_length=250,default='')
    informations  =    models.CharField(max_length=200)
    enabled       =    models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class UserProfiles(models.Model):
    user          =   models.OneToOneField(User,on_delete = models.CASCADE)
    department    =   models.CharField(max_length = 100)
    telephone     =   models.CharField(max_length = 50)
    privilege     =   models.ManyToManyField(Privileges)
    business      =   models.ManyToManyField(Businesses)
