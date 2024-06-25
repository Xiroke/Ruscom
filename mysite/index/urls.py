from django.views.generic.base import TemplateView

from django.urls import path

from .views import *


urlpatterns = [
  path('', TemplateView.as_view(template_name='index/home.html'), name='home'),
  
  path('profile/', Profile.as_view(), name='profile'),
  path('login/', Login.as_view(), name='login'),
  path('register/', Register.as_view(), name='register'),
  path('logout/', Logout.as_view(), name='logout'),

  path('dicitionary/', Dictionary.as_view(), name='dictionary'),
  path('dicitionary/<int:id>/', DictionaryWord.as_view(), name='dictionary_word'),
  path('guidebook_graph/', GuidebookGraph.as_view(), name='guidebook_graph'),
  path('guidebook_item_handler/<int:id>/', GuidebookItemHandler.as_view(), name='guidebook_handler'),

  path('tasks/', Tasks.as_view(), name='tasks'),
  path('task_item/<int:id>/', GuidebookItemHandler.as_view(), name='task_item'),
  path('theory/', Theory.as_view(), name='theory'),
  path('task_simple', TaskSimple.as_view(), name="task_simple"),
  path('task_difficult_architecture', TaskDifficultArchitecture.as_view(), name="task_difficult_architecture"),

  path("renpy_game/", TemplateView.as_view(template_name="index/renpy_game.html"), name="renpy_game"),
  path('secret_game/', TemplateView.as_view(template_name='index/secret_game.html'), name='secret_game'),

  path('products/', TemplateView.as_view(template_name='index/products.html'), name='products'),
  path('products/<str:file>/', ProductsFile.as_view(), name='products_file'),
]
