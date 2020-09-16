import re
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_compound_fields.fields import ListOrItemField

from ..models import SMSGateway


class SendSMSSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=serializers.DictField(
            child=ListOrItemField(
                child=serializers.CharField()
            )
        )
    )

    def validate(self, attrs):
        for data in attrs['data']:
            text = data.get('text')
            phone_numbers = data.get('phone_numbers')
            if None in [text, phone_numbers]:
                raise ValidationError(_('text and phone_number fields are required!'))
            for number in phone_numbers:
                if re.match(r'^(0)?9\d{9}$', number) is None:
                    raise ValidationError(_('enter phone_number in the correct form!'))

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
