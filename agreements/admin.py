from django.contrib import admin

from .models import Agreement, Amendment, DigitalSignature


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'effective_date', 'expiration_date', 'agreement_type', 'last_amended_date')
    list_filter = ('status', 'agreement_type', 'created_by')
    search_fields = ('title', 'content')


class AmendmentAdmin(admin.ModelAdmin):
    list_display = ('agreement', 'updated_by', 'updated_at', 'version')
    list_filter = ('updated_by',)
    search_fields = ('agreement__title', 'description')


class DigitalSignatureAdmin(admin.ModelAdmin):
    list_display = ('amendment', 'signee', 'signed_at')
    list_filter = ('signee',)
    search_fields = ('amendment__agreement__title',)


# Register your models here
admin.site.register(Agreement, AgreementAdmin)
admin.site.register(Amendment, AmendmentAdmin)
admin.site.register(DigitalSignature, DigitalSignatureAdmin)
