from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView , FormView
from django.contrib.auth.views import LoginView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class TaskList(LoginRequiredMixin ,ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        
        input = self.request.GET.get('input_search') or ''
        
        if input:
            context['tasks'] = context['tasks'].filter(title__icontains = input)
            
            context['input_search'] = input
        
        return context

class Register(FormView):
    template_name = 'base/register.html'
    success_url = reverse_lazy('tasks')
    form_class = UserCreationForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request , user)
        return super(Register, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register, self).get(*args, **kwargs)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(CreateView):
    model = Task
    fields = ['title' , 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task
    fields = ['title' , 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')