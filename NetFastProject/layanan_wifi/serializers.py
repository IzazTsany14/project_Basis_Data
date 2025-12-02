# GANTI SEMUA ISI serializers.py DENGAN INI:

from rest_framework import serializers
from .models import (
    Pelanggan, Teknisi, PaketLayanan, Langganan,
    PemesananJasa, RiwayatTestingWifi, JenisJasa, AreaLayanan, JenisPerangkat
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
    username = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = Pelanggan
        fields = ['nama_lengkap', 'username', 'email', 'no_telepon', 'alamat_pemasangan', 'password']

    def validate_username(self, value):
        from .models import Teknisi
        if Teknisi.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username sudah digunakan.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username', None)  # Remove username since it's not stored (optional)

        # Ensure only valid fields are passed to Pelanggan constructor
        pelanggan_data = {k: v for k, v in validated_data.items() if k in ['nama_lengkap', 'email', 'no_telepon', 'alamat_pemasangan']}
        pelanggan = Pelanggan(**pelanggan_data)
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
    # Return numeric price so frontend can safely call numeric methods like toLocaleString
    harga_bulanan = serializers.SerializerMethodField()

    class Meta:
        model = PaketLayanan
        fields = ['id_paket', 'nama_paket', 'kecepatan_mbps', 'harga', 'harga_bulanan', 'deskripsi']
        read_only_fields = ['id_paket']

    def get_harga_bulanan(self, obj):
        try:
            return float(obj.harga) if obj.harga is not None else None
        except Exception:
            return None


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
    # Accept primary keys for related fields and create model instance
    id_pelanggan = serializers.PrimaryKeyRelatedField(queryset=Pelanggan.objects.all(), write_only=True)
    id_jenis_jasa = serializers.PrimaryKeyRelatedField(queryset=JenisJasa.objects.all())

    class Meta:
        model = PemesananJasa
        fields = ['id_pelanggan', 'id_jenis_jasa', 'tanggal_jadwal', 'catatan']

    def create(self, validated_data):
        # Ensure status_pemesanan is set by the view, but default in model if not provided
        return PemesananJasa.objects.create(**validated_data)
        

class RiwayatTestingWifiSerializer(serializers.ModelSerializer):
    nama_pelanggan = serializers.SerializerMethodField()
    nama_paket = serializers.SerializerMethodField()
    connection_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RiwayatTestingWifi
        fields = ['id_testing', 'id_langganan', 'nama_pelanggan', 'nama_paket',
                  'waktu_testing', 'download_speed_mbps', 'upload_speed_mbps', 'ping_ms', 'connection_type']
        read_only_fields = ['id_testing', 'waktu_testing']

    def get_nama_pelanggan(self, obj):
        if obj.id_langganan and obj.id_langganan.id_pelanggan:
            return obj.id_langganan.id_pelanggan.nama_lengkap
        return None

    def get_nama_paket(self, obj):
        if obj.id_langganan and obj.id_langganan.id_paket:
            return obj.id_langganan.id_paket.nama_paket
        return None

    def get_connection_type(self, obj):
        # Determine connection type heuristically from download speed
        try:
            download = float(obj.download_speed_mbps) if obj.download_speed_mbps is not None else 0.0
        except Exception:
            return 'Unknown'

        if download >= 100:
            return 'Fiber Optic'
        if download >= 50:
            return 'Cable Broadband'
        if download >= 25:
            return 'DSL'
        if download >= 10:
            return 'Mobile Data'
        return 'Slow Connection'


class RiwayatTestingWifiCreateSerializer(serializers.Serializer):
    id_pelanggan = serializers.IntegerField(write_only=True)
    download_speed_mbps = serializers.DecimalField(max_digits=7, decimal_places=2)
    upload_speed_mbps = serializers.DecimalField(max_digits=7, decimal_places=2)
    ping_ms = serializers.IntegerField()
    connection_type = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def create(self, validated_data):
        id_pelanggan = validated_data.pop('id_pelanggan')
        # pop optional connection_type so it won't be used in model create
        connection_type = validated_data.pop('connection_type', None)

        try:
            # Temukan langganan aktif milik pelanggan
            langganan = Langganan.objects.filter(
                id_pelanggan=id_pelanggan,
                status_langganan__iexact='aktif'
            ).latest('tanggal_mulai') # Ambil yang terbaru
        except Langganan.DoesNotExist:
            langganan = None

        # Buat riwayat tes dengan ID langganan yang ditemukan (boleh None)
        testing = RiwayatTestingWifi.objects.create(
            id_langganan=langganan,
            download_speed_mbps=validated_data.get('download_speed_mbps'),
            upload_speed_mbps=validated_data.get('upload_speed_mbps'),
            ping_ms=validated_data.get('ping_ms')
        )

        # Attach optional connection_type to instance for serializer output (non-persistent)
        if connection_type:
            setattr(testing, '_connection_type', connection_type)

        return testing


class AreaLayananSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaLayanan
        fields = ['id_area_layanan', 'nama_area', 'kode_pos']


class JenisPerangkatSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisPerangkat
        fields = ['id_jenis_perangkat', 'nama_jenis']
        model = AreaLayanan
        fields = ['id_area_layanan', 'nama_area', 'kode_pos']


class JenisPerangkatSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisPerangkat
        fields = ['id_jenis_perangkat', 'nama_jenis']
