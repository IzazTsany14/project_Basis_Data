from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wifi_service.urls')),  # URL root mengarah ke aplikasi wifi_service
]
