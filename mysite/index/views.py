from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django_email_verification import send_email
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .forms import SearchTestsForm, SignInForm, SignUpForm, TaskSimpleForm
from .models import DictionaryPage, GuidebookTopics, TaskCompleted, TaskCategory, Theory, GuidebookItem, TaskSimple, TaskDifficultАrchitecture
 


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


def guidebook_item_view(request, id):
  """
  Displaying the theory of tasks
  """
  if not request.user.is_authenticated:
    return redirect('sign_inUrl')
  
  task_object = GuidebookItem.objects.get(pk=id)
  if type(task_object) == TaskSimple:
      if request.method == 'POST':
        form = TaskSimpleForm(data=request.POST)

        if form.is_valid():
          form.save(commit=False)
          answer = form.cleaned_data['answer']

          accuracy = answer.lower() == task_object.answer.lower()
          if accuracy:
            if not TaskCompleted.objects.filter(user=request.user, task=task_object).exists():
              request.user.score += 1
              TaskCompleted.objects.create(user=request.user, task=task_object, completed=True)
              request.user.save()
          
          return render(request, 'index/task_completed.html', {'answer': answer, 'accuracy': accuracy})
            
      else:
        form = TaskSimpleForm()
        
      return render(request, 'index/task_simple.html', {'form': form, 'question': task_object.question})
  
  elif type(task_object) == Theory:
    return render(request, 'index/theory.html', {'theory': task_object})
  
  elif type(task_object) == TaskDifficultАrchitecture:
    allform, allquestion, accuracy = [], [], []
    for task_simple in task_object.task_simple.all():
      allform.append(TaskSimpleForm())
      allquestion.append(task_simple.question)

    
    if request.method == 'POST':
      for enum, item in enumerate(request.POST.getlist('answer')):
        accuracy.append(item.lower() == task_object.task_simple.all()[enum].answer.lower())
        print(accuracy)
      return render(request, 'index/task_difficult_architecture_completed.html', {'data': zip(request.POST.getlist('answer'), accuracy)})
      
    else:
      form = TaskSimpleForm()
    return render(request, 'index/task_difficult_architecture.html', {'tasks': task_object, 'item': zip(allform, allquestion)})


def task_edit(request):
  if not request.user.is_authenticated:
    return redirect('sign_inUrl')
  return render(request, 'index/task_edit.html')

def guidebook_view(request):
  #guiidebook_topics_items = GuidebookTopics.objects.all()
  return render(request, 'index/guidebook.html') #{'guiidebook_topics_items': guiidebook_topics_items})


def dictionary_view(request):
  dictionarypage = DictionaryPage.objects.all()
  if request.method == 'POST':
    dictionary_word_page = DictionaryPage.objects.get(word=request.POST['word'])
    if dictionary_word_page is not None:
      return redirect('dictionary_wordUrl', id=dictionary_word_page.id)

  return render(request, 'index/dictionary.html', {'dictionarypage': dictionarypage})

def dictionary_word_view(request, id):
  word = DictionaryPage.objects.get(pk=id)

  return render(request, 'index/dictionary_word.html', {'word': word})

def tests_view(request, filter='all', filter_value = None): 
  if request.method == 'POST':
    form = SearchTestsForm(data=request.POST)
    if form.is_valid():
      tests = GuidebookItem.objects.filter(title__icontains=form.cleaned_data['title'])
      return redirect('testsUrl', filter=form.cleaned_data['title'])
  else:
    print(filter)

    if filter_value is not None:
      match filter:
        case 'category':  tasks = GuidebookItem.objects.filter(category=TaskCategory.objects.filter(name=filter_value))
    else:
      match filter:
        case 'all': tasks = GuidebookItem.objects.all()
        case 'random': tasks = GuidebookItem.objects.order_by('?')
        
    form = SearchTestsForm()
    print(tasks)
  return render(request, 'index/tests.html', {'form': form, 'tasks': tasks})
  

def secret_game_view(request):
  return render(request, 'index/secret_game.html')

def renpy_game_view(request):
  return render(request, 'index/renpy_game.html')