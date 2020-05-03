from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):  # 为用户新添字段准备数据表
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'user {self.user.username}'