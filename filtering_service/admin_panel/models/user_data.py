from django.db import models

from admin_panel.mixins.audit_mixin import AuditMixin


class UserData(AuditMixin):
    email = models.CharField(max_length=255, null=True, blank=True)
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    support_level = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    login = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.CharField(max_length=255, null=True, blank=True)
    patronymic = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.email or 'User Data'