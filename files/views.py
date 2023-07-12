from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.views.generic.edit import FormView

from .models import Document
from .forms import FileUploadForm


class FileListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'files/list.html'
    context_object_name = 'files'
    paginate_by = 6
 
    
    
class FileDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'files/detail.html'
    context_object_name = 'file'
    

class FileUploadView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    template_name = 'files/upload_file.html'
    form_class = FileUploadForm
    success_url = reverse_lazy('list')
    success_message = 'File Uploaded Successfully'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        file_obj = form.cleaned_data['file']
        print(file_obj)
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        
        file_instance = Document(title=title, description=description, file=file_obj)
        file_instance.save()
        return super().form_valid(form)
    
    
class FileDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        file = get_object_or_404(Document, pk=self.kwargs['file_id'])
        file.total_downloads += 1
        file.save()
        return redirect(file.file.url)
    

class EmailFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        file = get_object_or_404(Document, pk=self.kwargs['file_id'])
        recipient_email = request.POST.get('recipient_email')
        message = request.POST.get('message')    
        email = EmailMessage(
            f'{file.title}',
            message,
            self.request.user.email,
            [recipient_email],
        )
        email.attach_file(file.file.path)
        email.send()
        
        file.total_emails_sent += 1
        file.save()
        messages.success(request, f'"{file.title}" successfully emailed')
        return redirect('file_detail', pk=self.kwargs['file_id'])
    
    
class SearchView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'files/search_results.html'
    context_object_name = 'files'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Document.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context