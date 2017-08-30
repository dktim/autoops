from __future__ import unicode_literals

from django.db import models

# Create your models here.




from django.db import models
import hashlib


class Account(models.Model):
	username=models.CharField('username',blank=True,max_length=32)
	password=models.CharField('password',blank=True,max_length=50)
	is_active=models.IntegerField('is_active',blank=True)

	def __unicode__(self):
		return self.username
	def is_authenticated(self):
		return True
	def hashed_pasword(self,password=None):
		if not password:
			return self.password
		else:
			return hashlib.md5(password).hexdigest()
	def check_password(self,password):
		if selt.hashed_password(password)==self.password:
			return True
		return Flase





	class Meta:
		db_table="account"
