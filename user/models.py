from django.db import models
from django.contrib.auth.models import User

from conf.models import District, SubCounty, Parish, County
from system.models import Clan
from system.models import TimeStampMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    profile_photo = models.ImageField(upload_to='user/', null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    sex = models.CharField('Sex', max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), null=True,
                           blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nin = models.CharField(max_length=255, null=True, blank=True)
    is_agent = models.BooleanField(default=False)
    clan = models.ForeignKey(Clan, null=True, blank=True, on_delete=models.CASCADE)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="profile_district")
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.SET_NULL)
    village = models.CharField(max_length=150, null=True, blank=True)
    gps_coodinates = models.CharField(max_length=150, null=True, blank=True)
    district_incharge = models.ManyToManyField(District, null=True, blank=True)
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ForeignKey(User, null=True, blank=True, related_name="supervisor", on_delete=models.SET_NULL)
    is_locked = models.BooleanField(default=0)
    receive_sms_notifications = models.BooleanField(default=0)
    enable_mfa = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'user_profile'


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.get_or_create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'user'):
#         instance.user.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def refresh_auth_token(sender, instance=None, **kwargs):
    Token.objects.filter(user=instance).delete()
    Token.objects.create(user=instance)