from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='homeUrl'),
    path('profile/', views.profile_view, name='profileUrl'),
    path('sign_in/', views.sign_in_view, name='sign_inUrl'),
    path('sign_up/', views.sign_up_view, name='sign_upUrl'),
    path('guidebook/', views.guidebook_view, name='guidebookUrl'),
    path('task/', views.task_view, name='taskUrl'),
    path('dicitionary/', views.dictionary_view, name='dictionaryUrl'),
    path('articles/', views.articles_view, name='articlesUrl'),
    path('one_article/', views.one_article_view, name='one_articleUrl'),
]
