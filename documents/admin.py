from django.contrib import admin

from documents.models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'content', 'document_type', 'creation_date', 'last_modified', 
        'status', 'is_template', 'access_level', 
    ]


admin.site.register(Document, DocumentAdmin)
