from . import views
from django.urls import path


urlpatterns = [
  path('', views.home_view, name='homeUrl'),
  path('profile/', views.profile_view, name='profileUrl'),
  path('sign_in/', views.sign_in_view, name='sign_inUrl'),
  path('sign_up/', views.sign_up_view, name='sign_upUrl'),
  path('guidebook/', views.guidebook_view, name='guidebookUrl'),
  path('task_item/<int:id>/', views.guidebook_item_view, name='task_itemUrl'),
  path('dicitionary/', views.dictionary_view, name='dictionaryUrl'),
  path('dicitionary_word/<int:id>/', views.dictionary_word_view, name='dictionary_wordUrl'),
  path('guidebook_graph/', views.guidebook_graph, name='guidebook_graphUrl'),
  path('tests/<str:filter>/', views.tests_view, name='testsUrl'),
  path('tests/<str:filter>/<str:filter_value>/', views.tests_view, name='testsUrl'),
  path('secret_game/', views.secret_game_view, name='secret_gameUrl'),
]
