from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import SMSGateway


class SendSMSSerializer(serializers.Serializer):
    text = serializers.CharField()
    phone_numbers = serializers.ListField(child=serializers.RegexField(r'^(0)?9\d{9}$'))

    def validate(self, attrs):
        service = self.context['service']
        sms_gateway = SMSGateway.objects.filter(
            service=service,
            provider__is_enable=True,
            is_enable=True).order_by('priority').first()
        if sms_gateway is not None:
            attrs.update({'sms_gateway': sms_gateway})
            return attrs
        else:
            raise ValidationError(_('there is no available sms gateway for this service!'))

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()
