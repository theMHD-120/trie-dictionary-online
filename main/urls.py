from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('search_word/', views.search_word_view, name='search_word'),
    path('add_word/', views.add_word_view, name='add_word'),
]
