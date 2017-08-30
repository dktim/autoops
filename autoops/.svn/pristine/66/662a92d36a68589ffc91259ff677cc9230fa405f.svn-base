#coding=utf-8


from django.contrib.auth.models import User
from myauth.models import Account

class MyCustomBackend:
	def authenticate(self,username=None,password=None):
		try:
			user=Account.objects.get(username=username)
		except Account.DoesNotExist:
			return None
		else:
			if user.check_password(password):
				try:
					django_user=User.objects.get(username=username)
				except User.DoesNotExist:
					django_user=User(username=user.username,password=user.password)
					django_user.is_staff=True
					djangp_user.save()
				return django_user
			else:
				return None

	def get_user(self,user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
