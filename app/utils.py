from django.core.mail import send_mail,EmailMessage
import threading
import time
from django.conf import settings

class SendEmail(threading.Thread):
	def __init__(self,subject,message,email):
		self.email = email
		self.subject = subject
		self.message = message
		threading.Thread.__init__(self)

	def run(self):
		time.sleep(20)
		print("hi")
		try:
			email_from = settings.EMAIL_HOST_USER
			email_message = EmailMessage(self.subject,self.message,email_from,[self.email])
			email_message.content_subtype = 'html'
			email_message.send()
			print("hello")
		except Exception as e:
			print(e)