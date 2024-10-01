from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Map the root URL to index view
    path('api_content/', views.api_content, name='api_content'),
]
