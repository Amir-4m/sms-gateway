from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Provider(models.Model):
    CODE_RAHYAB = "RAHYAB"
    PROVIDER_CODES = (
        (CODE_RAHYAB, _('RAHYAB')),
    )

    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    title = models.CharField(_('title'), max_length=120)
    properties = JSONField(_("properties"), default=dict)
    provider_code = models.CharField(_("provider code"), max_length=15, choices=PROVIDER_CODES, default=CODE_RAHYAB)
    head_number = models.IntegerField(_('sms code'))
    is_enable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('head_number', 'provider_code')

    def __str__(self):
        return f"{self.title} - {self.head_number}"


class SMSGateway(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    provider = models.ForeignKey(Provider, related_name='gateways', on_delete=models.PROTECT)
    service = models.ForeignKey('services.Service', related_name='gateways', on_delete=models.PROTECT)
    priority = models.IntegerField(_('priority'), unique=True)
    is_enable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('provider', 'service')

    def __str__(self):
        return f"{self.provider} - {self.service}"
