from django import forms
from .models import Document

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']
