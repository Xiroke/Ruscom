from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django_email_verification import send_email
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import SearchTestsForm, SignInForm, SignUpForm, TaskSimpleForm
from .models import DictionaryPage, GuidebookTopics, TaskSimple, TaskCompleted, TaskCategory, Theory
 
  
def get_children(topic, data):
  children = topic.child.all()
  for child_topic in children:
    data["nodes"].append({'id': child_topic.name, 'label': child_topic.name, 'pack_tasks_title': [i.title for i in child_topic.task_pack.all()], 'pack_tasks_id': [i.pk for i in child_topic.task_pack.all()]})
    data["links"].append({'from': topic.name, 'to': child_topic.name})
    data = get_children(child_topic, data)
  else: 
    return data 
  

def home_view(request):
  return render(request, 'index/home.html')


def profile_view(request):
  if not request.user.is_authenticated:
    return redirect('sign_inUrl')
  return render(request, 'index/profile.html')


def sign_in_view(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
      form = SignInForm(data=request.POST)
      if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
          login(request, user)
          return redirect('profileUrl')
        else:
          return render(request, 'index/sign_in.html', {'form':form})
    else:
      form = SignInForm()
      return render(request, 'index/sign_in.html', {'form':form})
  else:
    return redirect('profileUrl')


def sign_up_view(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save(commit=False)
      user_name = form.cleaned_data['name']
      user_email = form.cleaned_data['email']
      user_password = form.cleaned_data['password1']

      # Create new user
      user = get_user_model().objects.create_user(name=user_name, email=user_email, password=user_password)
      user.is_active = False
      send_email(user)

      return HttpResponseRedirect(reverse('sign_inUrl'))

  else:
    form = SignUpForm()
  return render(request, 'index/sign_up.html', {'form': form})


def logout_view(request):
  logout(request)
  return redirect('homeUrl')
    

def guidebook_graph(request):
  topics = GuidebookTopics.objects.get(name = 'Ruscom')
  
  data = {
    "nodes": [],
    "links": [],
  }
  data["nodes"].append({'id': topics.name, 'label': topics.name})
  data = get_children(topics, data)
  print(data['nodes'])
  return render(request, 'index/guidebook_graph.html', {'data': data}, )


def task_simple(request, id):
  if not request.user.is_authenticated:
    return redirect('sign_inUrl')
  
  task_object = TaskSimple.objects.get(pk=id)
  if request.method == 'POST':
    form = TaskSimpleForm(data=request.POST)

    if form.is_valid():
      form.save(commit=False)
      answer = form.cleaned_data['answer']

      if answer == task_object.answer:
        if not TaskCompleted.objects.filter(user=request.user, task=task_object).exists():
          request.user.score += 1
          TaskCompleted.objects.create(user=request.user, task=task_object, completed=True)
          request.user.save()
      
      return render(request, 'index/task_simple.html', {'form': form, 'question': task_object.question})
        
  else:
    form = TaskSimpleForm()
    
  return render(request, 'index/task_simple.html', {'form': form, 'question': task_object.question})


def theory_view(request, id):
  theory = Theory.objects.get(pk=id)
  return render(request, 'index/theory.html', {'theory': theory})

def task_edit(request):
  if not request.user.is_authenticated:
    return redirect('sign_inUrl')
  return render(request, 'index/task_edit.html')


def guidebook_view(request):
  #guiidebook_topics_items = GuidebookTopics.objects.all()
  return render(request, 'index/guidebook.html') #{'guiidebook_topics_items': guiidebook_topics_items})


def dictionary_view(request):
  dictionarypage = DictionaryPage.objects.all()
  return render(request, 'index/dictionary.html', {'dictionarypage': dictionarypage})

def tests_view(request, filter='all', filter_value = None):
  if request.method == 'POST':
    form = SearchTestsForm(data=request.POST)
    if form.is_valid():
      tests = TaskSimple.objects.filter(title__icontains=form.cleaned_data['title'])
      return redirect('testsUrl', filter=form.cleaned_data['title'])
  else:
    print(filter)

    if filter_value is not None:
      match filter:
        case 'category':  tasks = TaskSimple.objects.filter(category=TaskCategory.objects.filter(name=filter_value))
    else:
      match filter:
        case 'all': tasks = TaskSimple.objects.all()
        case 'random': tasks = TaskSimple.objects.order_by('?')
        
    form = SearchTestsForm()
    print(tasks)
  return render(request, 'index/tests.html', {'form': form, 'tasks': tasks})
  

