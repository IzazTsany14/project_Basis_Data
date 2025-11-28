# GANTI SEMUA ISI serializers.py DENGAN INI:

from rest_framework import serializers
from .models import (
    Pelanggan, Teknisi, PaketLayanan, Langganan,
    PemesananJasa, RiwayatTestingWifi, JenisJasa, AreaLayanan
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
    password_plain = serializers.SerializerMethodField()

    class Meta:
        model = Pelanggan
        fields = ['id_pelanggan', 'nama_lengkap', 'email', 'password_hash', 'password_plain', 'alamat_pemasangan', 'no_telepon', 'tanggal_daftar']
        read_only_fields = ['id_pelanggan', 'tanggal_daftar']

    def get_password_plain(self, obj):
        # For display purposes, show a masked password since we don't store plain text
        return "••••••••" if obj.password_hash else ""

class PelangganRegistrasiSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    area_layanan = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Pelanggan
        fields = ['nama_lengkap', 'email', 'no_telepon', 'alamat_pemasangan', 'password', 'area_layanan']

    def create(self, validated_data):
        area_name = validated_data.pop('area_layanan', None)
        password = validated_data.pop('password')

        # Find the area by name
        area = None
        if area_name:
            try:
                area = AreaLayanan.objects.get(nama_area=area_name)
            except AreaLayanan.DoesNotExist:
                pass  # Leave as None if not found

        pelanggan = Pelanggan(**validated_data)
        # Assign area only if the Pelanggan model actually defines it
        if area and hasattr(pelanggan, 'id_area_layanan'):
            pelanggan.id_area_layanan = area
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
    harga_bulanan = serializers.DecimalField(source='harga', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = PaketLayanan
        fields = ['id_paket', 'nama_paket', 'kecepatan_mbps', 'harga', 'harga_bulanan', 'deskripsi']
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
    # Return related objects as nested serializers/objects so frontend can access
    id_pelanggan = PelangganSerializer(read_only=True)
    id_teknisi = TeknisiSerializer(read_only=True, allow_null=True)
    nama_jasa = serializers.CharField(source='id_jenis_jasa.nama_jasa', read_only=True)
    alamat_pemasangan = serializers.CharField(source='id_pelanggan.alamat_pemasangan', read_only=True)
    # Try to provide area info: from pelanggan relation (if present), infer from address, or fallback to teknisi area
    area_layanan = serializers.SerializerMethodField()

    class Meta:
        model = PemesananJasa
        fields = ['id_pemesanan', 'id_pelanggan', 'id_teknisi', 'id_jenis_jasa',
                  'alamat_pemasangan', 'nama_jasa', 'area_layanan',
                  'tanggal_pemesanan', 'tanggal_jadwal', 'status_pemesanan', 'catatan']
        read_only_fields = ['id_pemesanan', 'tanggal_pemesanan']

    def get_area_layanan(self, obj):
        # 1) If pelanggan has id_area_layanan (older schema), use it
        pelanggan = getattr(obj, 'id_pelanggan', None)
        if pelanggan is not None:
            if hasattr(pelanggan, 'id_area_layanan') and getattr(pelanggan, 'id_area_layanan'):
                return getattr(pelanggan.id_area_layanan, 'nama_area', None)

            # 2) Try to infer from alamat_pemasangan by checking AreaLayanan names
            alamat = getattr(pelanggan, 'alamat_pemasangan', '') or ''
            if alamat:
                from .models import AreaLayanan
                try:
                    areas = AreaLayanan.objects.all()
                    alamat_lower = alamat.lower()
                    for a in areas:
                        if a.nama_area and a.nama_area.lower() in alamat_lower:
                            return a.nama_area
                except Exception:
                    pass

        # 3) Fallback: if teknisi assigned, return teknisi area
        teknisi = getattr(obj, 'id_teknisi', None)
        if teknisi and hasattr(teknisi, 'id_area_layanan') and teknisi.id_area_layanan:
            return getattr(teknisi.id_area_layanan, 'nama_area', None)

        return None

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
        # Note: model `RiwayatTestingWifi` (from .sql) does not have a 'connection_type' column.
        # Do not include it here to avoid ImproperlyConfigured errors.
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


class AreaLayananSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaLayanan
        fields = ['id_area_layanan', 'nama_area', 'kode_pos']
