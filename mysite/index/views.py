from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from .forms import SignInForm, SignUpForm
#from .models import GuidebookTopics
# Create your views here.



def home_view(request):
	return render(request, 'main/home.html')


def profile_view(request):
	if not request.user.is_authenticated:
		return redirect('sign_inUrl')
	return render(request, 'main/profile.html')


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
			form = SignInForm()
			return render(request, 'main/sign_in.html', {'form':form})
	else:
		return redirect('profileUrl')


def sign_up_view(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('sign_inUrl')
	else:
		form = SignUpForm()
	return render(request, 'main/sign_up.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('homeUrl')




def task_view(request):
	return render(request, 'main/task.html')


def guidebook_view(request):
	#guiidebook_topics_items = GuidebookTopics.objects.all()
	return render(request, 'main/guidebook.html') #{'guiidebook_topics_items': guiidebook_topics_items})


def dictionary_view(request):
	return render(request, 'main/dictionary.html')


def articles_view(request):
	return render(request, 'main/articles.html')


def one_article_view(request):
	return render(request, 'main/one_article.html')