import secrets
import string

from django.contrib import admin
from django.http import HttpResponseRedirect

from apps.services.models import Service


@admin.register(Service)
class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_enable', 'created_time', 'updated_time')
    list_filter = ('is_enable',)
    readonly_fields = ('secret_key',)

    change_form_template = "services/admin/change-form.html"

    def random_secret_generator(self, length):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(length))

    def response_change(self, request, obj):
        if "change-secret" in request.POST:
            key = self.random_secret_generator(10)
            while True:
                if not Service.objects.filter(secret_key=key).exists():
                    obj.secret_key = key
                    obj.save()
                    break

            return HttpResponseRedirect(".")  # stay on the same detail page
        return super().response_change(request, obj)
