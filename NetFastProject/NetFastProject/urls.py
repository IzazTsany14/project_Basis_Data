"""
URL configuration for NetFastProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 1. Tambahkan import ini
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Ganti ini agar menunjuk ke 'layanan_wifi'
    path('', include('layanan_wifi.urls')),
    
    # 3. Baris ini duplikat dan salah, saya hapus
    # path('dashboard/', include('wifi_service.urls')), 
]

# 4. Tambahkan blok ini di akhir untuk memperbaiki CSS/JS
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
