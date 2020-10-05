import re
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import SMSGateway


def phone_number_validator(value):
    if re.match(r'^(0)?9\d{9}$', value) is None:
        raise serializers.ValidationError(_('enter phone_number in the correct form!'))


class MessageSerializer(serializers.Serializer):
    phone_numbers = serializers.ListField(
        child=serializers.CharField(validators=[phone_number_validator]),
        required=True
    )
    text = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()


class SendSMSSerializer(serializers.Serializer):
    data = serializers.ListField(child=MessageSerializer())

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
