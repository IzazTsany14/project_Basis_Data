# GANTI SEMUA ISI serializers.py DENGAN INI:

from rest_framework import serializers
from .models import (
    Pelanggan, Teknisi, PaketLayanan, Langganan,
    PemesananJasa, RiwayatTestingWifi, JenisJasa
)

# --- Serializer untuk Login ---

class LoginSerializer(serializers.Serializer):
    """
    Serializer untuk login.
    'login_id' bisa berupa 'email' (Pelanggan) atau 'username' (Teknisi/Admin).
    """
    login_id = serializers.CharField()
    password = serializers.CharField(write_only=True)


class PelangganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelanggan
        fields = ['id_pelanggan', 'nama_lengkap', 'email', 'no_telepon', 'alamat_pemasangan', 'tanggal_daftar']
        read_only_fields = ['id_pelanggan', 'tanggal_daftar']

class PelangganRegistrasiSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Pelanggan
        fields = ['nama_lengkap', 'email', 'no_telepon', 'alamat_pemasangan', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        pelanggan = Pelanggan(**validated_data)
        pelanggan.set_password(password)
        pelanggan.save()
        return pelanggan


class TeknisiSerializer(serializers.ModelSerializer):
    area_layanan = serializers.CharField(source='id_area_layanan.nama_area', read_only=True, allow_null=True)
    
    class Meta:
        model = Teknisi
        fields = ['id_teknisi', 'nama_teknisi', 'username', 'no_telepon', 'role_akses', 'id_area_layanan', 'area_layanan']
        read_only_fields = ['id_teknisi']


class PaketLayananSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaketLayanan
        fields = ['id_paket', 'nama_paket', 'kecepatan_mbps', 'harga', 'deskripsi']
        read_only_fields = ['id_paket']


class LanggananSerializer(serializers.ModelSerializer):
    nama_pelanggan = serializers.CharField(source='id_pelanggan.nama_lengkap', read_only=True)
    nama_paket = serializers.CharField(source='id_paket.nama_paket', read_only=True)
    harga_bulanan = serializers.DecimalField(source='id_paket.harga', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Langganan
        fields = ['id_langganan', 'id_pelanggan', 'id_paket', 'nama_pelanggan',
                  'nama_paket', 'harga_bulanan', 'tanggal_mulai', 'tanggal_akhir',
                  'status_langganan']
        read_only_fields = ['id_langganan']


class PemesananJasaSerializer(serializers.ModelSerializer):
    nama_pelanggan = serializers.CharField(source='id_pelanggan.nama_lengkap', read_only=True)
    nama_teknisi = serializers.CharField(source='id_teknisi.nama_teknisi', read_only=True, allow_null=True)
    nama_jasa = serializers.CharField(source='id_jenis_jasa.nama_jasa', read_only=True)

    class Meta:
        model = PemesananJasa
        fields = ['id_pemesanan', 'id_pelanggan', 'id_teknisi', 'id_jenis_jasa',
                  'nama_pelanggan', 'nama_teknisi', 'nama_jasa',
                  'tanggal_pemesanan', 'tanggal_jadwal', 'status_pemesanan', 'catatan']
        read_only_fields = ['id_pemesanan', 'tanggal_pemesanan']

class PemesananJasaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PemesananJasa
        # id_pelanggan dan id_jenis_jasa harus dikirim dari frontend
        fields = ['id_pelanggan', 'id_jenis_jasa', 'tanggal_jadwal', 'catatan']
        

class RiwayatTestingWifiSerializer(serializers.ModelSerializer):
    nama_pelanggan = serializers.CharField(source='id_langganan.id_pelanggan.nama_lengkap', read_only=True)
    nama_paket = serializers.CharField(source='id_langganan.id_paket.nama_paket', read_only=True)

    class Meta:
        model = RiwayatTestingWifi
        fields = ['id_testing', 'id_langganan', 'nama_pelanggan', 'nama_paket',
                  'waktu_testing', 'download_speed_mbps', 'upload_speed_mbps', 'ping_ms']
        read_only_fields = ['id_testing', 'waktu_testing']


class RiwayatTestingWifiCreateSerializer(serializers.Serializer):
    id_pelanggan = serializers.IntegerField(write_only=True)
    download_speed_mbps = serializers.DecimalField(max_digits=5, decimal_places=2)
    upload_speed_mbps = serializers.DecimalField(max_digits=5, decimal_places=2)
    ping_ms = serializers.IntegerField()

    def create(self, validated_data):
        id_pelanggan = validated_data.pop('id_pelanggan')

        try:
            # Temukan langganan aktif milik pelanggan
            langganan = Langganan.objects.filter(
                id_pelanggan=id_pelanggan,
                status_langganan='Aktif'
            ).latest('tanggal_mulai') # Ambil yang terbaru
        except Langganan.DoesNotExist:
            raise serializers.ValidationError("Tidak ada langganan aktif untuk pelanggan ini")

        # Buat riwayat tes dengan ID langganan yang ditemukan
        testing = RiwayatTestingWifi.objects.create(
            id_langganan=langganan,
            **validated_data
        )
        return testing