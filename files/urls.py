from django.urls import path

from .views import (
    FileListView, FileDownloadView, EmailFileView,
    SearchView, FileUploadView, FileDetailView,
)

urlpatterns = [
    path('', FileListView.as_view(), name='list'),
    path('detail/<int:pk>/', FileDetailView.as_view(), name='file_detail'),
    path('file-upload/', FileUploadView.as_view(), name='file_upload'),
    path('search/', SearchView.as_view(), name='file_search'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file_download'),
    path('email/file/<int:file_id>/', EmailFileView.as_view(), name='email_file'),
]
