from django.shortcuts import get_object_or_404, render, redirect

from django_email_verification import send_email
from django.contrib.auth import get_user_model
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import SearchTestsForm, LoginForm, RegisterForm, TaskSimpleForm
from .models import DictionaryModel, GuidebookTopicsModel, TaskCompletedModel, TaskCategoryModel, TheoryModel, GuidebookItemModel, TaskSimpleModel, TaskDifficultАrchitectureModel
 
from django.views.generic import ListView, FormView, TemplateView, View, DetailView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView

import json


def get_children(topic, data):
  children = topic.child.all()
  for child_topic in children:
    data["nodes"].append({
      'id': child_topic.name, 
      'label': child_topic.name, 
      'pack_guidebook_item_title': [i.title for i in child_topic.guidebook_item.all()],
      'pack_guidebook_item_id': [i.pk for i in child_topic.guidebook_item.all()],
      'pack_guidebook_item_type': [i for i in child_topic.guidebook_item.all()],
    })
    data["links"].append({'source': topic.name, 'target': child_topic.name})
    data = get_children(child_topic, data)
  else: 
    return data 

class Profile(TemplateView):
  template_name = 'index/profile.html'

  def get(self, request):
    if not request.user.is_authenticated:
      return redirect('login')
    
    return super().get(self, request)
  

class Login(LoginView):
  template_name = 'index/login.html'
  form_class = LoginForm


class Register(FormView):
  template_name = 'index/register.html'
  form_class = RegisterForm
  success_url = '/'

  def form_valid(self, form):
    form.save(commit=False)
    user_name = form.cleaned_data['name']
    user_email = form.cleaned_data['email']
    user_password = form.cleaned_data['password1']

    # Create new user
    user = get_user_model().objects.create_user(name=user_name, email=user_email, password=user_password)
    #user.is_active = False
    send_email(user)

    return super().form_valid(form)

class Logout(LogoutView):
  template_name = 'index/logged_out.html'
  
class GuidebookGraph(TemplateView):
  #_________________________json_script tag django html__________________________
  template_name = 'index/guidebook_graph.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    topics = get_object_or_404(GuidebookTopicsModel, name = 'Ruscom')
  
    data = {
      "nodes": [],
      "links": [],
    }
    data["nodes"].append({'id': topics.name, 'label': topics.name})
    data = get_children(topics, data)
    context['data'] = data
    return context

class GuidebookItemHandler(View):
  def get(self, request, id):
    self.guidebook_item = get_object_or_404(GuidebookItemModel, pk=id)
    if type(self.guidebook_item) == TheoryModel:
      return redirect('theory', pk=id)
    elif type(self.guidebook_item) == TaskSimpleModel:
      return redirect('task_simple', pk=id)
    elif type(self.guidebook_item) == TaskDifficultАrchitectureModel:
      return redirect('task_difficult_architecture', pk=id)

class TaskDifficultArchitecture(TemplateView):
  template_name = 'index/task_difficult_architecture.html'
  
  def get(self, request, id):
    self.allform, self.allquestion, self.accurancy = [], [], []
    self.guidebook_item = get_object_or_404(GuidebookItemModel, pk=id)
    
    if not request.user.is_authenticated:
      return redirect('login')
    
    for task_simple in self.guidebook_item.task_simple.all():
      self.allform.append(TaskSimpleForm())
      self.allquestion.append(task_simple.question)
      return super().get(request)
  
  def post(self, request):
    for enum, item in enumerate(request.POST.getlist('answer')):
      if item.lower() == self.guidebook_item.task_simple.all()[enum].answer.lower():
        self.accuracy.append(True)
        if not TaskCompletedModel.objects.filter(user=request.user, task=self.guidebook_item.task_simple.all()[enum]).exists():
          request.user.score += 1
          TaskCompletedModel.objects.create(user=request.user, task=self.guidebook_item.task_simple.all()[enum], completed=True)
          request.user.save()
      else:
        self.accuracy.append(False)
    return render(request, 'index/task_difficult_architecture_completed.html', {'data': zip(request.POST.getlist('answer'), self.accuracy)})
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['guidebook_item'] = self.guidebook_item
    context['item'] = zip(self.allform, self.allquestion)
    return context

class Theory(DetailView):
  model = TheoryModel
  template_name = 'index/theory.html'

  def get(self, request, id):
    self.guidebook_item = get_object_or_404(Theory, pk=id)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['guidebook_item'] = self.guidebook_item
    return context

class TaskSimple(FormView):
  form_class = TaskSimpleForm
  template_name = 'index/task_simple.html'

  def get(self, request, pk):
    if not request.user.is_authenticated:
      return redirect('login')
    self.guidebook_item = get_object_or_404(GuidebookItemModel, pk=pk)
    return super().get(request)
  
  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['question'] = self.guidebook_item.question
    return context

  def post(self, request):
    form = super().post(request)
    form.save(commit=False)
    answer = form.cleaned_data['answer']
    accuracy = answer.lower() == self.guidebook_item.answer.lower()
    if accuracy:
      if not TaskCompletedModel.objects.filter(user=request.user, task=self.guidebook_item).exists():
        request.user.score += 1
        TaskCompletedModel.objects.create(user=request.user, task=self.guidebook_item, completed=True)
        request.user.save()
      return render(request, 'index/task_completed.html', {'answer': answer, 'accuracy': accuracy}) 
    

class Dictionary(ListView): 
  template_name = 'index/dictionary.html'
  model = DictionaryModel
  context_object_name = 'dictionary'

  def post(self, request):
    word_object = self.model.objects.get(word=request.POST['word'])
    if word_object is not None:
      return redirect(reverse('dictionary_word', args=[word_object.id]))
  
  
class DictionaryWord(TemplateView):
  template_name = 'index/dictionary_word.html'

  def get(self, request, id):
    self.id = int(id)
    return super().get(self, request)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['word'] = DictionaryModel.objects.get(pk=self.id)
    return context
  
class Tasks(ListView):
  model = TaskDifficultАrchitectureModel
  template_name = 'index/tests.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks'] = TaskDifficultАrchitectureModel.objects.all()
    return context

class ProductsFile(View):
  def get(self, request, file):
    if file[-1: -4: -1] == 'fdp': #pdf reverse
      url = 'products/' + file
      return render(request, 'index/products_pdf.html', {'url': url})
    else:
      return redirect('products')