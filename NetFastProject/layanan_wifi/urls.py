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
    
    # User pages
    path('user/speed-test/', views.speed_test_view, name='speed_test'),
    path('user/speed-history/', views.speed_history_view, name='speed_history'),
    path('user/edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('user/packages/', views.packages_view, name='packages'),
    path('user/services-history/', views.services_history_view, name='services_history'),
    
    # User API endpoints
    path('api/user/data/', views.user_dashboard, name='user_data'),
    path('api/user/profile/', views.profile_api, name='profile_api'),
    path('api/user/packages/', views.package_api, name='package_api'),
    path('api/packages/', views.package_api, name='packages_api'),  # Alias for consistency
    path('api/speed-test/', views.speed_test_api, name='speed_test_api'),
    path('api/speed-test/history/', views.user_riwayat_testing, name='speed_test_history'),
    path('api/services/', views.services_list_api, name='services_api'),
    path('api/services/<int:service_id>/', views.service_detail_api, name='service_detail_api'),
    path('api/services-history/', views.services_history_api, name='services_history_api'),
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
    path('admin/penugasan/', views.admin_tugaskan_teknisi, name='admin_penugasan'),

    # Admin Order Management
    path('api/admin/pesanan-menunggu/', views.admin_pemesanan_menunggu, name='admin_pesanan_menunggu'),
    path('api/admin/pesanan-aktif/', views.admin_pesanan_aktif, name='admin_pesanan_aktif'),
    path('api/admin/teknisi/list/', views.admin_list_teknisi, name='admin_teknisi_list'),
    path('admin/paket/', views.admin_paket_layanan, name='admin_paket'),
    path('admin/paket/<int:id_paket>/', views.admin_paket_layanan, name='admin_paket_detail'),
    path('admin/dashboard/stats/', views.admin_dashboard_stats, name='admin_stats'),
    path('admin/dashboard/chart/', views.admin_dashboard_chart, name='admin_chart'),

    # Admin Customer Management
    path('api/admin/pelanggan/', views.admin_pelanggan, name='admin_pelanggan'),
    path('api/admin/pelanggan/<int:id_pelanggan>/', views.admin_pelanggan, name='admin_pelanggan_detail'),
    path('api/admin/pelanggan/<int:id_pelanggan>/delete/', views.admin_pelanggan, name='admin_pelanggan_delete'),

    # Admin Technician Management
    path('api/admin/teknisi/', views.admin_teknisi, name='admin_teknisi'),
    path('api/admin/teknisi/<int:id_teknisi>/', views.admin_teknisi, name='admin_teknisi_detail'),
    path('api/admin/teknisi/<int:id_teknisi>/delete/', views.admin_teknisi, name='admin_teknisi_delete'),

    # Admin Area Layanan
    path('api/area-layanan/', views.admin_area_layanan, name='admin_area_layanan'),


    # --- Admin Pages ---
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/manajemen-pesanan/', views.admin_manajemen_pesanan_view, name='admin_manajemen_pesanan'),
    path('admin/manajemen-teknisi/', views.admin_manajemen_teknisi_view, name='admin_manajemen_teknisi'),
    path('admin/manajemen-pelanggan/', views.admin_manajemen_pelanggan_view, name='admin_manajemen_pelanggan'),

    # --- Teknisi Pages ---
    path('teknisi/dashboard/', views.teknisi_dashboard_view, name='teknisi_dashboard'),
    path('teknisi/detail-tugas/', views.teknisi_detail_tugas_view, name='teknisi_detail_tugas'),
]