from django.db import models
import mimetypes

class Document(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    total_downloads = models.PositiveIntegerField(default=0)
    total_emails_sent = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at',]

    def get_file_type(self):
        file_path = self.file.path
        file_type, _ = mimetypes.guess_type(file_path)
        if file_type:
            return file_type.split('/')[0]
       
    def __str__(self):
        return self.title