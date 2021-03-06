from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #user = models.ForeignKey(User, unique=True, related_name='profile', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, unique=True, related_name='profile', on_delete=models.CASCADE)
    
    #phone = models.TextField(max_length=20, blank=True, default='')
    #nickname = models.TextField(max_length=20, blank=True, default='')
    phone = models.TextField(max_length=20, blank=True, default='')
    nickname = models.TextField(max_length=20, blank=True, default='')
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''