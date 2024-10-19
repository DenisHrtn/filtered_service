from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from users.managers.user_manager import UserManager
from admin_panel.mixins.audit_mixin import AuditMixin


class User(AbstractUser, AuditMixin):
    id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', ]

    objects = UserManager()

    def gas_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

    def update_fields(self, **kwargs):
        for field, value in kwargs.items():
            if field == 'password':
                self.set_password(value)
            else:
                setattr(self, field, value)
        self.save()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
