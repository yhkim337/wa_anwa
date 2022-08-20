from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    kakao_id = models.IntegerField(blank=True, null=True)
    profile_img = models.TextField(verbose_name='프로필 이미지 URL', blank=True, null=True)
    connected_at = models.DateTimeField(default=timezone.now)
    point = models.IntegerField(default=0)