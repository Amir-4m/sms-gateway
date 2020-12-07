from django.contrib import admin

from .models import Provider, SMSGateway, SentMessage


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider_code', 'head_number', 'is_enable', 'created_time', 'updated_time')
    list_filter = ('provider_code',)
    search_fields = ('head_number', 'title')


@admin.register(SMSGateway)
class SMSGatewayAdmin(admin.ModelAdmin):
    list_display = ('service', 'provider', 'is_enable', 'priority', 'created_time', 'updated_time')
    list_filter = ('provider', 'service')
    search_fields = ('provider__head_number',)


@admin.register(SentMessage)
class SentMessagesAdmin(admin.ModelAdmin):
    list_display = ('phone_numbers', 'sms_gateway', 'result', 'recipient_id', 'created_time')
    list_filter = ('sms_gateway__provider', 'sms_gateway__service')
    search_fields = ('target_number',)
    readonly_fields = ('sms_gateway', 'phone_numbers', 'result', 'recipient_id', 'text')
