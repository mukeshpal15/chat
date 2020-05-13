from .views import *
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError, send_mail


def sendmail(e,p):
	try:
		subject='GAZZ - Your Account Password'
		msg= ''' Hi there!,

		Your account's password is,

		your Password is : '''+p+''' 

		Thanks & Regards
		GAZZ APP''' 


		email = EmailMessage(subject, msg, to=[e])
		email.send()
		return 1
	except:
		return 0