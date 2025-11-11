# GANTI ISI urls.py DENGAN INI:

from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama dan Autentikasi
    path('', views.login_page, name='login'),
    path('auth/login/', views.login, name='api_login'),
    path('auth/registrasi/', views.registrasi_pelanggan, name='registrasi_pelanggan'),
    path('auth/logout/', views.logout, name='logout'),
    
    # Generic Dashboard Redirect
    path('dashboard/', views.dashboard_redirect_view, name='dashboard'), # New generic dashboard

    # Dashboard dan Halaman User
    path('user/dashboard/', views.dashboard_pelanggan_view, name='user_dashboard'), # Renamed from 'dashboard'
    path('user/dashboard/', views.dashboard_pelanggan_view, name='user_index'),
    # path('user/index.html', views.dashboard_pelanggan_view, name='user_index'),
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

    # --- Admin Pages ---
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/manajemen-pesanan/', views.admin_manajemen_pesanan_view, name='admin_manajemen_pesanan'),
    path('admin/manajemen-teknisi/', views.admin_manajemen_teknisi_view, name='admin_manajemen_teknisi'),
    path('admin/manajemen-pelanggan/', views.admin_manajemen_pelanggan_view, name='admin_manajemen_pelanggan'),

    # --- Teknisi Pages ---
    path('teknisi/dashboard/', views.teknisi_dashboard_view, name='teknisi_dashboard'),
    path('teknisi/detail-tugas/', views.teknisi_detail_tugas_view, name='teknisi_detail_tugas'),
]