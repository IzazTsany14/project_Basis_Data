from django.urls import path
from . import views

urlpatterns = [
    # Root path for login page
    path('', views.login_page, name='login_page'),

    # Authentication
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),

    # User Views
    path('user/dashboard/', views.dashboard_pelanggan_view, name='dashboard'),
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
    path('teknisi/update-status/<int:id_pemesanan>/', views.teknisi_update_status, name='teknisi_update_status'),

    # Legacy/Compatibility
    path('api/user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('api/user/langganan/', views.user_langganan, name='user_langganan'),
    path('api/save-speed-test/', views.save_speed_test, name='save_speed_test'),
    path('api/registrasi/', views.registrasi_pelanggan, name='registrasi_pelanggan'),
    path('api/admin/dashboard-stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
]
