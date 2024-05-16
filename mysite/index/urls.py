from . import views
from django.urls import path


urlpatterns = [
  path('', views.home_view, name='homeUrl'),
  path('profile/', views.profile_view, name='profileUrl'),
  path('sign_in/', views.sign_in_view, name='sign_inUrl'),
  path('sign_up/', views.sign_up_view, name='sign_upUrl'),
  path('guidebook/', views.guidebook_view, name='guidebookUrl'),
  path('task_type1/<int:id>/', views.task_simple, name='task_type1Url'),
  path('theory/<int:id>/', views.theory_view, name='theoryUrl'),
  path('dicitionary/', views.dictionary_view, name='dictionaryUrl'),
  path('guidebook_graph/', views.guidebook_graph, name='guidebook_graphUrl'),
  path('tests/<str:filter>/', views.tests_view, name='testsUrl'),
  path('tests/<str:filter>/<str:filter_value>/', views.tests_view, name='testsUrl'),
]
