# GANTI ISI urls.py DENGAN INI:

from django.urls import path
from . import views

urlpatterns = [
    # URL untuk halaman login
    path('', views.login_page, name='login_page'),
    # URL untuk API login
    path('auth/login/', views.login, name='login'),
    path('auth/registrasi/', views.registrasi_pelanggan, name='registrasi_pelanggan'),

    # Endpoint User
    path('user/dashboard/', views.dashboard_pelanggan_view, name='dashboard_pelanggan'),
    path('user/pemesanan/', views.user_pemesanan, name='user_pemesanan'),
    path('user/langganan/', views.user_langganan, name='user_langganan'),
    path('user/riwayat-testing/', views.user_riwayat_testing, name='user_riwayat_testing'),
    # Endpoint Tagihan & Notifikasi dihapus
    
    # Endpoint Speed Test
    path('testing/save/', views.save_speed_test, name='save_speed_test'),

    # Endpoint Teknisi
    path('teknisi/tugas/', views.teknisi_tugas, name='teknisi_tugas'),
    path('teknisi/pemesanan/<int:id_pemesanan>/update/', views.teknisi_update_status, name='teknisi_update_status'),
    # Endpoint Laporan dihapus

    # Endpoint Admin
    path('admin/pemesanan/menunggu/', views.admin_pemesanan_menunggu, name='admin_pemesanan_menunggu'),
    path('admin/penugasan/', views.admin_tugaskan_teknisi, name='admin_tugaskan_teknisi'),
    # Mengganti 'teknisi/tersedia' menjadi 'teknisi/list'
    path('admin/teknisi/list/', views.admin_list_teknisi, name='admin_list_teknisi'),
    path('admin/paket/', views.admin_paket_layanan, name='admin_paket_layanan_list'),
    path('admin/paket/<int:id_paket>/', views.admin_paket_layanan, name='admin_paket_layanan_detail'),
    path('admin/dashboard/stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
]