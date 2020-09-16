from django.contrib import admin

from .models import Provider, SMSGateway, SentMessage


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'provider_code', 'head_number', 'is_enable', 'created_time', 'updated_time')
    list_filter = ('provider_code',)
    search_fields = ('head_number', 'title')


@admin.register(SMSGateway)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'provider', 'is_enable', 'priority', 'created_time', 'updated_time')
    list_filter = ('provider', 'service')
    search_fields = ('provider__head_number',)


@admin.register(SentMessage)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'sms_gateway', 'target_numbers', 'status', 'recipient_id', 'created_time')
    list_filter = ('sms_gateway__provider', 'sms_gateway__service')
    search_fields = ('sms_gateway__provider__head_number',)
    readonly_fields = ('sms_gateway', 'target_numbers', 'status', 'recipient_id', 'text')
