from django.db import models
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    name = models.CharField(_('name'), max_length=120, null=False, blank=False)
    secret_key = models.CharField(_('secret key'), max_length=50, null=False, blank=False, unique=True)
    is_enable = models.BooleanField(_('is enable'), default=True)

    def __str__(self):
        return self.name
