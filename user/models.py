from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from .constant import USER_ROLE


# 고객 모델 생성
class CustomManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, email=None, role=None):
        if not email:
            raise ValueError("must have user email")

        user = self.model(
            email=self.normalize_email(email),
            role=role if role in USER_ROLE.__members__ else USER_ROLE.CUST.name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


# 고객 모델(테이블)
class Custom(AbstractBaseUser):
    objects = CustomManager()

    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    role = models.CharField(max_length=10, null=False, default=USER_ROLE.CUST.name)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "custom"

    is_superuser = models.BooleanField(default=False)
    s_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]
