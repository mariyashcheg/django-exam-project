from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField("Полное имя", max_length=100, default='', blank=True, null=True) 
    info = models.CharField("О себе", max_length=300, default='-')
    photo = models.ImageField("Фото", upload_to='accounts', default='accounts/default.jpg')

    def __str__(self):
        return self.user.username
    
    def get_pk_for_photo(self):
        return self.user.pk

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.account.save()
    
