# File: NetFastProject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wifi_service.urls')),  
]

# --- ⬇️ PERBAIKAN ADA DI SINI ⬇️ ---
# Ini penting agar 'runserver' mau memuat file CSS/JS dari folder 'static'
if settings.DEBUG:
    # Ganti 'settings.STATIC_ROOT' menjadi 'settings.STATICFILES_DIRS[0]'
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])