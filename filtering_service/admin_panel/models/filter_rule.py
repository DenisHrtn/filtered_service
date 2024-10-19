from admin_panel.mixins.audit_mixin import AuditMixin
from django.db import models


class FilterRule(AuditMixin):
    regex = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
