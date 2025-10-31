# GANTI ISI urls.py DENGAN INI:

from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama dan Autentikasi
    path('', views.login_page, name='login'),
    path('', views.login_page, name='login_page'),
    path('auth/login/', views.login, name='api_login'),
    path('auth/registrasi/', views.registrasi_pelanggan, name='registrasi_pelanggan'),
        path('auth/logout/', views.logout, name='logout'),
    
    # Dashboard dan Halaman User
    path('user/dashboard/', views.dashboard_pelanggan_view, name='dashboard'),
    # convenience alias so /user/index.html (if typed in browser) shows the dashboard
    path('user/index.html', views.dashboard_pelanggan_view, name='user_index'),
    path('user/pemesanan/', views.user_pemesanan, name='pemesanan'),
    # alias used in templates
    path('user/pemesanan/', views.user_pemesanan, name='user_pemesanan'),
    path('user/langganan/', views.user_langganan, name='langganan'),
    path('user/riwayat-testing/', views.user_riwayat_testing, name='riwayat_testing'),
    
    # Endpoint Speed Test
    path('testing/save/', views.save_speed_test, name='save_speed_test'),
    
    # Teknisi Routes
    path('teknisi/tugas/', views.teknisi_tugas, name='teknisi_tugas'),
    path('teknisi/pemesanan/<int:id_pemesanan>/update/', views.teknisi_update_status, name='teknisi_update'),
    
    # Admin Routes
    path('admin/pemesanan/menunggu/', views.admin_pemesanan_menunggu, name='admin_pemesanan'),
    path('admin/penugasan/', views.admin_tugaskan_teknisi, name='admin_penugasan'),
    path('admin/teknisi/list/', views.admin_list_teknisi, name='admin_teknisi'),
    path('admin/paket/', views.admin_paket_layanan, name='admin_paket'),
    path('admin/paket/<int:id_paket>/', views.admin_paket_layanan, name='admin_paket_detail'),
    path('admin/dashboard/stats/', views.admin_dashboard_stats, name='admin_stats'),
    
    # Dashboard dan Halaman User
    path('user/dashboard/', views.dashboard_pelanggan_view, name='dashboard'),
    path('user/pemesanan/', views.user_pemesanan, name='pemesanan'),
    path('user/riwayat-testing/', views.user_riwayat_testing, name='riwayat_testing'),
    path('user/langganan/', views.user_langganan, name='langganan'),
    
    # Endpoint Speed Test
    path('testing/save/', views.save_speed_test, name='save_speed_test'),
    
    # Teknisi Routes
    path('teknisi/tugas/', views.teknisi_tugas, name='teknisi_tugas'),
    path('teknisi/pemesanan/<int:id_pemesanan>/update/', views.teknisi_update_status, name='teknisi_update'),
    
    # Admin Routes
    path('admin/pemesanan/menunggu/', views.admin_pemesanan_menunggu, name='admin_pemesanan'),
    path('admin/penugasan/', views.admin_tugaskan_teknisi, name='admin_penugasan'),
    path('admin/teknisi/list/', views.admin_list_teknisi, name='admin_teknisi'),
    path('admin/paket/', views.admin_paket_layanan, name='admin_paket'),
    path('admin/paket/<int:id_paket>/', views.admin_paket_layanan, name='admin_paket_detail'),
    path('admin/dashboard/stats/', views.admin_dashboard_stats, name='admin_stats'),
]