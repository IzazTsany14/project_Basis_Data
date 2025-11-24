# GANTI SEMUA ISI admin.py DENGAN INI:

from django.contrib import admin
from .models import (
    AreaLayanan, JenisJasa, JenisPerangkat, Langganan,
    MetodePembayaran, PaketLayanan, Pelanggan, Pembayaran,
    PemesananJasa, PenempatanPerangkat, Perangkat,
    RiwayatTestingWifi, Teknisi
)

@admin.register(Pelanggan)
class PelangganAdmin(admin.ModelAdmin):
    list_display = ('id_pelanggan', 'nama_lengkap', 'email', 'no_telepon', 'tanggal_daftar')
    search_fields = ('nama_lengkap', 'email', 'no_telepon')
    readonly_fields = ('tanggal_daftar',)

@admin.register(Teknisi)
class TeknisiAdmin(admin.ModelAdmin):
    list_display = ('id_teknisi', 'nama_teknisi', 'role_akses', 'no_telepon', 'id_area_layanan')
    search_fields = ('nama_teknisi', 'email')
    list_filter = ('role_akses', 'id_area_layanan')

@admin.register(PaketLayanan)
class PaketLayananAdmin(admin.ModelAdmin):
    list_display = ('id_paket', 'nama_paket', 'kecepatan_mbps', 'harga')
    search_fields = ('nama_paket',)

@admin.register(Langganan)
class LanggananAdmin(admin.ModelAdmin):
    list_display = ('id_langganan', 'id_pelanggan', 'id_paket', 'tanggal_mulai', 'status_langganan')
    search_fields = ('id_pelanggan__nama_lengkap',)
    list_filter = ('status_langganan',)
    raw_id_fields = ('id_pelanggan', 'id_paket')

@admin.register(PemesananJasa)
class PemesananJasaAdmin(admin.ModelAdmin):
    list_display = ('id_pemesanan', 'id_pelanggan', 'id_jenis_jasa', 'id_teknisi', 'tanggal_pemesanan', 'status_pemesanan')
    search_fields = ('id_pelanggan__nama_lengkap', 'id_teknisi__nama_teknisi')
    list_filter = ('status_pemesanan', 'id_jenis_jasa')
    raw_id_fields = ('id_pelanggan', 'id_jenis_jasa', 'id_teknisi')
    readonly_fields = ('tanggal_pemesanan',)

@admin.register(RiwayatTestingWifi)
class RiwayatTestingWifiAdmin(admin.ModelAdmin):
    list_display = ('id_testing', 'id_langganan', 'waktu_testing', 'download_speed_mbps', 'upload_speed_mbps', 'ping_ms')
    search_fields = ('id_langganan__id_pelanggan__nama_lengkap',)
    raw_id_fields = ('id_langganan',)
    readonly_fields = ('waktu_testing',)

# Daftarkan model-model lainnya
admin.site.register(AreaLayanan)
admin.site.register(JenisJasa)
admin.site.register(JenisPerangkat)
admin.site.register(MetodePembayaran)
admin.site.register(Pembayaran)
admin.site.register(Perangkat)
admin.site.register(PenempatanPerangkat)
