from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','total_downloads', 'total_emails_sent', 'uploaded_at',)
    list_filter = ('uploaded_at', 'total_downloads', 'total_emails_sent')
    search_fields = ('title', 'description')

admin.site.register(Document, DocumentAdmin)