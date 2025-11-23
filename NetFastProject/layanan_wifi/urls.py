from django.urls import path
from . import views

urlpatterns = [
    # Root path for login page
    path('', views.login_page, name='login_page'),

    # Authentication
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
<<<<<<< HEAD
    
    # Generic Dashboard Redirect
    path('dashboard/', views.dashboard_redirect_view, name='dashboard'), # New generic dashboard

    # Dashboard dan Halaman User
    path('user/dashboard/', views.dashboard_pelanggan_view, name='user_dashboard'), # Renamed from 'dashboard'
    path('user/dashboard/', views.dashboard_pelanggan_view, name='user_index'),
    
    # User pages
=======

    # User Views
    path('user/dashboard/', views.dashboard_pelanggan_view, name='dashboard'),
>>>>>>> 5871e0f2112f2a668ba64d308a3c3aa076281f3f
    path('user/speed-test/', views.speed_test_view, name='speed_test'),
    path('user/speed-history/', views.speed_history_view, name='speed_history'),
    path('user/packages/', views.packages_view, name='packages'),
    path('user/services-history/', views.services_history_view, name='services_history'),
    path('user/edit-profile/', views.edit_profile_view, name='edit_profile'),

    # API Endpoints
    path('api/packages/', views.package_api, name='package_api'),
    path('api/packages/delete/', views.delete_package_api, name='delete_package_api'),
    path('api/speed-test/', views.speed_test_api, name='speed_test_api'),
    path('api/user/profile/', views.profile_api, name='profile_api'),
    path('api/user/services/', views.services_list_api, name='services_list_api'),
    path('api/user/services/<int:service_id>/', views.service_detail_api, name='service_detail_api'),
    path('api/user/speed-history/', views.user_riwayat_testing, name='user_riwayat_testing'),
    path('api/services-history/', views.services_history_api, name='services_history_api'),
    path('api/ping-test/', views.ping_test_api, name='ping_test_api'),
    path('api/speed-test-upload/', views.speed_test_upload, name='speed_test_upload'),

    # User Pemesanan
    path('user/pemesanan/', views.user_pemesanan, name='user_pemesanan'),

    # Admin Endpoints
    path('admin/pemesanan-menunggu/', views.admin_pemesanan_menunggu, name='admin_pemesanan_menunggu'),
    path('admin/tugaskan-teknisi/', views.admin_tugaskan_teknisi, name='admin_tugaskan_teknisi'),
    path('admin/list-teknisi/', views.admin_list_teknisi, name='admin_list_teknisi'),
    path('admin/paket-layanan/', views.admin_paket_layanan, name='admin_paket_layanan'),
    path('admin/paket-layanan/<int:id_paket>/', views.admin_paket_layanan, name='admin_paket_layanan_detail'),

    # Teknisi Endpoints
    path('teknisi/tugas/', views.teknisi_tugas, name='teknisi_tugas'),
<<<<<<< HEAD
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
=======
    path('teknisi/update-status/<int:id_pemesanan>/', views.teknisi_update_status, name='teknisi_update_status'),

    # Legacy/Compatibility
    path('api/user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('api/user/langganan/', views.user_langganan, name='user_langganan'),
    path('api/save-speed-test/', views.save_speed_test, name='save_speed_test'),
    path('api/registrasi/', views.registrasi_pelanggan, name='registrasi_pelanggan'),
    path('api/admin/dashboard-stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
]
>>>>>>> 5871e0f2112f2a668ba64d308a3c3aa076281f3f
