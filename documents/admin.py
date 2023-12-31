from django.contrib import admin

from documents.models import Document, User


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'created_by', 'creation_date', 'last_modified', 'status', 'is_template']
    list_filter = ['document_type', 'status', 'is_template', 'creation_date', 'last_modified']
    search_fields = ['title', 'content', 'created_by__username']
    raw_id_fields = ['created_by']
    filter_horizontal = ['shared_with']
    date_hierarchy = 'creation_date'

    def get_queryset(self, request):
        # Custom queryset to improve performance if needed
        qs = super().get_queryset(request)
        return qs.select_related('created_by').prefetch_related('shared_with')

admin.site.register(Document, DocumentAdmin)
