from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

class Userdetails(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='userpic', default='icon.png')
    Wallet= models.FloatField(default=0.00)
    otp=models.CharField(max_length=50, blank=True)
    social_link=models.CharField(max_length=500, blank=True)
    Affiliate=models.CharField(max_length=500, blank=True)
    Wishlist=models.CharField(max_length=500, blank=True)
    cart=models.CharField(max_length=500, blank=True)
    Order=models.CharField(max_length=500, blank=True)
    description=models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)
    
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else: 
            return False

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userdetails.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userdetails.save()



