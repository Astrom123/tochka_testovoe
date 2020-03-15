from django.urls import path
from subscribers import views

urlpatterns = [
    path('ping/', views.ping),
    path('add/', views.add),
    path('substract/', views.subtract),
    path('status/', views.status),
]
