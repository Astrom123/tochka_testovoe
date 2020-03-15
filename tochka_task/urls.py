from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('subscribers.urls')),
    path('admin/', admin.site.urls),
]
